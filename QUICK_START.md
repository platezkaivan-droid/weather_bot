# ⚡ Быстрый старт Weather Bot

## 🎯 За 5 минут до деплоя на Render

### 1️⃣ Подготовка токенов (2 минуты)

**Токен бота:**
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен (выглядит как `1234567890:AAAA...`)

**API ключ погоды:**
1. Зайдите на [OpenWeatherMap](https://openweathermap.org/api)
2. Зарегистрируйтесь (бесплатно)
3. Перейдите в API Keys
4. Скопируйте ключ

### 2️⃣ Загрузка на GitHub (1 минута)

```bash
# Создайте репозиторий на github.com, затем:
git init
git add .
git commit -m "Weather Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/weather-bot.git
git push -u origin main
```

### 3️⃣ Деплой на Render (2 минуты)

1. **Зайдите на [render.com](https://render.com)**
2. **Войдите через GitHub**
3. **Нажмите "New" → "Web Service"**
4. **Выберите ваш репозиторий**
5. **Настройте:**
   - Name: `weather-bot-yourname`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

6. **Добавьте переменные окружения:**
   ```
   BOT_TOKEN=ваш_токен_бота
   WEATHER_API_KEY=ваш_ключ_погоды
   USE_WEBHOOK=true
   WEBHOOK_URL=https://weather-bot-yourname.onrender.com
   ```

7. **Нажмите "Create Web Service"**

### 4️⃣ Проверка (30 секунд)

После деплоя:
1. Откройте `https://your-app.onrender.com/healthz`
2. Должен показать: `{"status": "healthy"}`
3. Напишите боту в Telegram - он должен ответить!

## 🆘 Если что-то не работает

### Бот не отвечает:
```bash
# Проверьте логи в Render Dashboard
# Убедитесь, что все переменные окружения установлены
```

### 404 ошибка на /healthz:
```bash
# Проверьте, что используется файл main.py, а не bot.py
# Start Command должен быть: python main.py
```

### Webhook ошибки:
```bash
# Убедитесь, что WEBHOOK_URL правильный
# URL должен быть HTTPS
# Проверьте логи на наличие ошибок установки webhook
```

## 🎉 Готово!

Ваш бот теперь работает 24/7 на Render!

**Полезные ссылки:**
- Health check: `https://your-app.onrender.com/healthz`
- Логи: Render Dashboard → Logs
- Статистика бота: команда `/stats` в Telegram

**Автоматические обновления:**
Каждый `git push` автоматически обновит бота на Render.