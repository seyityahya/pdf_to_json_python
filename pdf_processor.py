import pdfplumber
import re

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_data(self, template_content):
        #print("template", template_content)
        text = self._extract_text_from_pdf()
        print("Extracted Text:", text)  # Debug için
        return self._process_lines2(text)

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

    def _process_lines2(self, text):
        result = []
        # İki metin arasındaki verileri al
        match = re.search(r'Valuation Date(.*?)Natixis may use', text, re.DOTALL)
        # match = re.search(r'These prices are indicative only(.*?)VALUATION DISCLAIMER', text, re.DOTALL)
        # match = re.search(r'Description(.*?)Page 2 of 2', text, re.DOTALL)
        # match = re.search(r'CUSIP/ISIN(.*?)IMPORTANT EXPLANATION', text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Satırları böl
            lines = [line.strip() for line in content.split('\n') if line.strip()]
        
            for line in lines:
                print("line", line)
                # ISIN (US ile başlayan 12 karakter)
                isin_match = re.search(r'(US\w{10})', line)
                # CUSIP (9 karakter veya BCC ile başlayan)
                cusip_match = re.search(r'(?:^|\s)([A-Z0-9]{9}|BCC[A-Z0-9]{6})(?:\s|$)', line)
                # Price (sondaki sayısal değer)
                price_match = re.search(r'(\d+\.\d{3})', line)
            
                if price_match:
                    entry = {
                        "isin": isin_match.group(1) if isin_match else None,
                        "cusip": cusip_match.group(1) if cusip_match else None,
                        "price": float(price_match.group(1))
                    }
                    if entry["isin"] or entry["cusip"]:
                        result.append(entry)
    
        return result

    def _process_lines(self, text):
        result = []
        # Satırları böl
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Tarih ile başlayan satırları işle
            if re.match(r'\d{2}/\d{2}/\d{4}', line):
                # ISIN (US ile başlayan 12 karakter)
                print("line", line)
                isin_match = re.search(r'(US\w{10})', line)
                # CUSIP (9 karakter veya BCC ile başlayan)
                cusip_match = re.search(r'(?:^|\s)([A-Z0-9]{9}|BCC[A-Z0-9]{6})(?:\s|$)', line)
                # Price (sondaki sayısal değer)
                price_match = re.search(r'(\d+\.\d{3})\s*$', line)
                
                # print(f"Processing line: {line}")  # Debug
                # print(f"ISIN match: {isin_match.group(1) if isin_match else None}")  # Debug
                # print(f"CUSIP match: {cusip_match.group(1) if cusip_match else None}")  # Debug
                # print(f"Price match: {price_match.group(1) if price_match else None}")  # Debug

                if isin_match and cusip_match and price_match:
                    entry = {
                        "isin": isin_match.group(1),
                        "cusip": cusip_match.group(1),
                        "price": float(price_match.group(1))
                    }
                    result.append(entry)
                    # print(f"Added entry: {entry}")  # Debug

        # print(f"Final result: {result}")  # Debug
        return result
