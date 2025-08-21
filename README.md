# Chatbot Asisten Indonesia

Aplikasi web chatbot sederhana dengan Flask backend dan integrasi OpenRouter API menggunakan model "openai/gpt-oss-20b".

## Fitur

- 🤖 Chatbot dengan kepribadian asisten Indonesia yang responsif
- 🌐 Web interface yang user-friendly dengan Bootstrap dark theme
- 🔌 API endpoint untuk integrasi eksternal
- 📊 Health check endpoint untuk monitoring UptimeRobot
- 🌍 CORS support untuk akses dari GitHub Pages
- 📱 Responsive design untuk mobile dan desktop

## Setup dan Instalasi

### 1. Konfigurasi API Key

Anda perlu menyimpan API Key OpenRouter sebagai environment variable:

**Di Replit:**
1. Buka sidebar "Secrets" (ikon kunci)
2. Tambahkan secret baru:
   - Key: `OPENROUTER_API_KEY`
   - Value: API key OpenRouter Anda

**Di environment lokal:**
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

### 2. Menjalankan Aplikasi

```bash
# Install dependencies
uv add requests flask-cors

# Jalankan server
python main.py
```

Server akan berjalan di `http://localhost:5000`

### 3. Setup UptimeRobot untuk Keep-Alive

Untuk menjaga aplikasi tetap hidup 24/7, setup monitoring di UptimeRobot:

1. Buka https://uptimerobot.com
2. Buat akun baru atau login
3. Klik "Add New Monitor"
4. Pilih "HTTP(s)" monitor type
5. Isi konfigurasi:
   - Monitor Type: HTTP(s)
   - Friendly Name: "Hmmz Bot Keep Alive"
   - URL: `https://your-replit-url.replit.app/ping`
   - Monitoring Interval: 5 minutes
6. Klik "Create Monitor"

Alternatively, jalankan script ping.py secara lokal:
```bash
# Test ping sekali
python ping.py --test

# Jalankan ping monitor terus-menerus
python ping.py
