from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(**name**)
CORS(app)

@app.route("/")
def home():
return "TubeScout Backend Online"

@app.route("/extract", methods=["POST"])
def extract():

```
data = request.get_json()

if not data:
    return jsonify({"error": "No data supplied"}), 400

url = data.get("url")

if not url:
    return jsonify({"error": "No URL supplied"}), 400

try:

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "no_warnings": True,
        "user_agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

        if info.get("entries"):

            for entry in info["entries"]:

                if not entry:
                    continue

                video_url = entry.get("url")

                if video_url:

                    if not video_url.startswith("http"):
                        video_url = (
                            "https://www.youtube.com/watch?v="
                            + video_url
                        )

                    urls.append(video_url)

        else:

            urls.append(url)

    return jsonify({
        "success": True,
        "count": len(urls),
        "urls": urls
    })

except Exception as e:

    return jsonify({
        "success": False,
        "error": str(e)
    }), 500
```

if **name** == "**main**":
app.run(debug=True)
