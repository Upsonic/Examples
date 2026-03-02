import glob
import os
import tempfile

from upsonic.ocr import OCR
from upsonic.ocr.layer_1.engines import EasyOCREngine
from upsonic.tools.config import tool


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
