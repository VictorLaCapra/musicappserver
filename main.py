from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# Endpoint di test per verificare se il server è online
@app.route('/', methods=['GET'])
def home():
    return "Server Online", 200

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        print(f"✅ Ricevuto JSON: {data}")

        if not data or 'query' not in data:
            print("❌ Richiesta errata, manca 'query'.")
            return jsonify({"error": "Invalid request"}), 400

        query = data['query']
        print(f"🔍 Query ricevuta: {query}")

        results = []
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                search_results = ydl.extract_info(f"ytsearch10:{query}", download=False)['entries']
                for result in search_results:
                    results.append({
                        "title": result.get("title"),
                        "url": result.get("webpage_url")
                    })
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
            return jsonify({"error": "Errore durante la ricerca"}), 500

        if not results:
            print("❌ Nessun risultato trovato.")
            return jsonify({"error": "No results found"}), 404

        print(f"✅ Risultati trovati: {results}")
        return jsonify(results), 200

    except Exception as e:
        print(f"🔥 Errore Generale: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
