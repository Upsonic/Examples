import os

from upsonic.ocr import OCR
from upsonic.ocr.layer_1.engines import EasyOCREngine
from upsonic.tools.config import tool


_engine = EasyOCREngine(languages=["en", "tr"], gpu=False, rotation_fix=True)
_ocr = OCR(layer_1_ocr_engine=_engine)

WORKSPACE: str = os.path.join(os.path.dirname(__file__), "workspace")


@tool(timeout=300.0)
def ocr_extract_text(image_path: str) -> str:
    """Extracts text from a receipt image (PNG, JPG) using OCR.

    Use this for image files. For PDFs, read them directly — no need to call this tool.

    Args:
        image_path: Absolute or workspace-relative path to the image file.

    Returns:
        Extracted text blocks with confidence scores, or an error message.
    """
    # Resolve workspace-relative paths
    if not os.path.isabs(image_path):
        image_path = os.path.join(WORKSPACE, image_path)

    if not os.path.isfile(image_path):
        return f"ERROR: File not found: {image_path}"

    try:
        result = _ocr.process_file(image_path)
    except Exception as e:
        return f"ERROR: OCR failed: {e}"

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
        return "OCR could not detect any text. The image may be unclear or empty."

    avg_confidence = total_confidence / block_count
    output = f"=== OCR Result (avg confidence: {avg_confidence:.0%}) ===\n" + "\n".join(lines)

    if avg_confidence < 0.6:
        output += "\n\nWARNING: Low confidence (<60%). Results may be inaccurate."

    return output