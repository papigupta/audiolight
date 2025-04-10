from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import time
import requests

app = Flask(__name__)
CORS(app)

def generate_audio(text, output_filename):
    aiff_file = output_filename.replace(".wav", ".aiff")
    say_command = f'say -v Alex -o "{aiff_file}" "{text}"'
    print("Running say command:", say_command)

    try:
        result = subprocess.run(say_command, shell=True, capture_output=True, text=True, check=True)
        print("say output:", result.stdout)
        print("say errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("say FAILED:", e)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return False

    ffmpeg_command = f'ffmpeg -y -i "{aiff_file}" -ac 1 -ar 16000 "{output_filename}"'
    print("Running ffmpeg command:", ffmpeg_command)

    try:
        result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True, check=True)
        print("ffmpeg output:", result.stdout)
        print("ffmpeg errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("ffmpeg FAILED:", e)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return False

    if os.path.exists(aiff_file):
        os.remove(aiff_file)

    return True

def run_forced_alignment(audio_file, transcript):
    gentle_url = "http://127.0.0.1:8767/transcriptions?async=false"
    try:
        with open(audio_file, 'rb') as f:
            files = {
                'audio': f,
                'transcript': (None, transcript)
            }
            response = requests.post(gentle_url, files=files)
        if response.status_code != 200:
            print("Gentle failed:", response.text)
            return None
        return response.json()
    except Exception as e:
        print("Error calling Gentle:", e)
        return None

@app.route('/generate-reading', methods=['POST'])
def generate_reading():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    timestamp = int(time.time())
    output_filename = f"audio/output_{timestamp}.wav"

    if not os.path.exists("audio"):
        os.makedirs("audio")

    success = generate_audio(text, output_filename)
    if not success:
        return jsonify({"error": "Failed to generate audio"}), 500

    alignment_result = run_forced_alignment(output_filename, text)
    if alignment_result is None:
        words = text.split()
        alignment = [{"word": word, "start": idx * 0.5, "duration": 0.5} for idx, word in enumerate(words)]
    else:
        alignment = []
        for word in alignment_result.get("words", []):
            if word.get("case") == "success" and "start" in word and "end" in word:
                alignment.append({
                    "word": word["alignedWord"],
                    "start": word["start"],
                    "duration": word["end"] - word["start"]
                })

    audio_url = "http://127.0.0.1:5001/" + output_filename
    return jsonify({
        "audioUrl": audio_url,
        "alignment": alignment
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory("audio", filename)

@app.route('/')
def index():
    return "Welcome to the Immersive Reading API. Use /generate-reading to process text."

if __name__ == "__main__":
    if not os.path.exists("audio"):
        os.makedirs("audio")
    app.run(host="0.0.0.0", port=5001, debug=True)
