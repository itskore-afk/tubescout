from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import extract_youtube_data

app = Flask(__name__)
# This allows your frontend HTML file to talk to this backend server securely
CORS(app)

@app.route('/extract', modalities=['POST'])
@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    youtube_url = data['url']
    try:
        result = extract_youtube_data(youtube_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'TubeScout Backend Engine is Running Live!'})

if __name__ == '__main__':
    import os
    # Render assigns a dynamic port using an environment variable. Defaults to 10000 locally.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
