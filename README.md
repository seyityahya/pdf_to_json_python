# PDF to JSON API

This API service extracts specific data from PDF files based on provided templates and returns the data in JSON format.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## API Usage

### Process PDF

**Endpoint:** POST /process-pdf

**Request:**
- Content-Type: multipart/form-data
- Body:
  - file: PDF file
  - template: JSON object defining the fields to extract

**Example template:**
```json
{
  "Description": {
    "pattern": "Description"
  },
  "ISIN": {
    "pattern": "ISIN"
  },
  "CUSIP": {
    "pattern": "CUSIP"
  },
  "Price": {
    "pattern": "Price"
  }
}
```

**Response:**
```json
{
  "Description": "Sample Description",
  "ISIN": "US1234567890",
  "CUSIP": "123456789",
  "Price": "100.00"
}
```
