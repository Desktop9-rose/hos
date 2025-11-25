import os
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from config.settings import FONT_PATH, THEME_STYLE, PRIMARY_PALETTE
from ui.home import HomeScreen
from ui.history import HistoryScreen
from ui.result import ResultScreen
from ui.camera_page import CameraScreen  # <--- 新增导入


class MedicalApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

        if os.path.exists(FONT_PATH):
            LabelBase.register(name="Roboto", fn_regular=FONT_PATH, fn_bold=FONT_PATH)

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(CameraScreen(name='camera'))  # <--- 注册相机页

        return sm


if __name__ == '__main__':
    MedicalApp().run()