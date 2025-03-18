import pdfplumber
import re

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_data(self, template):
        text = self._extract_text_from_pdf()
        print("Extracted Text:", text)  # Debug için
        return self._process_lines(text)

    def _extract_text_from_pdf(self):
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"PDF okuma hatası: {str(e)}")
            raise

    def _process_lines(self, text):
        result = []
        # Satırları böl
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Tarih ile başlayan satırları işle
            if re.match(r'\d{2}/\d{2}/\d{4}', line):
                # ISIN (US ile başlayan 12 karakter)
                isin_match = re.search(r'(US\w{10})', line)
                # CUSIP (9 karakter veya BCC ile başlayan)
                cusip_match = re.search(r'(?:^|\s)([A-Z0-9]{9}|BCC[A-Z0-9]{6})(?:\s|$)', line)
                # Price (sondaki sayısal değer)
                price_match = re.search(r'(\d+\.\d{3})\s*$', line)
                
                print(f"Processing line: {line}")  # Debug
                print(f"ISIN match: {isin_match.group(1) if isin_match else None}")  # Debug
                print(f"CUSIP match: {cusip_match.group(1) if cusip_match else None}")  # Debug
                print(f"Price match: {price_match.group(1) if price_match else None}")  # Debug

                if isin_match and cusip_match and price_match:
                    entry = {
                        "isin": isin_match.group(1),
                        "cusip": cusip_match.group(1),
                        "price": float(price_match.group(1))
                    }
                    result.append(entry)
                    print(f"Added entry: {entry}")  # Debug

        print(f"Final result: {result}")  # Debug
        return result
