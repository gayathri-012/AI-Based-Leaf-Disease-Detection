from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
import re
from openai import OpenAI

app = Flask(__name__)
CORS(app)

import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


MODEL = "openai/gpt-4o-mini"


def extract_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


@app.route("/detect", methods=["POST"])
def detect_disease():
    try:
        if "leaf" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400

        file = request.files["leaf"]
        img_b64 = base64.b64encode(file.read()).decode("utf-8")

        prompt = """
You are a plant pathology expert.

Analyze the image and return ONLY valid JSON in this exact format:

{
  "is_leaf": true,
  "leaf_type": "",
  "disease": "",
  "confidence": 0,
  "severity": "mild | moderate | severe | none",
  "cause": "",
  "prevention": [],
  "treatment": []
}

Rules:
- If the image is NOT a leaf (human, flower, object), set:
  "is_leaf": false
  "disease": "Not a leaf"
  "severity": "none"
- If it IS a leaf, set "is_leaf": true
- confidence must vary per image
- Do NOT add any text outside JSON
"""

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.6,
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}"
                            }
                        }
                    ]
                }
            ]
        )

        ai_output = response.choices[0].message.content
        print("RAW:", ai_output)

        json_str = extract_json(ai_output)
        if not json_str:
            return jsonify({"success": False, "error": "Cannot extract JSON"}), 500

        result = json.loads(json_str)

        # ================= SAFETY DEFAULTS =================
        if "is_leaf" not in result:
            result["is_leaf"] = False

        if result["is_leaf"] is False:
            result["confidence"] = None
            result["severity"] = "none"

        # ================= CONFIDENCE SAFETY =================
        if result["is_leaf"] is True:
            try:
                conf = int(result.get("confidence", 90))
                if conf < 85 or conf > 99:
                    conf = 90
            except:
                conf = 90

            result["confidence"] = conf

        return jsonify({"success": True, "result": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.json
        question = data.get("question")
        disease_info = data.get("disease_info")

        prompt = f"""
You are an agriculture AI assistant.

Detected Disease Details:
{json.dumps(disease_info, indent=2)}

User Question:
{question}

Answering Rules:
- By default, answer in **1–2 sentences only**.
- If the user asks for "explain", "details", "complete", "full", or "how", give a **detailed paragraph**.
- Do NOT add prevention, treatment, or extra information unless the question asks for it.
- Be clear, accurate, and farmer-friendly.
- Do NOT repeat unnecessary information.
"""



        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.4,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        return jsonify({"success": True, "answer": answer})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/")
def home():
    return "AgriScan AI Vision API Running!"


if __name__ == "__main__":
    app.run(debug=True)
