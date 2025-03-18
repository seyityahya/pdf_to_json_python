from flask import Flask, request, jsonify
from pdf_processor import PDFProcessor
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    template_file = request.form.get('template')
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        try:
            # if template_file:
            #     template_content = json.load(template_file)
            # else:
            #     template_content = {}
                
            processor = PDFProcessor(file_path)
            result = processor.extract_data(template_file)
            os.remove(file_path)
            return jsonify(result)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Development için 
    app.run(
        host='127.0.0.1',  # Sadece localhost'tan erişime izin ver
        port=5000,         # Port numarası
        debug=True,        # Geliştirme modu açık
        use_reloader=True  # Kod değişikliklerinde otomatik yeniden başlatma
    )
