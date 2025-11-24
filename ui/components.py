from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from config.settings import FONT_SIZE_NORMAL, FONT_SIZE_LARGE


class ElderLabel(MDLabel):
    """老年人专用文本标签：默认大字号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # KivyMD 2.0 颜色处理略有不同，但 Custom 模式基本兼容
        self.theme_text_color = "Custom"
        self.text_color = (0, 0, 0, 1)  # 纯黑
        if not self.font_style:
            self.font_style = "Body"
            self.role = "large"  # 使用内置的大号样式


class ElderButton(MDButton):
    """
    老年人专用按钮 (KivyMD 2.0适配版)
    结构：MDButton(容器) -> MDButtonText(文字)
    """

    def __init__(self, text="", **kwargs):
        # 1. 设置按钮容器样式
        kwargs.setdefault("style", "filled")  # 填充样式
        kwargs.setdefault("theme_width", "Custom")
        kwargs.setdefault("size_hint_x", 0.8)
        kwargs.setdefault("height", dp(80))
        kwargs.setdefault("size_hint_y", None)  # 必须显式关闭Y轴自适应以固定高度
        kwargs.setdefault("pos_hint", {"center_x": 0.5})

        super().__init__(**kwargs)

        # 2. 添加按钮内部文字
        # 注意：字号需要根据 KivyMD 2.0 的规范调整，这里使用 Display/Headline 样式模拟大字体
        self.add_widget(
            MDButtonText(
                text=text,
                font_style="Headline",
                role="small",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)  # 强制白字
            )
        )