# extract_text.py

import os
import pytesseract
from pdf2image import convert_from_path
import docx

# ---- UPDATE THIS PATH TO TESSERACT EXECUTABLE ----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Tesseract languages: English + Malayalam
TESSERACT_LANG = "eng+mal"

# Folder containing PDFs/DOCXs
INPUT_FOLDER = "input_docs"  # <-- updated folder name
OUTPUT_FOLDER = "extracted_texts"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    try:
        POPPLER_PATH = r"E:\Release-25.07.0-0\poppler-25.07.0\Library\bin"
        pages = convert_from_path(file_path, dpi=300, poppler_path=POPPLER_PATH)
        for i, page in enumerate(pages):
            page_text = pytesseract.image_to_string(page, lang=TESSERACT_LANG)
            text += f"\n\n--- Page {i+1} ---\n{page_text}\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
    return text

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print(f"Skipping unsupported file type: {file_path}")
        return ""

# ---------------------------
# Process all files in directory
# ---------------------------
for filename in os.listdir(INPUT_FOLDER):
    file_path = os.path.join(INPUT_FOLDER, filename)
    print(f"\nProcessing {filename}...")

    text = extract_text_from_file(file_path)
    if text.strip():
        output_file = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(filename)[0]}_text.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved extracted text to {output_file}")
    else:
        print(f"No text extracted from {filename}")