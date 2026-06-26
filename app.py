python
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import extract_urls
import csv
import os

app = Flask(__name__)

# Allow requests from your frontend
CORS(app)


@app.route("/")
def home():
    return "TubeScout Backend Running"


@app.route("/extract", methods=["POST"])
def extract():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        url = data.get("url")

        if not url:
            return jsonify({
                "error": "URL is required"
            }), 400

        urls = extract_urls(url)

        return jsonify({
            "count": len(urls),
            "urls": urls
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/waitlist", methods=["POST"])
def waitlist():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        email = data.get("email", "").strip()

        if email == "":
            return jsonify({
                "error": "Email is required"
            }), 400

        file_exists = os.path.isfile("waitlist.csv")

        with open("waitlist.csv", "a", newline="") as csvfile:

            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(["Email"])

            writer.writerow([email])

        return jsonify({
            "success": True
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
