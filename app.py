from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yt_dlp # Ensure yt-dlp is in your requirements.txt

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    channel_url = data.get('url')
    
    ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        urls = [video['url'] for video in result.get('entries', [])]
        
    return jsonify({"urls": urls})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
