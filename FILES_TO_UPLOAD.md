# 📁 Файлы для загрузки на GitHub

## ✅ Обязательные файлы для деплоя

### Основные файлы бота:
- `main.py` - главный файл для Render с webhook поддержкой
- `bot.py` - логика телеграм бота
- `config.py` - конфигурация с поддержкой переменных окружения
- `database.py` - работа с базой данных
- `keyboards.py` - клавиатуры и кнопки
- `requirements.txt` - зависимости Python

### Конфигурационные файлы:
- `.env.example` - пример переменных окружения
- `.gitignore` - исключения для Git
- `Dockerfile` - для контейнеризации
- `render.yaml` - конфигурация для Render

### Документация:
- `README.md` - основная документация
- `README_DEPLOY.md` - инструкция по деплою

### Тестирование и деплой:
- `test_health.py` - тестирование health endpoints
- `test_webhook.py` - локальное тестирование webhook режима
- `deploy.py` - скрипт подготовки к деплою
- `Makefile` - команды для разработки

### GitHub Actions:
- `.github/workflows/test.yml` - автоматическое тестирование

## ⚠️ НЕ загружайте эти файлы:

### Секретные данные:
- `.env` - ваши токены (добавлен в .gitignore)
- `config_local.py` - локальная конфигурация

### Временные файлы:
- `*.db` - база данных SQLite
- `*.log` - файлы логов
- `users_backup_*.db` - резервные копии БД
- `__pycache__/` - кэш Python

### Локальные скрипты (опционально):
- `run_bot.py` - система автоперезапуска (для локального использования)
- `setup_commands.py` - установка команд (для локального использования)
- `fix_database.py` - исправление БД (для локального использования)
- `*.bat` - Windows скрипты (для локального использования)
- `*.sh` - Linux/Mac скрипты (для локального использования)

## 📋 Итоговая структура репозитория:

```
weather-bot/
├── .github/
│   └── workflows/
│       └── test.yml
├── .env.example
├── .gitignore
├── bot.py
├── config.py
├── database.py
├── Dockerfile
├── keyboards.py
├── main.py
├── README.md
├── README_DEPLOY.md
├── render.yaml
├── requirements.txt
├── test_health.py
├── test_webhook.py
├── deploy.py
└── Makefile
```

## 🚀 Команды для загрузки:

```bash
# Инициализация Git (если еще не сделано)
git init
git add .
git commit -m "Initial commit: Weather Bot for Render"

# Добавление удаленного репозитория
git remote add origin https://github.com/YOUR_USERNAME/weather-bot.git

# Загрузка на GitHub
git branch -M main
git push -u origin main
```

## 🔑 После загрузки на GitHub:

1. **Не забудьте добавить переменные окружения в Render Dashboard**
2. **Проверьте, что .env файл не попал в репозиторий**
3. **Убедитесь, что все секретные данные в .gitignore**
#
# 📋 Итоговый чек-лист:

### ✅ Перед загрузкой на GitHub:
- [ ] Все файлы из списка выше присутствуют
- [ ] .env файл НЕ включен (должен быть в .gitignore)
- [ ] Токены НЕ в коде (используются переменные окружения)
- [ ] README.md содержит инструкции

### ✅ После загрузки на GitHub:
- [ ] Репозиторий создан и файлы загружены
- [ ] .env файл не попал в репозиторий
- [ ] Все секретные данные в .gitignore

### ✅ При деплое на Render:
- [ ] Web Service создан и подключен к GitHub
- [ ] Переменные окружения установлены
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `python main.py`
- [ ] Health Check Path: `/healthz`

### ✅ После деплоя:
- [ ] Health endpoint отвечает: `/healthz`
- [ ] Бот отвечает в Telegram
- [ ] Логи не показывают ошибок
- [ ] Webhook установлен успешно

## 🚀 Команды для быстрого старта:

```bash
# Проверка готовности
python deploy.py

# Тестирование health endpoints
python test_health.py https://your-app.onrender.com

# Локальное тестирование webhook
python test_webhook.py

# Использование Makefile
make help
make setup
make install
make test
make run
```

## 🎉 Готово к деплою!