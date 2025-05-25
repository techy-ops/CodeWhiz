from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/analyze_code', methods=['POST'])
def analyze_code():
    data = request.get_json()
    code = data.get('code')
    task = data.get('task')

    prompt = ""
    if task == "explain":
        prompt = f"Explain what this code does:\n{code}"
    elif task == "debug":
        prompt = f"Find and fix bugs in this code:\n{code}"
    elif task == "write":
        prompt = f"Write code for the following task:\n{code}"
    else:
        return jsonify({"error": "Invalid task"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
