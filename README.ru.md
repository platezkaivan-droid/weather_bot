# 🌤️ Телеграм-бот погоды

Надёжный Telegram-бот для получения прогноза погоды с автоперезапуском, SQLite базой данных и интерактивной картой погоды (Web App).

## Возможности

- 🌡️ Актуальная погода для любого города мира
- 🏙️ Сохранение города по умолчанию для каждого пользователя
- 🔄 Автоперезапуск при сбоях (watchdog-процесс)
- 📊 Статистика использования
- 💾 Автоматическое резервное копирование БД
- 🛡️ Полная обработка ошибок + защита от rate-limit
- ⌨️ Меню команд Telegram с инлайн-клавиатурами
- 🕐 Точное местное время + восход/закат солнца
- 🗺️ Интерактивная карта погоды (Telegram Web App)

## Стек

| | |
|---|---|
| Язык | Python 3 |
| Фреймворк | python-telegram-bot |
| API погоды | [OpenWeatherMap](https://openweathermap.org/api) |
| База данных | SQLite |
| Деплой | [Render](https://render.com) (webhook-режим) |
| Контейнер | Docker |

## Быстрый старт

```bash
git clone https://github.com/platezkaivan-droid/weather_bot.git
cd weather_bot
cp .env.example .env
pip install -r requirements.txt
python main.py
```

### Windows

```bat
install_menu.bat
start_bot.bat
```

### Linux / Mac

```bash
chmod +x *.sh && ./install_menu.sh && ./start_bot.sh
```

## Деплой на Render

1. Сделай форк репозитория.
2. Создай **Web Service** на [render.com](https://render.com) и подключи форк.
3. Переменные окружения:

| Переменная | Значение |
|---|---|
| `BOT_TOKEN` | Токен от [@BotFather](https://t.me/BotFather) |
| `WEATHER_API_KEY` | Ключ [OpenWeatherMap](https://openweathermap.org/api) |
| `USE_WEBHOOK` | `true` |
| `WEBHOOK_URL` | `https://your-app-name.onrender.com` |

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Запустить бота |
| `/weather` | Текущая погода |
| `/forecast` | Прогноз на 5 дней |
| `/map` | Карта погоды (Web App) |
| `/setcity` | Установить город по умолчанию |
| `/stats` | Статистика |
| `/help` | Справка |

## Структура проекта

```
weather_bot/
├── main.py           # Точка входа + webhook
├── bot.py            # Логика бота
├── database.py       # SQLite
├── config.py         # Конфигурация
├── keyboards.py      # Клавиатуры
├── run_bot.py        # Watchdog
├── weather_map.html  # Карта (Web App)
├── Dockerfile
└── requirements.txt
```

## Лицензия

MIT
