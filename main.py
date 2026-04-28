from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PERSONA = os.environ.get("PERSONA")

chat_history = []

@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history
    data = request.get_json()
    user_msg = data.get("message", "")

    chat_history.append({"role": "user", "content": user_msg})
    if len(chat_history) > 12:
        chat_history = chat_history[-12:]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "system", "content": PERSONA}] + chat_history,
        "temperature": 0.7
    }

    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "网络或API出错了，等会再试试~"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
