from flask import Flask, render_template, request, jsonify
import speech_transcriber as transcribe
from vertex_ai_component import notify
from google.cloud import storage
import urllib.parse
import os 

app = Flask(__name__)
PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
GCS_URI = f"gs://{BUCKET_NAME}/"

storage_client = storage.Client()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']

        if uploaded_file:
            bucket = storage_client.get_bucket(BUCKET_NAME)
            blob = bucket.blob(uploaded_file.filename)
            blob.upload_from_string(
                uploaded_file.read(),
                content_type=uploaded_file.content_type
            )
            return jsonify({'message': 'File uploaded successfully'}), 200
    except:
        return jsonify({'error': 'Error uploading the File'}), 400

@app.route("/viewfiles", methods = ["GET"])
def view_uploaded_files():
    try:
        uploaded_files = [blob.name for blob in storage_client.list_blobs(BUCKET_NAME)]
        return jsonify({"files": uploaded_files})
    except:
        return jsonify({"files": []})

@app.route("/process", methods = ["GET"])
def process_notify():
    file_name = request.args.get('filename')
    decoded_file_name = urllib.parse.unquote(file_name)
    file_destination = GCS_URI + decoded_file_name
    print(f"Received File Destination: {file_destination}")

    transcibe_response = transcribe.transcribe_file_with_auto_punctuation(file_destination)
    
    transcribe_response_text = str()
    for result in transcibe_response.results:
        alternative = result.alternatives[0]
        transcribe_response_text += " " + alternative.transcript
    print(f"Transcribed Text: {transcribe_response_text}")

    notify_response = notify(transcribe_response_text, PROJECT_ID)
    print(f"Notify Response: {notify_response}")

    return jsonify({"content": notify_response})

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')


