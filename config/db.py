import sqlite3
import json
from config.settings import DB_PATH, DEFAULT_CONFIG

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False) # 允许跨线程调用
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
        # 历史表：增加 details 字段存储 JSON 数据
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date TEXT,
                summary TEXT,
                details TEXT,  -- JSON 字符串
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.init_default_settings()
        self.conn.commit()

    def init_default_settings(self):
        for key, value in DEFAULT_CONFIG.items():
            self.cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
            if not self.cursor.fetchone():
                self.cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?)', (key, str(value)))

    # --- 新增：保存历史记录 ---
    def add_history(self, summary, details_dict, file_path):
        import datetime
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            self.cursor.execute(
                'INSERT INTO history (report_date, summary, details, file_path) VALUES (?, ?, ?, ?)',
                (date_str, summary, json.dumps(details_dict, ensure_ascii=False), file_path)
            )
            self.conn.commit()
            print("DEBUG [DB]: 历史记录保存成功")
        except Exception as e:
            print(f"DEBUG [DB]: 保存失败 {e}")

    # --- 新增：获取所有记录 ---
    def get_all_history(self):
        self.cursor.execute('SELECT * FROM history ORDER BY id DESC')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

db = DatabaseManager()