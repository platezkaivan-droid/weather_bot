# 🌤️ Weather Bot - Деплой на Render

Полная инструкция по деплою телеграм-бота на Render Web Service.

## 📋 Что нужно подготовить

1. **Токен бота** - получите у [@BotFather](https://t.me/BotFather)
2. **API ключ погоды** - зарегистрируйтесь на [OpenWeatherMap](https://openweathermap.org/api)
3. **Аккаунт GitHub** - для хранения кода
4. **Аккаунт Render** - для хостинга (бесплатный план доступен)

## 🚀 Пошаговый деплой

### Шаг 1: Подготовка репозитория

1. **Создайте новый репозиторий** на GitHub:
   - Зайдите на github.com
   - Нажмите "New repository"
   - Назовите его "weather-bot"
   - Сделайте публичным
   - Нажмите "Create repository"

2. **Загрузите файлы**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Weather Bot for Render"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/weather-bot.git
   git push -u origin main
   ```

3. **Проверьте загрузку**:
   ```bash
   # Быстрая проверка готовности к деплою
   python deploy.py
   ```

### Шаг 2: Создание сервиса на Render

1. Зайдите на [render.com](https://render.com) и войдите через GitHub
2. Нажмите **"New"** → **"Web Service"**
3. Выберите ваш репозиторий
4. Настройте сервис:
   - **Name**: `weather-bot-yourname`
   - **Root Directory**: `weatherbot`
   - **Environment**: `Python 3`
   - **Python Version**: `3.11.0`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### Шаг 3: Настройка переменных окружения

В разделе **Environment Variables** добавьте:

```
BOT_TOKEN=1234567890:AAAA-your-bot-token-here
WEATHER_API_KEY=your-openweathermap-api-key-here
USE_WEBHOOK=true
WEBHOOK_URL=https://your-app-name.onrender.com
PORT=10000
```

### Шаг 4: Деплой

1. Нажмите **"Create Web Service"**
2. Дождитесь завершения деплоя (5-10 минут)
3. Проверьте логи на наличие ошибок

### Шаг 5: Проверка работы

1. Откройте `https://your-app-name.onrender.com/health`
2. Должен вернуться JSON: `{"status": "ok", "bot": "weather_bot"}`
3. Напишите боту в Telegram - он должен ответить

## 🔧 Устранение проблем

### Бот не отвечает
- Проверьте логи в Render Dashboard
- Убедитесь, что все переменные окружения установлены
- Проверьте правильность токенов

### Ошибки деплоя
- Проверьте `requirements.txt`
- Убедитесь, что `main.py` находится в корне проекта
- Проверьте Python версию (должна быть 3.11)

### Webhook не работает
- Убедитесь, что `WEBHOOK_URL` правильный
- Проверьте, что сервис запущен и доступен
- Webhook URL должен быть HTTPS

## 📊 Мониторинг

- **Логи**: Render Dashboard → Logs
- **Метрики**: Render Dashboard → Metrics  
- **Health Check**: `https://your-app.onrender.com/health`
- **Статистика бота**: команда `/stats` в Telegram

## 🔄 Обновления

После настройки каждый `git push` в main ветку автоматически обновит бота на Render.

```bash
git add .
git commit -m "Update bot"
git push origin main
```

## 💰 Стоимость

- **Render Free Plan**: 750 часов в месяц бесплатно
- **Render Paid Plan**: $7/месяц за безлимитное время работы

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте логи в Render Dashboard
2. Убедитесь в правильности всех настроек
3. Создайте Issue в GitHub репозитории