import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful assistant."}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify(error="No messages provided"), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # change to any model you have access to
            messages=[SYSTEM_PROMPT] + messages,
        )
        reply = response.choices[0].message.content
        return jsonify(reply=reply)
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
