from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/extract", methods=["POST"])
def extract():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400


    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                url,
                download=False
            )


        urls = []

        for video in info.get("entries", []):
            if video:
                urls.append(
                    "https://youtube.com/watch?v=" + video["id"]
                )


        return jsonify({
            "count": len(urls),
            "urls": urls
        })


    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
