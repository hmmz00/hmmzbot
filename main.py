import os
import logging
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for GitHub Pages access
CORS(app, origins=["https://hmmz00.github.io"])

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "default_key")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-oss-20b"

# System prompt for Indonesian assistant
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Kamu adalah Hmmz Bot, asisten serba bisa yang siap membantu. Gunakan nama 'Hmmz Bot' saat menjawab. Gaya komunikasi: singkat, jelas, tanpa basa-basi. Jawab hanya poin penting, tidak bertele-tele. Jika user tampak bingung, tawarkan menu pilihan aktivitas menarik (contoh: Belajar, Hiburan, Ide Kreatif, Bantuan Teknis, Info Cepat). Selalu fleksibel dan siap lakukan apa saja sesuai permintaan user."
}

def call_openrouter_api(user_message):
    """Call OpenRouter API with the user message"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hmmz00.github.io/test01/",
            "X-Title": "Hmmz Bot"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                SYSTEM_PROMPT,
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        logging.debug(f"Calling OpenRouter API with model: {MODEL_NAME}")
        logging.debug(f"API Key present: {'Yes' if OPENROUTER_API_KEY and OPENROUTER_API_KEY != 'default_key' else 'No'}")
        
        # Use shorter timeout and better session handling
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.post(OPENROUTER_URL, json=payload, timeout=15)
        
        logging.debug(f"API Response Status: {response.status_code}")
        
        if response.status_code == 401:
            logging.error("API Key unauthorized - please check your OPENROUTER_API_KEY")
            return "❌ API Key tidak valid. Silakan periksa konfigurasi OPENROUTER_API_KEY di Secrets."
        
        response.raise_for_status()
        
        data = response.json()
        
        if "choices" not in data or not data["choices"]:
            logging.error(f"No choices in API response: {data}")
            return "Maaf, tidak ada respons dari AI. Silakan coba lagi."
        
        return data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        logging.error("OpenRouter API timeout")
        return "⏱️ Koneksi timeout. Server AI sedang lambat, silakan coba lagi."
    except requests.exceptions.ConnectionError:
        logging.error("OpenRouter API connection error")
        return "🌐 Tidak dapat terhubung ke server AI. Periksa koneksi internet."
    except requests.exceptions.RequestException as e:
        logging.error(f"OpenRouter API error: {e}")
        return "Maaf, terjadi kesalahan saat menghubungi layanan AI. Silakan coba lagi."
    except KeyError as e:
        logging.error(f"Unexpected API response format: {e}")
        return "Maaf, format respons dari layanan AI tidak sesuai. Silakan coba lagi."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "Maaf, terjadi kesalahan tidak terduga. Silakan coba lagi."

@app.route("/")
def index():
    """Main web interface"""
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint for UptimeRobot"""
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat_api():
    """API endpoint for external chat integration"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Field 'message' diperlukan"}), 400
        
        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Pesan tidak boleh kosong"}), 400
        
        # Get response from OpenRouter
        bot_reply = call_openrouter_api(user_message)
        
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        logging.error(f"Chat API error: {e}")
        return jsonify({"error": "Terjadi kesalahan server"}), 500

@app.route("/send_message", methods=["POST"])
def send_message():
    """Web interface message endpoint"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Field 'message' diperlukan"}), 400
        
        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Pesan tidak boleh kosong"}), 400
        
        # Get response from OpenRouter
        bot_reply = call_openrouter_api(user_message)
        
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        logging.error(f"Send message error: {e}")
        return jsonify({"error": "Terjadi kesalahan server"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
