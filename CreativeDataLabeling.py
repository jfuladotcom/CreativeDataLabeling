import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from google import genai

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

GEMINI_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it before running the application.")
client = genai.Client(api_key=GEMINI_API_KEY)

DATA = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('CreativeDataLabeling.html')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        df = pd.read_csv(file_path)
        DATA['df'] = df
        df_json = df.to_json(orient='split')
        return jsonify({
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'df_json': df_json
        })
    except Exception as e:
        return jsonify({'error': f'Failed to process CSV: {str(e)}'}), 400

@app.route('/label', methods=['POST'])
def label():
    try:
        data = request.get_json()
        df_json = data.get('df_json')
        column = data.get('column')
        prompt = data.get('prompt')

        if not (df_json and column and prompt):
            return jsonify({'error': 'Missing data, column, or prompt.'}), 400

        df = pd.read_json(df_json, orient='split')
        sample = df[column].dropna().astype(str).head(10).tolist()
        sample_text = "\n".join(f"- {row}" for row in sample)

        gemini_prompt = (
            f"You are an expert data annotator. Given the labeling rule:\n"
            f"'{prompt}'\n"
            f"Apply this rule to each example below. For each, reply with either 'LABEL' or 'NO LABEL'.\n"
            f"Examples:\n{sample_text}"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=gemini_prompt
        )
        answer = response.text.strip() if response.text else ""
        results = []
        for line in answer.splitlines():
            label = 1 if 'LABEL' in line.upper() and 'NO LABEL' not in line.upper() else 0
            results.append(label)
        results = (results + [0]*len(sample))[:len(sample)]
        labeled = list(zip(sample, results))

        return jsonify({
            'examples': labeled,
            'raw_response': answer
        })
    except Exception as e:
        return jsonify({'error': f'Gemini labeling failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
