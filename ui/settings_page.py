from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        self.add_widget(MDLabel(text="设置页（待开发）", halign="center"))