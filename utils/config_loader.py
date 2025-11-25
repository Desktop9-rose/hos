import configparser
import os
import sys


class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = self._get_config_path()
        self._load_config()

    def _get_config_path(self):
        """获取配置文件路径"""
        # 1. 优先查找当前目录
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ini_path = os.path.join(current_dir, 'config.ini')

        if os.path.exists(ini_path):
            return ini_path

        # 2. 如果是在 Android APK 内部运行，可能需要特殊处理
        # Kivy 通常会将根目录文件打包在 ./
        return 'config.ini'

    def _load_config(self):
        try:
            # 必须指定 utf-8 编码，否则中文注释会报错
            read_files = self.config.read(self.config_path, encoding='utf-8')
            if not read_files:
                print(f"⚠️ [Config] 未找到配置文件: {self.config_path}")
        except Exception as e:
            print(f"❌ [Config] 配置文件读取错误: {e}")

    def get(self, section, key, default=None):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def get_int(self, section, key, default=0):
        try:
            return self.config.getint(section, key)
        except:
            return default


# 单例模式
config_manager = ConfigManager()

if __name__ == "__main__":
    # 测试代码
    print("Baidu Key:", config_manager.get("BAIDU_OCR", "API_KEY"))