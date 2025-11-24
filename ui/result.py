from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

from ui.components import ElderButton, ElderLabel
from privacy.desensitize import desensitizer
from ocr.local_ocr import ocr_engine
from ai.local_ai import local_ai
from utils.voice import voice_assistant


class ResultCard(MDCard):
    """封装结果展示卡片 (修复颜色显示)"""

    def __init__(self, title, content, color=(0.98, 0.98, 0.98, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = "20dp"
        self.radius = [15, 15, 15, 15]

        # [关键修复] KivyMD 2.0 必须设置这个才能自定义背景色
        self.theme_bg_color = "Custom"
        self.md_bg_color = color

        # 标题
        self.add_widget(MDLabel(
            text=title,
            font_style="Title",
            role="medium",
            size_hint_y=None,
            height="30dp",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),  # 强制黑色标题
            bold=True
        ))

        # 内容
        self.content_label = MDLabel(
            text=content,
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),  # 强制深灰内容
            size_hint_y=None,
            line_height=1.2
        )
        self.content_label.bind(texture_size=self.update_height)
        self.add_widget(self.content_label)

    def update_height(self, instance, value):
        instance.height = value[1]
        self.height = value[1] + dp(70)


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result'
        self.current_image_path = None
        self.build_ui()

    def build_ui(self):
        self.main_scroll = ScrollView()
        self.layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint_y=None,
            adaptive_height=True
        )

        # 状态提示 (加大字号，更显眼)
        self.status_label = ElderLabel(
            text="准备解读...",
            halign="center",
            size_hint_y=None,
            height="60dp",
            font_style="Headline",
            role="small"
        )

        self.image_preview = Image(
            size_hint_y=None,
            height="200dp",
            allow_stretch=True,
            keep_ratio=True
        )

        self.result_container = MDBoxLayout(
            orientation='vertical',
            spacing="15dp",
            size_hint_y=None,
            adaptive_height=True
        )

        btn_layout = MDBoxLayout(spacing="20dp", size_hint_y=None, height="80dp")
        btn_speak = ElderButton(text="🔊 重新播报")
        btn_speak.size_hint_x = 0.4
        btn_speak.bind(on_release=self.play_voice)

        btn_back = ElderButton(text="返回")
        btn_back.size_hint_x = 0.4
        btn_back.bind(on_release=self.go_back)

        btn_layout.add_widget(btn_speak)
        btn_layout.add_widget(btn_back)

        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.image_preview)
        self.layout.add_widget(self.result_container)
        self.layout.add_widget(btn_layout)

        self.main_scroll.add_widget(self.layout)
        self.add_widget(self.main_scroll)

    def set_image(self, file_path):
        self.current_image_path = file_path
        self.image_preview.source = file_path
        self.image_preview.reload()
        self.result_container.clear_widgets()
        self.analysis_result = None

        # 步骤 0: 初始状态
        self.status_label.text = "⏳ 正在初始化..."
        Clock.schedule_once(self.step_1_desensitize, 1.0)

    def step_1_desensitize(self, dt):
        self.status_label.text = "🛡️ 正在进行隐私脱敏..."

        # 延迟 1.5秒 执行实际操作，让用户看清提示
        Clock.schedule_once(self._do_desensitize, 1.5)

    def _do_desensitize(self, dt):
        output_path = self.current_image_path.replace(".jpg", "_blur.jpg")
        success = desensitizer.blur_image_region(self.current_image_path, output_path)

        if success:
            self.image_preview.source = output_path
            self.image_preview.reload()
            # 进入下一步
            self.step_2_ocr(output_path)
        else:
            self.status_label.text = "❌ 图片处理失败"

    def step_2_ocr(self, image_path):
        self.status_label.text = "👁️ 正在识别文字..."
        Clock.schedule_once(lambda d: self._do_ocr(image_path), 1.5)

    def _do_ocr(self, image_path):
        ocr_text = ocr_engine.extract_text(image_path)
        # 进入下一步
        self.step_3_ai(ocr_text)

    def step_3_ai(self, ocr_text):
        self.status_label.text = "🧠 正在生成智能解读..."
        Clock.schedule_once(lambda d: self._do_ai(ocr_text), 1.5)

    def _do_ai(self, ocr_text):
        result = local_ai.analyze_report(ocr_text)
        self.analysis_result = result

        # 渲染彩色卡片 (注意颜色代码)
        # 核心结论 - 淡蓝色
        self.result_container.add_widget(
            ResultCard("💡 核心结论", result['summary'], color=(0.8, 0.9, 1, 1))
        )

        # 异常指标 - 淡红色
        if result['anomalies']:
            self.result_container.add_widget(
                ResultCard("⚠️ 异常指标", "\n".join(result['anomalies']), color=(1, 0.85, 0.85, 1))
            )

        # 生活建议 - 淡绿色
        self.result_container.add_widget(
            ResultCard("❤️ 生活建议", "\n".join(result['advice']), color=(0.85, 1, 0.85, 1))
        )

        self.status_label.text = "✅ 解读完成"
        self.play_voice(None)

    def play_voice(self, instance):
        if self.analysis_result:
            # 构建更自然的语音文本
            text = f"解读完成。{self.analysis_result['summary']}。"
            if self.analysis_result['anomalies']:
                text += "其中，异常指标有：" + "，".join(self.analysis_result['anomalies']) + "。"
            text += "建议您：" + "，".join(self.analysis_result['advice'])

            voice_assistant.speak(text)

    def go_back(self, instance):
        voice_assistant.stop()
        if self.manager:
            self.manager.current = 'home'