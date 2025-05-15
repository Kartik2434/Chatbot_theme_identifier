import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

SUPPORTED_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        # Convert PDF pages to images, OCR each page
        pages = convert_from_path(file_path)
        text_by_page = []
        for i, page_img in enumerate(pages):
            text = pytesseract.image_to_string(page_img)
            text_by_page.append(f"[Page {i+1}]\n{text}")
        return '\n'.join(text_by_page)
    elif ext in SUPPORTED_IMAGE_EXTS:
        # OCR image file
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    elif ext in {'.txt'}:
        # Read text file directly
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "[Unsupported file type for OCR]" 