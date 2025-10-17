#!/usr/bin/env python3
"""
Простой HTTP сервер для размещения Web App карты погоды
Используется для локального тестирования
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Порт для сервера
PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для работы с Telegram Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # Переходим в директорию с HTML файлом
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    print(f"🌐 Запуск Web App сервера...")
    print(f"📁 Директория: {web_dir}")
    print(f"🔗 URL: http://localhost:{PORT}/weather_map.html")
    print(f"🛑 Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Сервер запущен на порту {PORT}")
            print(f"🌍 Откройте в браузере: http://localhost:{PORT}/weather_map.html")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Порт {PORT} уже используется")
            print(f"💡 Попробуйте другой порт или остановите процесс на порту {PORT}")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()