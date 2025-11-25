from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

from ui.components import ElderLabel, ElderButton
from config.db import db


class HistoryItem(MDCard):
    """单个历史记录卡片"""

    def __init__(self, date, summary, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = "100dp"
        self.padding = "15dp"
        self.radius = [10, 10, 10, 10]
        self.theme_bg_color = "Custom"
        self.md_bg_color = (0.95, 0.95, 0.95, 1)

        # 日期
        self.add_widget(MDLabel(
            text=date,
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="Label",
            role="large"
        ))
        # 结论摘要
        self.add_widget(MDLabel(
            text=summary,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Body",
            role="large",
            bold=True
        ))


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'history'
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, md_bg_color=(0.98, 0.98, 0.98, 1))

        # 标题栏
        header = MDBoxLayout(size_hint_y=None, height="80dp", spacing="10dp")
        back_btn = ElderButton(text="< 返回")
        back_btn.size_hint_x = 0.3
        back_btn.bind(on_release=self.go_back)

        title = ElderLabel(text="历史记录", halign="center", font_style="Headline", role="medium")

        header.add_widget(back_btn)
        header.add_widget(title)

        # 列表容器
        self.scroll = ScrollView()
        self.list_layout = MDBoxLayout(orientation='vertical', spacing="15dp", size_hint_y=None, adaptive_height=True)
        self.list_layout.padding = [0, 10, 0, 20]

        self.scroll.add_widget(self.list_layout)

        layout.add_widget(header)
        layout.add_widget(self.scroll)
        self.add_widget(layout)

    def load_data(self):
        """刷新列表数据"""
        self.list_layout.clear_widgets()
        rows = db.get_all_history()

        if not rows:
            self.list_layout.add_widget(ElderLabel(text="暂无记录", halign="center", size_hint_y=None, height="200dp"))
            return

        # rows: [(id, date, summary, ...), ...]
        for row in rows:
            date_str = row[1]
            summary = row[2]
            item = HistoryItem(date_str, summary)
            self.list_layout.add_widget(item)

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'home'