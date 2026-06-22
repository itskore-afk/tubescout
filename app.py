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
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            
            # This safely handles the data structure to prevent the KeyError
            urls = []
            for entry in result.get('entries', []):
                link = entry.get('url') or entry.get('webpage_url')
                if link:
                    urls.append(link)
                    
            return jsonify({"urls": urls})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
