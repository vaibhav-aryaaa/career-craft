import pdfplumber
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Career Coach! The server is running."

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            with pdfplumber.open(file) as pdf:
                # Extract text from all pages
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
            
            # Return the filename and a preview of the extracted content
            return jsonify({
                'filename': file.filename,
                'content_preview': full_text[:500] # Show first 500 characters
            })
        except Exception as e:
            return jsonify({'error': f"Error processing PDF: {str(e)}"}), 500
    else:
        return jsonify({'error': 'Invalid file type, please upload a PDF'}), 400