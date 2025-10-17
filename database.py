import sqlite3
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = 'users.db'

def init_db():
    """Инициализация базы данных с улучшенной структурой"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        
        # Проверяем существующую структуру таблицы
        cur.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cur.fetchall()]
        
        if not columns:
            # Таблица не существует, создаем новую
            logger.info("📝 Создаю новую таблицу users...")
            cur.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                city TEXT,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        else:
            # Таблица существует, проверяем и добавляем недостающие столбцы
            logger.info("🔄 Проверяю структуру существующей таблицы...")
            
            # Добавляем недостающие столбцы
            if 'username' not in columns:
                logger.info("➕ Добавляю столбец username...")
                cur.execute('ALTER TABLE users ADD COLUMN username TEXT')
                
            if 'first_name' not in columns:
                logger.info("➕ Добавляю столбец first_name...")
                cur.execute('ALTER TABLE users ADD COLUMN first_name TEXT')
                
            if 'created_at' not in columns:
                logger.info("➕ Добавляю столбец created_at...")
                cur.execute('ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                
            if 'updated_at' not in columns:
                logger.info("➕ Добавляю столбец updated_at...")
                cur.execute('ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            
            # Убираем NOT NULL с city если он есть (для совместимости)
            if 'city' in columns:
                logger.info("🔧 Обновляю структуру таблицы...")
                # Создаем временную таблицу с правильной структурой
                cur.execute('''
                CREATE TABLE users_new (
                    user_id INTEGER PRIMARY KEY,
                    city TEXT,
                    username TEXT,
                    first_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Копируем данные
                cur.execute('''
                INSERT INTO users_new (user_id, city, username, first_name, created_at, updated_at)
                SELECT 
                    user_id, 
                    city,
                    CASE WHEN 'username' IN (SELECT name FROM pragma_table_info('users')) THEN username ELSE NULL END,
                    CASE WHEN 'first_name' IN (SELECT name FROM pragma_table_info('users')) THEN first_name ELSE NULL END,
                    CASE WHEN 'created_at' IN (SELECT name FROM pragma_table_info('users')) THEN created_at ELSE CURRENT_TIMESTAMP END,
                    CASE WHEN 'updated_at' IN (SELECT name FROM pragma_table_info('users')) THEN updated_at ELSE CURRENT_TIMESTAMP END
                FROM users
                ''')
                
                # Удаляем старую таблицу и переименовываем новую
                cur.execute('DROP TABLE users')
                cur.execute('ALTER TABLE users_new RENAME TO users')
        
        # Создаем индекс для быстрого поиска
        cur.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id)')
        
        conn.commit()
        logger.info("✅ База данных успешно инициализирована")
        
        # Показываем финальную структуру
        cur.execute("PRAGMA table_info(users)")
        columns_info = cur.fetchall()
        logger.info("📋 Структура таблицы users:")
        for col in columns_info:
            logger.info(f"   {col[1]} ({col[2]})")
        
    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        raise
    finally:
        if conn:
            conn.close()

def set_user_city(user_id, city, username=None, first_name=None):
    """Установка города пользователя с дополнительной информацией"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        
        # Проверяем структуру таблицы
        cur.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cur.fetchall()]
        
        # Проверяем, существует ли пользователь
        cur.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        exists = cur.fetchone()
        
        if exists:
            # Обновляем существующего пользователя
            if 'username' in columns and 'first_name' in columns and 'updated_at' in columns:
                # Полная структура
                cur.execute('''
                    UPDATE users 
                    SET city = ?, username = ?, first_name = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ?
                ''', (city, username, first_name, user_id))
            else:
                # Базовая структура
                cur.execute('''
                    UPDATE users 
                    SET city = ?
                    WHERE user_id = ?
                ''', (city, user_id))
        else:
            # Создаем нового пользователя
            if 'username' in columns and 'first_name' in columns:
                # Полная структура
                cur.execute('''
                    INSERT INTO users (user_id, city, username, first_name) 
                    VALUES (?, ?, ?, ?)
                ''', (user_id, city, username, first_name))
            else:
                # Базовая структура
                cur.execute('''
                    INSERT INTO users (user_id, city) 
                    VALUES (?, ?)
                ''', (user_id, city))
        
        conn.commit()
        logger.info(f"✅ Город '{city}' установлен для пользователя {user_id}")
        
    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка при установке города: {e}")
        # Попробуем базовый вариант без дополнительных полей
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cur = conn.cursor()
            cur.execute('INSERT OR REPLACE INTO users (user_id, city) VALUES (?, ?)', (user_id, city))
            conn.commit()
            logger.info(f"✅ Город '{city}' установлен для пользователя {user_id} (базовый режим)")
        except sqlite3.Error as e2:
            logger.error(f"❌ Критическая ошибка при установке города: {e2}")
            raise
        finally:
            if conn:
                conn.close()
    finally:
        if conn:
            conn.close()

def get_user_city(user_id):
    """Получение города пользователя"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        
        cur.execute('SELECT city FROM users WHERE user_id = ?', (user_id,))
        result = cur.fetchone()
        
        if result:
            logger.debug(f"Город для пользователя {user_id}: {result[0]}")
            return result[0]
        else:
            logger.debug(f"Город для пользователя {user_id} не найден")
            return None
            
    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка при получении города: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_stats():
    """Получение статистики пользователей"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cur = conn.cursor()
        
        cur.execute('SELECT COUNT(*) FROM users')
        total_users = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(DISTINCT city) FROM users WHERE city IS NOT NULL')
        unique_cities = cur.fetchone()[0]
        
        return {
            'total_users': total_users,
            'unique_cities': unique_cities
        }
        
    except sqlite3.Error as e:
        logger.error(f"❌ Ошибка при получении статистики: {e}")
        return {'total_users': 0, 'unique_cities': 0}
    finally:
        if conn:
            conn.close()

def backup_database():
    """Создание резервной копии базы данных"""
    try:
        if os.path.exists(DB_PATH):
            backup_name = f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            # Копируем файл
            import shutil
            shutil.copy2(DB_PATH, backup_name)
            
            logger.info(f"✅ Резервная копия создана: {backup_name}")
            return backup_name
        else:
            logger.warning("⚠️ Файл базы данных не найден для создания резервной копии")
            return None
            
    except Exception as e:
        logger.error(f"❌ Ошибка при создании резервной копии: {e}")
        return None