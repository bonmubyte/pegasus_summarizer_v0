from flask import request, jsonify, send_from_directory, render_template, Response
from yourapp import app, db
from yourapp.models import TextRecord
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import os
from io import StringIO
import csv

'''
# Serve the index.html file from the frontend directory
@app.route('/')
def index():
    print("Serving index.html")
    FRONTEND_FOLDER = os.path.abspath("../../frontend")
    return send_from_directory(FRONTEND_FOLDER, 'index.html')
'''

'''
2nd version
@app.route('/')
def index():
    # Navigate up one directory from the 'yourapp' package to the 'backend' directory
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return send_from_directory(backend_dir, 'index.html')
'''

@app.route('/')
def index():
    return render_template('index.html')

# Serve static files (css, js, images, etc.)
@app.route('/<path:path>')
def static_proxy(path):
    FRONTEND_FOLDER = os.path.abspath("../../frontend")  # Adjust the path as necessary
    return send_from_directory(FRONTEND_FOLDER, path)

# Summarization route

@app.route('/summarize', methods=['POST'])
def summarize():
    # Extract the text to be summarized from the incoming JSON request
    data = request.get_json()
    text = data['text']

    # Initialize the tokenizer and model for Pegasus
    tokenizer = PegasusTokenizer.from_pretrained('tuner007/pegasus_summarizer')
    model = PegasusForConditionalGeneration.from_pretrained('tuner007/pegasus_summarizer')

    # Tokenize the input text and generate the summary
    tokens = tokenizer(text, truncation=True, padding='longest', return_tensors='pt')
    summary_ids = model.generate(tokens['input_ids'], num_beams=4, max_length=60, min_length=20, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Save the input text and its summary to the database
    record = TextRecord(input_text=text, output_text=summary)
    db.session.add(record)
    db.session.commit()

    # Return the summary in the response
    return jsonify({'summary': summary})

# Route to fetch all records
@app.route('/records')
def records():
    records = TextRecord.query.all()
    return render_template('records.html', records=records)

@app.route('/download-csv')
def download_csv():
    records = TextRecord.query.all()

    def generate_csv():
        data = StringIO()
        writer = csv.writer(data)

        # Write header
        writer.writerow(['Input Text', 'Output Text'])

        # Write records
        for record in records:
            writer.writerow([record.input_text, record.output_text])
            data.seek(0)
            yield data.read()
            data.seek(0)
            data.truncate(0)

    response = Response(generate_csv(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='records.csv')
    return response