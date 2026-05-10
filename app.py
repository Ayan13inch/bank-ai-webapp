from flask import Flask, request, render_template, jsonify, send_file
import parser as bp
import os, io, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['statement']
    content = f.read()
    # detect type and parse
    txns = bp.parse_statement(content, filename=f.filename)
    # optional: call LLM for categorization (replace with your key)
    # categories = categorize_with_llm(txns)
    return jsonify({"transactions": txns})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
