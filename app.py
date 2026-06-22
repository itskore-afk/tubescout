import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# CORS enabled to allow requests from any origin for your public tool
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        channel_url = data.get('url')
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            urls = [v['url'] for v in result.get('entries', [])]
        return jsonify({"urls": urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
