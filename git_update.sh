#!/bin/bash
# Скрипт для обновления Weather Bot на GitHub

echo "🚀 Обновление Weather Bot v2.1 на GitHub..."
echo "=" * 50

# Проверяем статус git
echo "📋 Проверяем статус репозитория..."
git status

echo ""
echo "📦 Добавляем все изменения..."
git add .

echo ""
echo "💬 Создаем коммит с описанием изменений..."
git commit -m "🎉 Weather Bot v2.1: Добавлены команды в меню Telegram и Web App карта

✨ Новые возможности:
- 📋 Все команды теперь доступны в меню Telegram
- 🌍 Web App для интерактивной карты погоды с геолокацией
- 🗺️ Карты осадков, облачности, температуры и ветра
- 📱 Мобильная оптимизация и адаптация под тему Telegram

🔧 Обновленные файлы:
- bot.py - добавлены обработчики Web App и команд
- keyboards.py - новые клавиатуры с Web App
- setup_commands.py - обновлен список команд для меню

🆕 Новые файлы:
- weather_map.html - Web App для интерактивной карты
- serve_webapp.py - локальный сервер для тестирования
- .env.example - пример конфигурации
- UPDATE_SUMMARY.md - описание обновлений"

echo ""
echo "🌐 Отправляем изменения на GitHub..."
git push origin main

echo ""
echo "✅ Готово! Изменения отправлены на GitHub"
echo "🔗 Проверьте репозиторий: https://github.com/platezkaivan-droid/weatherbot"
echo ""
echo "📱 Если бот развернут на Render, он автоматически обновится через несколько минут"