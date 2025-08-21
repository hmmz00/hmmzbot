#!/usr/bin/env python3
"""
Ping script untuk menjaga server tetap hidup.
Script ini akan melakukan ping ke endpoint /ping setiap 5 menit.
Bisa dijalankan di UptimeRobot atau sebagai cron job.
"""

import time
import requests
import sys
from datetime import datetime

# URL server yang akan di-ping
SERVER_URL = "https://your-replit-url.replit.app/ping"

def ping_server():
    """Ping server endpoint dan cek response"""
    try:
        response = requests.get(SERVER_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print(f"[{datetime.now()}] ✓ Server online - Status: {data['status']}")
                return True
            else:
                print(f"[{datetime.now()}] ⚠️ Server response tidak sesuai: {data}")
                return False
        else:
            print(f"[{datetime.now()}] ❌ Server error - Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] ❌ Ping error: {e}")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Unexpected error: {e}")
        return False

def main():
    """Main loop untuk ping setiap 5 menit"""
    print(f"[{datetime.now()}] 🚀 Memulai ping monitor untuk {SERVER_URL}")
    print("Ping akan dilakukan setiap 5 menit...")
    print("Tekan Ctrl+C untuk berhenti")
    
    try:
        while True:
            success = ping_server()
            if not success:
                print("Server tidak merespons dengan benar!")
            
            # Tunggu 5 menit (300 detik)
            time.sleep(300)
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] 🛑 Ping monitor dihentikan")
        sys.exit(0)
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Untuk testing sekali
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing ping sekali...")
        ping_server()
    else:
        main()