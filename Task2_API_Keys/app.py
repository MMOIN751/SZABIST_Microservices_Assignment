from flask import Flask, jsonify, request
import hmac
import os

app = Flask(__name__)

def configured_keys():
    # Set API_KEYS to a comma-separated list of three or more generated secrets.
    return [key.strip() for key in os.environ.get("API_KEYS", "").split(",") if key.strip()]

@app.post("/process")
def process_text():
    keys = configured_keys()
    if len(keys) < 3:
        return jsonify({"error": "Server is not configured: set at least three API keys"}), 503

    supplied = request.headers.get("X-API-Key", "")
    if not supplied or not any(hmac.compare_digest(supplied, key) for key in keys):
        return jsonify({"error": "Invalid or missing API key"}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "A non-empty text string is required"}), 400

    return jsonify({"original_text": text, "processed_text": text.upper()})

@app.get("/")
def home():
    return jsonify({"message": "Text Processing API", "endpoint": "POST /process"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=False)
