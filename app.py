from flask import Flask, request, jsonify
from pdf_processor import PDFProcessor
import os
import json
import base64

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
UPLOAD_FOLDER = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        base64_file = data.get("file")
        template_file = data.get("template")
        file_name = data.get("fileName", "uploaded.pdf")

        if not base64_file:
            return jsonify({"error": "No file data provided"}), 400

        try:
            file_data = base64.b64decode(base64_file, validate=True)
        except base64.binascii.Error:
            return jsonify({"error": "Invalid base64 encoding"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, "wb") as f:
            f.write(file_data)

        if os.path.exists(file_path):
            processor = PDFProcessor(file_path)
            result = processor.extract_data(template_file)
            os.remove(file_path)
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to save the file"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# def process_pdf():
#     template_file = request.form.get('template')
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400

#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if file and file.filename.endswith('.pdf'):
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)
        
#         try:
#             # if template_file:
#             #     template_content = json.load(template_file)
#             # else:
#             #     template_content = {}
                
#             processor = PDFProcessor(file_path)
#             result = processor.extract_data(template_file)
#             os.remove(file_path)
#             return jsonify(result)
#         except Exception as e:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
