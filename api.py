from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import traceback

from components.history_parser import WatchHistoryParser
from components.classifier_model import classify_user_content
from rag_module.rag_engine import analyze_psychology_from_summary

app = Flask(__name__, static_folder="frontend")
CORS(app)

UPLOAD_FOLDER = "data"
PARSED_CSV = os.path.join(UPLOAD_FOLDER, "parsed_watch_history.csv")
HTML_FILE = os.path.join(UPLOAD_FOLDER, "watch-history.html")
SUMMARY_TXT = os.path.join("output", "summary.txt")
ANALYSIS_TXT = os.path.join("output", "psych_analysis.txt")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("frontend", path)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")
        if not file:
            print("❌ No file received.")
            return jsonify({"error": "No file uploaded."}), 400

        print("📥 File received:", file.filename)
        file.save(HTML_FILE)
        print(f"✅ File saved to {HTML_FILE}")

        # Step 1: Parse HTML to CSV
        print("🔍 Parsing watch-history.html...")
        parser = WatchHistoryParser(input_path=HTML_FILE, output_path=PARSED_CSV)
        parser.run()
        print("✅ Parsing complete")

        # Step 2: Classify
        print("📊 Classifying video content...")
        summary = classify_user_content()
        with open(SUMMARY_TXT, "w") as f:
            f.write(summary)
        print("✅ Classification complete")
        print("📝 Summary:\n", summary)

        # Step 3: Analyze
        print("🧠 Performing psychological analysis...")
        result = analyze_psychology_from_summary(summary)
        with open(ANALYSIS_TXT, "w") as f:
            f.write(result)
        print("✅ Analysis complete")

        return jsonify({
            "message": "✅ Upload and analysis successful!",
            "summary": summary,
            "result": result
        })

    except Exception as e:
        print("❌ Exception during upload/analysis:")
        traceback.print_exc()
        return jsonify({"error": f"❌ Failed during processing: {str(e)}"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        with open(SUMMARY_TXT, "r") as f:
            summary = f.read()
        result = analyze_psychology_from_summary(summary)
        with open(ANALYSIS_TXT, "w") as f:
            f.write(result)
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"❌ Analysis failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
