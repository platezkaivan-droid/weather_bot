# 🌍 Создание репозитория для Web App

## Шаги для размещения Web App на GitHub Pages:

### 1. Создайте новый репозиторий на GitHub
- Название: `weather-bot-webapp`
- Описание: `Web App для интерактивной карты погоды Telegram бота`
- Публичный репозиторий
- Добавьте README.md

### 2. Клонируйте репозиторий локально
```bash
git clone https://github.com/platezkaivan-droid/weather-bot-webapp.git
cd weather-bot-webapp
```

### 3. Скопируйте файл Web App
```bash
# Скопируйте weather_map.html в корень нового репозитория
cp ../weatherbot/weather_map.html ./
```

### 4. Создайте README для Web App
```bash
# Создайте README.md с описанием
```

### 5. Загрузите на GitHub
```bash
git add .
git commit -m "🌍 Initial commit: Weather Bot Web App"
git push origin main
```

### 6. Включите GitHub Pages
1. Перейдите в Settings репозитория
2. Найдите раздел "Pages"
3. Выберите Source: "Deploy from a branch"
4. Выберите Branch: "main" и папку "/ (root)"
5. Нажмите Save

### 7. Обновите URL в боте
После активации GitHub Pages, обновите URL в `keyboards.py`:
```python
web_app_url = "https://platezkaivan-droid.github.io/weather-bot-webapp/weather_map.html"
```

## 🚀 Готово!
Web App будет доступен по адресу:
`https://platezkaivan-droid.github.io/weather-bot-webapp/weather_map.html`