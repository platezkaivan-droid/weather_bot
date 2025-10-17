#!/usr/bin/env python3
"""
Скрипт для тестирования webhook режима локально
"""

import asyncio
import os
import sys
from aiohttp import web
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_webhook_server():
    """Запускает тестовый webhook сервер"""
    
    # Устанавливаем тестовые переменные окружения
    os.environ['USE_WEBHOOK'] = 'true'
    os.environ['WEBHOOK_URL'] = 'http://localhost:8000'
    os.environ['PORT'] = '8000'
    
    # Проверяем наличие токенов
    if not os.getenv('BOT_TOKEN'):
        print("❌ Установите переменную окружения BOT_TOKEN")
        sys.exit(1)
        
    if not os.getenv('WEATHER_API_KEY'):
        print("❌ Установите переменную окружения WEATHER_API_KEY")
        sys.exit(1)
    
    print("🧪 Запуск тестового webhook сервера...")
    print("🌐 URL: http://localhost:8000")
    print("📡 Health check: http://localhost:8000/healthz")
    print("🛑 Для остановки нажмите Ctrl+C")
    print()
    
    try:
        # Импортируем и запускаем main
        from main import main
        await main()
        
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
    except Exception as e:
        print(f"\n💥 Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_webhook_server())