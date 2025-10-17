# Makefile для Weather Bot

.PHONY: help install test run webhook health deploy clean

help: ## Показать справку
	@echo "Weather Bot - Команды:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

test: ## Запустить тесты
	python -c "import bot, database, keyboards, config; print('✅ Все импорты успешны')"
	python -c "import database; database.init_db(); print('✅ База данных инициализирована')"

run: ## Запустить бота (polling режим)
	python main.py

webhook: ## Запустить в webhook режиме (для тестирования)
	python test_webhook.py

health: ## Тестировать health endpoints (требует URL)
	@if [ -z "$(URL)" ]; then \
		echo "Использование: make health URL=https://your-app.onrender.com"; \
	else \
		python test_health.py $(URL); \
	fi

deploy: ## Подготовка к деплою
	python deploy.py

clean: ## Очистить временные файлы
	rm -rf __pycache__/
	rm -f *.log
	rm -f *.db
	rm -f users_backup_*.db

setup: ## Первоначальная настройка
	@echo "🔧 Настройка Weather Bot"
	@echo "1. Скопируйте .env.example в .env"
	@echo "2. Заполните токены в .env файле"
	@echo "3. Запустите: make install && make test && make run"
	cp .env.example .env
	@echo "✅ Файл .env создан. Отредактируйте его!"

# Примеры использования:
# make install          - установить зависимости
# make test            - проверить работоспособность
# make run             - запустить бота локально
# make webhook         - тестировать webhook режим
# make health URL=https://your-app.onrender.com - тестировать health endpoints
# make deploy          - подготовка к деплою
# make clean           - очистить временные файлы