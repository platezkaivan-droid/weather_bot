#!/usr/bin/env python3
"""
Скрипт для исправления структуры базы данных
"""

import sqlite3
import logging
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = 'users.db'

def fix_database():
    """Исправляет структуру базы данных"""
    try:
        if not os.path.exists(DB_PATH):
            logger.info("📝 База данных не существует, будет создана при запуске бота")
            return True
            
        # Создаем резервную копию
        backup_name = f"users_backup_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        import shutil
        shutil.copy2(DB_PATH, backup_name)
        logger.info(f"💾 Создана резервная копия: {backup_name}")
        
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        
        # Проверяем текущую структуру
        cur.execute("PRAGMA table_info(users)")
        columns_info = cur.fetchall()
        columns = [col[1] for col in columns_info]
        
        logger.info("🔍 Текущая структура таблицы users:")
        for col in columns_info:
            logger.info(f"   {col[1]} ({col[2]})")
        
        if not columns:
            logger.info("❌ Таблица users не найдена")
            return False
            
        # Создаем новую таблицу с правильной структурой
        logger.info("🔧 Создаю новую таблицу с правильной структурой...")
        cur.execute('''
        CREATE TABLE users_fixed (
            user_id INTEGER PRIMARY KEY,
            city TEXT,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Копируем данные из старой таблицы
        logger.info("📋 Копирую данные...")
        if 'city' in columns:
            cur.execute('SELECT user_id, city FROM users')
            old_data = cur.fetchall()
            
            for user_id, city in old_data:
                cur.execute('''
                INSERT INTO users_fixed (user_id, city, created_at, updated_at) 
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (user_id, city))
            
            logger.info(f"✅ Скопировано записей: {len(old_data)}")
        
        # Удаляем старую таблицу и переименовываем новую
        logger.info("🔄 Обновляю структуру...")
        cur.execute('DROP TABLE users')
        cur.execute('ALTER TABLE users_fixed RENAME TO users')
        
        # Создаем индекс
        cur.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id)')
        
        conn.commit()
        
        # Проверяем результат
        cur.execute("PRAGMA table_info(users)")
        new_columns = cur.fetchall()
        
        logger.info("✅ Новая структура таблицы users:")
        for col in new_columns:
            logger.info(f"   {col[1]} ({col[2]})")
        
        # Показываем данные
        cur.execute('SELECT COUNT(*) FROM users')
        count = cur.fetchone()[0]
        logger.info(f"📊 Всего записей в базе: {count}")
        
        logger.info("🎉 База данных успешно исправлена!")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка при исправлении БД: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🔧 Исправление базы данных Weather Bot")
    print("=" * 40)
    
    success = fix_database()
    
    if success:
        print("\n✅ База данных успешно исправлена!")
        print("💡 Теперь можно запускать бота")
    else:
        print("\n❌ Ошибка при исправлении базы данных")
        print("💡 Попробуйте удалить файл users.db и перезапустить бота")