# app.py
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="512x512",
            n=1
        )
        print("RAW OPENAI RESPONSE:", response)  # 👈 Add this line

        # Depending on the SDK version, use one of the following:
        try:
            image_url = response.data[0].url
        except AttributeError:
            image_url = response['data'][0]['url']

        return jsonify({"image_url": image_url})

    except Exception as e:
        print("IMAGE GENERATION ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
