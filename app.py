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
        # These options mimic a real browser to bypass YouTube's bot detection
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            info = ydl.extract_info(url, download=False)
            
            # Handle different types of URLs (video vs channel/playlist)
            if 'entries' in info:
                # It's a channel or playlist
                videos = []
                for entry in info['entries']:
                    if entry:
                        videos.append({
                            "title": entry.get('title'),
                            "url": entry.get('webpage_url')
                        })
                result = {"type": "playlist", "videos": videos}
            else:
                # It's a single video
                result = {
                    "type": "video",
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "url": url
                }
        
        print("DEBUG: Extraction successful")
        return jsonify(result)
    
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG: Error occurred: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
