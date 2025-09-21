import fitz  # PyMuPDF
import pdfplumber
import docx
import docx2txt
import os

class TextExtractor:
    def extract_text(self, file_path):
        if file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._extract_from_docx(file_path)
        elif file_path.endswith('.txt'):
            return self._extract_from_txt(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def _clean_text(self, text):
        if text is None:
            return ""
        # Remove non-UTF-8 characters by encoding and decoding with replacement
        return text.encode('utf-8', 'replace').decode('utf-8')
    
    def _extract_from_pdf(self, file_path):
        text = ""
        # Try PyMuPDF first
        try:
            doc = fitz.open(file_path)
            # Check if PDF is encrypted
            if doc.is_encrypted:
                # Try to decrypt with empty password
                doc.authenticate("")
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
        except Exception as e:
            print(f"PyMuPDF failed: {e}, trying pdfplumber")
            # Fallback to pdfplumber
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                print(f"pdfplumber also failed: {e2}")
                text = f"Error extracting PDF text: {e}, {e2}"
        
        return self._clean_text(text)
    
    def _extract_from_docx(self, file_path):
        try:
            text = docx2txt.process(file_path)
        except:
            try:
                doc = docx.Document(file_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            except Exception as e:
                text = f"Error extracting DOCX text: {e}"
        return self._clean_text(text)
    
    def _extract_from_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            # Try with error handling
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                text = file.read()
        except Exception as e:
            text = f"Error extracting TXT text: {e}"
        return self._clean_text(text)