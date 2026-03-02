import csv
import glob
import os
import tempfile
from datetime import datetime
from pathlib import Path

from upsonic.ocr import OCR
from upsonic.ocr.layer_1.engines import EasyOCREngine
from pydantic import ValidationError
from upsonic.tools.config import tool

from models import ExpenseData

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "expenses.csv"
CSV_FIELDS = ["date", "amount", "merchant", "category", "description", "ocr_confidence", "created_at"]


def _find_latest_telegram_image() -> str | None:
    """Find the most recently created telegram_media temp file."""
    tmp_dir = tempfile.gettempdir()
    candidates = glob.glob(os.path.join(tmp_dir, "telegram_media_*"))
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


@tool
def ocr_extract_text(image_path: str = "") -> str:
    """Extracts text from receipt/invoice photos sent by the user.

    Reads text in the image using EasyOCR and returns it with confidence scores.
    Call this tool when the user sends a photo from Telegram.
    image_path can be left empty; the system will automatically find the incoming photo's path.

    Args:
        image_path: Image file path (can be left empty, auto-detected)

    Returns:
        OCR result: extracted text blocks, confidence scores, and average confidence score
    """
    if not image_path or not os.path.isfile(image_path):
        discovered = _find_latest_telegram_image()
        if discovered:
            image_path = discovered
        else:
            return "ERROR: No image found to process. Please send a photo again."

    try:
        engine = EasyOCREngine(languages=["tr"], gpu=False, rotation_fix=True)
        ocr = OCR(layer_1_ocr_engine=engine)
        result = ocr.process_file(image_path)
    except Exception as e:
        return f"ERROR: OCR operation failed: {e}"

    lines = []
    total_confidence = 0.0
    block_count = 0

    for block in result.blocks:
        text = block.text.strip()
        if not text:
            continue
        conf = block.confidence
        total_confidence += conf
        block_count += 1
        lines.append(f"[{conf:.0%}] {text}")

    if block_count == 0:
        return "OCR could not detect any text. The image may not be clear."

    avg_confidence = total_confidence / block_count

    output = f"=== OCR Result (Average Confidence: {avg_confidence:.0%}) ===\n"
    output += "\n".join(lines)

    if avg_confidence < 0.6:
        output += (
            "\n\nWARNING: OCR confidence score is low (<60%). "
            "Results may be incorrect, ask the user for confirmation."
        )

    return output


@tool
def save_expense(
    date: str,
    amount: float,
    merchant: str,
    category: str,
    description: str = "",
    ocr_confidence: float = 0.0,
) -> str:
    """Saves an expense record to a CSV file.

    Validates all fields via ExpenseData model, performs duplicate checking,
    and returns a monthly summary. All expenses are stored in a single CSV file.

    Args:
        date: Invoice date (in YYYY-MM-DD format, e.g. 2026-02-14)
        amount: Total amount as a number (e.g. 415.20)
        merchant: Merchant/store name
        category: Expense category (Groceries, Restaurant, Transportation, Health, Bills, Clothing, Technology, Banking, Other)
        description: Optional description
        ocr_confidence: OCR confidence score between 0 and 1 (from ocr_extract_text output)

    Returns:
        Save result and monthly expense summary
    """
    # Validate through Pydantic model
    try:
        expense = ExpenseData(
            date=date,
            amount=amount,
            merchant=merchant,
            category=category,
            description=description or None,
            ocr_confidence=ocr_confidence,
        )
    except ValidationError as e:
        errors = "; ".join(
            f"{err['loc'][0]}: {err['msg']}" for err in e.errors()
        )
        return f"VALIDATION ERROR: {errors}"

    # Read existing records for duplicate check
    existing_rows = []
    if CSV_PATH.exists():
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_rows = list(reader)

    # Duplicate check: same date + amount + merchant
    for row in existing_rows:
        try:
            if (
                row["date"] == date
                and float(row["amount"]) == amount
                and row["merchant"].lower() == merchant.lower()
            ):
                return (
                    f"DUPLICATE: {amount:.2f} TL for {merchant} on {date} "
                    f"is already recorded. Let me know if you want to save it again."
                )
        except (ValueError, KeyError):
            continue

    # Write new record
    is_new_file = not CSV_PATH.exists()
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(
            {
                "date": expense.date,
                "amount": expense.amount,
                "merchant": expense.merchant,
                "category": expense.category,
                "description": expense.description or "",
                "ocr_confidence": expense.ocr_confidence,
                "created_at": datetime.now().isoformat(),
            }
        )

    # Monthly summary
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        target_year = target_date.year
        target_month = target_date.month
    except ValueError:
        target_year = datetime.now().year
        target_month = datetime.now().month

    # Re-read all records including the new one
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    month_total = 0.0
    month_count = 0
    for row in all_rows:
        try:
            row_date = datetime.strptime(row["date"], "%Y-%m-%d")
            if row_date.year == target_year and row_date.month == target_month:
                month_total += float(row["amount"])
                month_count += 1
        except (ValueError, KeyError):
            continue

    month_name = target_date.strftime("%B %Y")
    return (
        f"Saved: {amount:.2f} TL - {merchant} ({category})\n"
        f"{month_name} total: {month_total:,.2f} TL ({month_count} transactions)"
    )


@tool
def get_monthly_summary(year: int, month: int) -> str:
    """Returns the expense summary for a specified month.

    Groups by category and calculates the total amount.

    Args:
        year: Year (e.g. 2026)
        month: Month (1-12)

    Returns:
        Monthly expense summary: breakdown by category and total
    """
    if not CSV_PATH.exists():
        return "No expenses recorded yet."

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    category_totals: dict[str, float] = {}
    category_counts: dict[str, int] = {}
    total = 0.0

    for row in all_rows:
        try:
            row_date = datetime.strptime(row["date"], "%Y-%m-%d")
            if row_date.year == year and row_date.month == month:
                amt = float(row["amount"])
                cat = row.get("category", "Other")
                category_totals[cat] = category_totals.get(cat, 0.0) + amt
                category_counts[cat] = category_counts.get(cat, 0) + 1
                total += amt
        except (ValueError, KeyError):
            continue

    if not category_totals:
        return f"No expenses recorded for {year}/{month:02d}."

    lines = [f"{year}/{month:02d} Expense Summary", "-" * 30]
    for cat in sorted(category_totals, key=lambda c: category_totals[c], reverse=True):
        amt = category_totals[cat]
        cnt = category_counts[cat]
        pct = (amt / total) * 100
        lines.append(f"  {cat}: {amt:,.2f} TL ({cnt} transactions, {pct:.0f}%)")

    lines.append("-" * 30)
    lines.append(f"  TOTAL: {total:,.2f} TL")

    return "\n".join(lines)
