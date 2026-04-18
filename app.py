from flask import Flask, render_template, request, jsonify, send_from_directory
import os

from utils.speech_to_text import transcribe_video
from utils.highlight_detection import get_highlights
from utils.video_editor import generate_clips

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["video"]

        if file.filename == "":
            return "No file selected"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        print("Step 1: Transcribing...")
        segments = transcribe_video(filepath)

        print("Step 2: Finding highlights...")
        highlights = get_highlights(segments)

        print("Step 3: Generating clips...")
        clips = generate_clips(filepath, highlights)

        return jsonify({"clips": clips})

    except Exception as e:
        print(f"💥 APP ERROR: {str(e)}") # This will force the error to show in your terminal!
        return jsonify({"error": str(e)}), 400 # This sends proper JSON so the frontend doesn't crash
@app.route('/outputs/<filename>')
def serve_video(filename):
    # This gives the frontend permission to load files from the outputs folder
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)
if __name__ == "__main__":
    app.run(debug=True)