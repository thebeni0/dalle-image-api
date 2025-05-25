# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        print("RAW OPENAI RESPONSE:", response)

        image_url = response["data"][0]["url"]
        return jsonify({"image_url": image_url})

    except Exception as e:
        print("IMAGE GENERATION ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
