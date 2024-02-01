from flask import request, jsonify
from yourapp import app, db
from yourapp.models import TextRecord
# Assuming you're using a dummy summarization for demonstration
# Replace this with actual summarization logic using your preferred model

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    input_text = data.get('input_text', '')

    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    # Dummy summarization logic; replace with actual model inference
    output_text = input_text[:50]  # Truncate text for demonstration

    text_record = TextRecord(input_text=input_text, output_text=output_text)
    db.session.add(text_record)
    db.session.commit()

    return jsonify({'input_text': input_text, 'output_text': output_text})

@app.route('/records', methods=['GET'])
def get_records():
    records = TextRecord.query.all()
    return jsonify([{'id': r.id, 'input': r.input_text, 'output': r.output_text} for r in records])
