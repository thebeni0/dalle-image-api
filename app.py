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

    # Validate and clean prompt
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt.strip()) < 5:
        print("INVALID PROMPT:", prompt)
        return jsonify({"error": "Invalid prompt"}), 400

    prompt = prompt.strip()[:100]  # Truncate to avoid long prompt issues
    cartoon_prompt = (
        "cartoon-style illustration for kids"
        f"Scene: {prompt}"
    )



    try:
        print("FINAL PROMPT:", cartoon_prompt)
        response = openai.images.generate(
            model="dall-e-3",
            prompt=cartoon_prompt,
            size="1024x1024",
            n=1
        )
        print("RAW OPENAI RESPONSE:", response)

        image_url = response.data[0].url
        return jsonify({"image_url": image_url})

    except openai.OpenAIError as e:
        print("OPENAI API ERROR:", e)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("UNEXPECTED ERROR:", e)
        return jsonify({"error": str(e)}), 500


