import os
from pathlib import Path

# Загружаем .env файл если он существует
try:
    from dotenv import load_dotenv
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ .env файл загружен")
except ImportError:
    # dotenv не установлен, используем только системные переменные
    pass

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Проверяем обязательные переменные
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не установлен! Добавьте его в переменные окружения или .env файл")

if not WEATHER_API_KEY:
    raise ValueError("❌ WEATHER_API_KEY не установлен! Добавьте его в переменные окружения или .env файл")

# Настройки для деплоя
PORT = int(os.getenv('PORT', 10000))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN.split(":")[0]}'  # Используем только ID бота

# Режим работы (webhook для продакшена, polling для разработки)
USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'

# Дополнительные настройки
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()