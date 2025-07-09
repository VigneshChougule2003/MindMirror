# api2.py
from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import json

app = Flask(__name__)

DATA_DIR = os.path.join("data")
OUTPUT_FILE = os.path.join("output", "psych_analysis.txt")
SUMMARY_FILE = os.path.join("output", "summary.json")
FRONTEND_DIR = os.path.join("frontend")

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index2.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".csv"):
        os.makedirs(DATA_DIR, exist_ok=True)
        file_path = os.path.join(DATA_DIR, "categorized_watch_history.csv")
        file.save(file_path)
        return jsonify({"message": "Categorized CSV uploaded successfully"}), 200

    return jsonify({"error": "Invalid file type. Please upload a .csv file."}), 400

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return jsonify({"error": "GET not supported. Use POST."}), 405
    try:
        subprocess.run(["python", "app.py", "--skip-parse"], check=True)
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            return jsonify({"error": "Analysis file not found"}), 500

        if os.path.exists(SUMMARY_FILE):
            with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
                summary_data = json.load(f)
        else:
            summary_data = {}

        return jsonify({"analysis": content, "summary": summary_data})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Analysis process failed"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
