import os
import io
import json
from flask import Flask, request, render_template, jsonify
from parser import parse_statement
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "statement" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    f = request.files["statement"]
    filename = f.filename or "uploaded"
    content = f.read()
    try:
        transactions = parse_statement(content, filename=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Basic response: parsed transactions
    return jsonify({"transactions": transactions})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
