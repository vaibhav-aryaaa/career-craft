import os
import json
import pdfplumber
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Please upload a valid PDF file'}), 400

    try:
        with pdfplumber.open(file) as pdf:
            full_text = "".join(page.extract_text() for page in pdf.pages)

        # --- AI Analysis Step ---
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert AI career coach. Analyze the following resume text and provide a concise analysis.

        Resume Text:
        "{full_text}"

        Provide your analysis in a structured JSON format with two main keys:
        1. "career_suggestions": A list of 2-3 suitable job titles.
        2. "skill_analysis": A brief paragraph analyzing the candidate's strengths based on the resume.
        
        Do not include any text or formatting outside of the JSON object.
        """
        
        response = model.generate_content(prompt)
        
        # Clean and parse the JSON response from the AI
        ai_response_text = response.text.strip().replace('```json', '').replace('```', '')
        ai_response_json = json.loads(ai_response_text)

        return jsonify(ai_response_json)

    except Exception as e:
        # This will catch errors from PDF processing or the AI call
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500