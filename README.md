# 🌤️ Weather Telegram Bot

A reliable Telegram weather bot with auto-restart watchdog, SQLite database, and an interactive weather map Web App.

## Features

- 🌡️ Current weather for any city worldwide
- 🏙️ Save a default city per user
- 🔄 Auto-restart on crash (watchdog process)
- 📊 Usage statistics
- 💾 Automatic database backup
- 🛡️ Full error handling + rate-limit protection
- ⌨️ Telegram command menu with inline keyboards
- 🕐 Accurate local time + sunrise/sunset times
- 🗺️ Interactive weather map (Telegram Web App)

## Stack

| | |
|---|---|
| Language | Python 3 |
| Bot framework | python-telegram-bot |
| Weather API | [OpenWeatherMap](https://openweathermap.org/api) |
| Database | SQLite |
| Deploy | [Render](https://render.com) (webhook mode) |
| Container | Docker |

## Quick Start

```bash
git clone https://github.com/platezkaivan-droid/weather_bot.git
cd weather_bot
cp .env.example .env        # fill in BOT_TOKEN and WEATHER_API_KEY
pip install -r requirements.txt
python main.py
```

### Windows

```bat
install_menu.bat   # set up Telegram command menu (once)
start_bot.bat      # start the bot
```

### Linux / Mac

```bash
chmod +x *.sh && ./install_menu.sh && ./start_bot.sh
```

## Deploy to Render

1. Fork this repo.
2. Create a **Web Service** on [render.com](https://render.com) and connect the fork.
3. Set environment variables:

| Variable | Value |
|---|---|
| `BOT_TOKEN` | Your bot token from [@BotFather](https://t.me/BotFather) |
| `WEATHER_API_KEY` | Your [OpenWeatherMap](https://openweathermap.org/api) key |
| `USE_WEBHOOK` | `true` |
| `WEBHOOK_URL` | `https://your-app-name.onrender.com` |

4. Build: `pip install -r requirements.txt` / Start: `python main.py`

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Launch the bot |
| `/weather` | Current weather for your city |
| `/forecast` | 5-day forecast |
| `/map` | Interactive weather map (Web App) |
| `/setcity` | Set your default city |
| `/stats` | Usage statistics |
| `/help` | Help and examples |

## Project Structure

```
weather_bot/
├── main.py           # Entry point + webhook server
├── bot.py            # Bot logic and handlers
├── database.py       # SQLite operations
├── config.py         # Configuration
├── keyboards.py      # Inline keyboards
├── run_bot.py        # Auto-restart watchdog
├── weather_map.html  # Interactive Web App map
├── render.yaml       # Render deploy config
├── Dockerfile
└── requirements.txt
```

## Health Endpoints

`/health`, `/healthz`, `/ready`, `/alive` — for uptime monitoring on Render.

## Troubleshooting

| Problem | Fix |
|---|---|
| Bot doesn't start | Check `BOT_TOKEN` in `.env` |
| No weather data | Check `WEATHER_API_KEY` |
| DB errors on setcity | Run `fix_db.bat` / `./fix_db.sh` |
| Command menu missing | Run `python setup_commands.py` |

## License

MIT
