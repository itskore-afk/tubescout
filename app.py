from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "TubeScout Backend is online and ready for requests!"

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    
    print(f"DEBUG: Received URL: {url}")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Using yt-dlp to get video information
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # Extracting specific data points
        result = {
            "title": info.get('title'),
            "thumbnail": info.get('thumbnail'),
            "duration": info.get('duration'),
            "uploader": info.get('uploader')
        }
        
        print("DEBUG: Extraction successful")
        return jsonify(result)
    
    except Exception as e:
        print(f"DEBUG: Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
