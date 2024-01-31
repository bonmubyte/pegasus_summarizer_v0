from flask import Flask, request, jsonify, send_from_directory
import os
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

app = Flask(__name__)

# Path to the frontend folder, assuming the backend folder is at the same level as the frontend folder
FRONTEND_FOLDER = os.path.abspath("../frontend")

@app.route('/')
def index():
    # Serve the index.html file from the frontend directory
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # Serve all other files (css, js, images, etc.) from the frontend directory
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route('/summarize', methods=['POST'])
def summarize():
    # Your summarization logic here
    data = request.get_json()
    text = data['text']

    # Load the model and tokenizer each time this function is called
    # For better performance, consider loading them outside of this function
    # so they're only loaded once when the app starts
    tokenizer = PegasusTokenizer.from_pretrained('tuner007/pegasus_summarizer')
    model = PegasusForConditionalGeneration.from_pretrained('tuner007/pegasus_summarizer')

    tokens = tokenizer(text, truncation=True, padding='longest', return_tensors='pt')
    summary_ids = model.generate(tokens['input_ids'], num_beams=4, max_length=60, min_length=20, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
