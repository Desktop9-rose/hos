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
from ocr.cloud_ocr import cloud_ocr
from ai.cloud_ai import cloud_ai
from utils.voice import voice_assistant
from config.db import db


class ResultCard(MDCard):
    def __init__(self, title, content, color=(0.98, 0.98, 0.98, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = "20dp"
        self.radius = [15, 15, 15, 15]
        self.theme_bg_color = "Custom"
        self.md_bg_color = color
        self.add_widget(MDLabel(text=title, font_style="Title", role="medium", size_hint_y=None, height="35dp",
                                theme_text_color="Custom", text_color=(0, 0, 0, 1), bold=True))
        self.content_label = MDLabel(text=content, theme_text_color="Custom", text_color=(0.1, 0.1, 0.1, 1),
                                     size_hint_y=None, line_height=1.3)
        self.content_label.bind(texture_size=self.update_height)
        self.add_widget(self.content_label)

    def update_height(self, instance, value):
        instance.height = value[1] + dp(80)


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result'
        self.current_image_path = None
        self.build_ui()

    def build_ui(self):
        self.main_scroll = ScrollView()
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None,
                                  adaptive_height=True)
        self.status_label = ElderLabel(text="准备就绪", halign="center", size_hint_y=None, height="80dp",
                                       font_style="Headline", role="small")
        self.image_preview = Image(size_hint_y=None, height="250dp", allow_stretch=True, keep_ratio=True)
        self.result_container = MDBoxLayout(orientation='vertical', spacing="20dp", size_hint_y=None,
                                            adaptive_height=True)
        btn_layout = MDBoxLayout(spacing="20dp", size_hint_y=None, height="90dp")
        btn_speak = ElderButton(text="🔊 播报")
        btn_speak.bind(on_release=self.play_voice)
        btn_back = ElderButton(text="返回")
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
        self.status_label.text = "⏳ 正在启动分析..."
        Clock.schedule_once(self.step_1, 1.0)

    def step_1(self, dt):
        self.status_label.text = "🛡️ 正在处理隐私信息..."
        output_path = self.current_image_path.replace(".jpg", "_blur.jpg")
        # 本地脱敏
        if desensitizer.blur_image_region(self.current_image_path, output_path):
            self.image_preview.source = output_path
            self.image_preview.reload()
            self.step_2(output_path)
        else:
            self.status_label.text = "❌ 图片处理失败"

    def step_2(self, image_path):
        self.status_label.text = "☁️ 正在扫描文字 (百度云)..."
        # 调用云端OCR (非阻塞)
        cloud_ocr.recognize(image_path, self.on_ocr_result)

    def on_ocr_result(self, text, error):
        # OCR 回调
        if error:
            self.status_label.text = f"⚠️ 识别中断: {error}"
            return

        safe_text = desensitizer.desensitize_text(text)
        self.step_3(safe_text)

    def step_3(self, text):
        self.status_label.text = "🧠 AI 专家正在会诊..."
        # 调用云端AI (非阻塞)
        cloud_ai.analyze(text, self.on_ai_result)

    def on_ai_result(self, result):
        # AI 回调
        self.analysis_result = result
        self.status_label.text = "✅ 解读完成"

        self.result_container.add_widget(
            ResultCard("💡 核心结论", result.get('summary', '无'), color=(0.85, 0.93, 1, 1)))

        anomalies = result.get('anomalies', [])
        if anomalies:
            self.result_container.add_widget(ResultCard("⚠️ 异常指标", "\n".join(anomalies), color=(1, 0.88, 0.88, 1)))

        advice = result.get('advice', [])
        if advice:
            self.result_container.add_widget(ResultCard("❤️ 生活建议", "\n".join(advice), color=(0.88, 1, 0.88, 1)))

        if self.current_image_path:
            db.add_history(result.get('summary', '自动解读'), result, self.current_image_path)

        self.play_voice(None)

    def play_voice(self, instance):
        if self.analysis_result:
            voice_assistant.speak(f"解读结果：{self.analysis_result.get('summary', '')}")

    def go_back(self, instance):
        voice_assistant.stop()
        if self.manager:
            self.manager.current = 'home'