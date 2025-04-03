from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    print("=== RICHIESTA /search RICEVUTA ===")

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query = data['query']
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'format': 'bestaudio/best',
        'default_search': 'ytsearch5',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if 'entries' not in results:
        return jsonify({"error": "No results found"}), 404

    entries = results['entries']
    response = []
    for entry in entries:
        if entry is None:
            continue
        video_info = {
            "title": entry.get("title", "No title"),
            "url": entry.get("webpage_url", "No URL")
        }
        response.append(video_info)

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
