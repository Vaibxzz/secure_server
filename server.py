from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage (can be replaced with database or file)
messages = {}

@app.route('/')
def home():
    return '🔒 Secure Relay Server is running.'

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    recipient = data.get('to')
    sender = data.get('from')
    encrypted_aes_key = data.get('aes_key')  # base64 string
    encrypted_message = data.get('message')  # base64 string

    if not all([recipient, sender, encrypted_message, encrypted_aes_key]):
        return jsonify({'error': 'Missing data'}), 400

    if recipient not in messages:
        messages[recipient] = []

    messages[recipient].append({
        'from': sender,
        'aes_key': encrypted_aes_key,
        'message': encrypted_message,
        'id': str(uuid.uuid4())
    })

    return jsonify({'status': 'Message stored securely.'})

@app.route('/receive/<user_id>', methods=['GET'])
def receive(user_id):
    user_messages = messages.pop(user_id, [])
    return jsonify(user_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
