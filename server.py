from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():

    return jsonify({
        "status": "Server Running"
    })

@app.route("/api/info")
def get_info():

    url = request.args.get("url")

    if not url:

        return jsonify({
            "success": False,
            "message": "URL Required"
        })

    ydl_opts = {
        'quiet': True,
        'noplaylist': True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        medias = []

        for f in info.get("formats", []):

            media_url = f.get("url")

            if media_url:

                medias.append({
                    "quality": str(
                        f.get("height", "")
                    ),
                    "ext": f.get("ext", ""),
                    "url": media_url
                })

        return jsonify({
            "success": True,
            "title": info.get("title", ""),
            "thumbnail": info.get(
                "thumbnail", ""
            ),
            "medias": medias
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )