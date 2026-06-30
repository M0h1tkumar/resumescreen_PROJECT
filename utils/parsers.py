import PyPDF2
import docx
from typing import Optional

def parse_pdf(file_path: str) -> Optional[str]:
    """Extract text from a PDF file."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return None

def parse_docx(file_path: str) -> Optional[str]:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
        return None

def extract_text(file_path: str) -> Optional[str]:
    """General extraction router based on file extension."""
    if file_path.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return None
