# ocr_module.py
from PIL import Image
import pytesseract

def extract_text_from_receipt(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"[OCR Error] {e}")
        return ""