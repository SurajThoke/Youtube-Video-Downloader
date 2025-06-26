from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app, origins=["https://nimble-snickerdoodle-c26f98.netlify.app"])
  # Allow frontend access from browser

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution", f"{f.get('height', '')}p"),
                    "url": f.get("url")
                }
                for f in info.get("formats", []) if f.get("url")
            ]

        return jsonify({
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

