import sqlite3
import json
from config.settings import DB_PATH, DEFAULT_CONFIG


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        """初始化数据库表结构"""
        # 1. 配置表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # 2. 历史记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date TEXT,
                report_type TEXT,
                summary TEXT,
                full_result TEXT,   -- JSON格式存储详细结果
                file_path TEXT,     -- 图片路径
                is_deleted INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 初始化默认设置（如果不存在）
        self.init_default_settings()
        self.conn.commit()

    def init_default_settings(self):
        for key, value in DEFAULT_CONFIG.items():
            self.cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
            if not self.cursor.fetchone():
                self.cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?)',
                                    (key, str(value)))

    def get_setting(self, key):
        self.cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_setting(self, key, value):
        self.cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                            (key, str(value)))
        self.conn.commit()

    def close(self):
        self.conn.close()


# 单例实例
db = DatabaseManager()