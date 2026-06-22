from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # This allows your GitHub page to talk to your Render backend

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    channel_url = data.get('url')
    
    # Placeholder: Replace this with your actual scraping logic
    # We are returning a dummy list to test the connection
    dummy_urls = [
        "https://youtube.com/watch?v=example1",
        "https://youtube.com/watch?v=example2"
    ]
    
    return jsonify({"urls": dummy_urls})

if __name__ == '__main__':
    # Render assigns a port via environment variable
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
