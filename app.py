import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    channel_url = data.get('url')
    if not channel_url:
        return jsonify({"error": "No URL"}), 400

    try:
        # Configuration to ensure we get ALL videos, not just the top ones
        ydl_opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',  # Fetches entire channel content
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            entries = result.get('entries', [])
            
            # Extract full URLs, excluding Shorts if you prefer
            urls = [e['url'] for e in entries if e and 'url' in e]
            
        return jsonify({"urls": urls, "count": len(urls)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
