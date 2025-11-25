from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


class ElderLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = "Custom"
        self.text_color = (0, 0, 0, 1)
        # 1.1.1 的样式名称略有不同，H5/Body1 是标准写法
        if not self.font_style:
            self.font_style = "Body1"


class ElderButton(MDFillRoundFlatButton):
    """
    适配 KivyMD 1.1.1 的大按钮
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 强制大字体
        self.font_size = "24sp"
        # 宽度设置
        self.size_hint_x = 0.8
        self.pos_hint = {"center_x": 0.5}
        # 高度设置
        self.height = dp(60)
        # 1.1.1 中圆角的写法
        self.radius = [15, 15, 15, 15]

        # 如果没有传入背景色，默认给一个醒目的颜色 (Teal)
        if 'md_bg_color' not in kwargs:
            self.md_bg_color = (0, 0.5, 0.5, 1)