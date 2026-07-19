import os
import json
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')

JSON_FILE = 'memories.json'

# Ensure the memories file exists on startup
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        # Initialize with preset default memories if empty
        initial_presets = [
            {"id": 1, "text": "All those moments will be lost in time, like tears in rain.", "clientId": "system"},
            {"id": 2, "text": "Technology accelerates time. Emotions slow it down, transmuting it.", "clientId": "system"},
            {"id": 3, "text": "Every ghost of a memory finds its sanctuary in the timeless void.", "clientId": "system"},
            {"id": 4, "text": "A vast room suspended in darkness, floating fragments of light.", "clientId": "system"}
        ]
        json.dump(initial_presets, f, indent=4)

@app.route('/')
def index():
    # Serves the frontend index.html file
    return send_from_directory('.', 'index.html')

@app.route('/api/memories', methods=['GET'])
def get_memories():
    with open(JSON_FILE, 'r') as f:
        memories = json.load(f)
    return jsonify(memories)

@app.route('/api/memories', methods=['POST'])
def add_memory():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text content'}), 400
    
    text = data['text']
    client_id = data.get('clientId', 'unknown')
    
    with open(JSON_FILE, 'r+') as f:
        memories = json.load(f)
        
        # Build the new memory payload
        new_memory = {
            'id': len(memories) + 1,
            'text': text,
            'clientId': client_id
        }
        
        memories.append(new_memory)
        
        # Rewind file pointer, write rewritten payload, and truncate remaining characters
        f.seek(0)
        json.dump(memories, f, indent=4)
        f.truncate()
        
    return jsonify(new_memory), 201

if __name__ == '__main__':
    # Runs the server locally on port 5000
    app.run(port=5000, debug=True)