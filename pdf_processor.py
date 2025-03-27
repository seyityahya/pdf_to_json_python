import pdfplumber
import re

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_data(self, template_content):
        text = self._extract_text_from_pdf()
        return self._process_lines2(text, template_content)

    def _extract_text_from_pdf(self):
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    def _process_lines2(self, text, template_content):
        result = []
        if not template_content:
            return False
        match = re.search(template_content, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            lines = [line.strip() for line in content.split('\n') if line.strip()]
        
            for line in lines:
                print("line", line)
                ticker_match = re.search(r'(\w+)\s+(\d{4}-\d+[A-Z]?)\s+([A-Z0-9]+)', line)
                isin_match = re.search(r'(US\w{10})', line)
                cusip_match = re.search(r'(?:^|\s)([A-Z0-9]{9}|BCC[A-Z0-9]{6})(?:\s|$)', line)
                price_match = re.search(r'(\d+\.\d{1,5})', line)
            
                if price_match:
                    entry = {
                        "isin": isin_match.group(1) if isin_match else None,
                        "cusip": cusip_match.group(1) if cusip_match else None,
                        "price": float(price_match.group(1)),
                        "ticker": f"{ticker_match.group(1)} {ticker_match.group(2)} {ticker_match.group(3)}" if ticker_match else None
                    }
                    if entry["isin"] or entry["cusip"]:
                        result.append(entry)
    
        return result

    # def _process_lines(self, text):
    #     result = []
    #     lines = [line.strip() for line in text.split('\n') if line.strip()]
        
    #     for line in lines:
    #         if re.match(r'\d{2}/\d{2}/\d{4}', line):
    #             isin_match = re.search(r'(US\w{10})', line)
    #             cusip_match = re.search(r'(?:^|\s)([A-Z0-9]{9}|BCC[A-Z0-9]{6})(?:\s|$)', line)
    #             price_match = re.search(r'(\d+\.\d{3})\s*$', line)

    #             if isin_match and cusip_match and price_match:
    #                 entry = {
    #                     "isin": isin_match.group(1),
    #                     "cusip": cusip_match.group(1),
    #                     "price": float(price_match.group(1))
    #                 }
    #                 result.append(entry)
    #                 # print(f"Added entry: {entry}")  # Debug

    #     # print(f"Final result: {result}")  # Debug
    #     return result
