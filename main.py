import os
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from config.settings import FONT_PATH, THEME_STYLE, PRIMARY_PALETTE
from ui.home import HomeScreen
from ui.history import HistoryScreen
from ui.result import ResultScreen  # <--- 1. 取消注释这行


# from ui.settings_page import SettingsScreen

class MedicalApp(MDApp):
    def build(self):
        # 1. 配置主题
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

        # 2. 注册中文字体
        if os.path.exists(FONT_PATH):
            LabelBase.register(name="Roboto", fn_regular=FONT_PATH, fn_bold=FONT_PATH)
            print(f"字体加载成功: {FONT_PATH}")
        else:
            print(f"警告: 未找到字体文件 {FONT_PATH}")

        # 3. 构建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(ResultScreen(name='result'))  # <--- 2. 取消注释这行，并注册 ResultScreen
        # sm.add_widget(SettingsScreen(name='settings'))

        return sm


if __name__ == '__main__':
    MedicalApp().run()