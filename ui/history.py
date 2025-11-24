from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty  # 修复报错的关键
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from ui.components import ElderLabel, ElderButton


class HistoryScreen(Screen):
    # 定义属性（必须在类级别定义）
    has_records = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'history'
        self.build_ui()

    def build_ui(self):
        # 垂直布局
        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            md_bg_color=(0.96, 0.96, 0.96, 1)
        )

        # 标题
        title = ElderLabel(
            text="历史记录",
            halign="center",
            size_hint_y=None,
            height="80dp",
            font_style="Headline",
            role="medium"
        )
        layout.add_widget(title)

        # 这里的逻辑后续会根据数据库动态生成列表
        # 目前先放一个占位提示
        self.no_record_label = ElderLabel(
            text="暂无历史记录",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.no_record_label)

        # 占位弹簧
        layout.add_widget(MDWidget(size_hint_y=1))

        # 返回按钮
        btn_back = ElderButton(text="返回首页")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'home'