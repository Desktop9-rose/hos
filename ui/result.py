import threading
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp

# 导入 UI 组件
from ui.components import ElderButton, ElderLabel

# 导入业务模块
from privacy.desensitize import desensitizer
from ocr.cloud_ocr import cloud_ocr  # [升级] 替换为云端 OCR
from ai.cloud_ai import cloud_ai  # [升级] 替换为云端双 AI
from utils.voice import voice_assistant
from config.db import db


class ResultCard(MDCard):
    """结果展示卡片 (样式保持不变)"""

    def __init__(self, title, content, color=(0.98, 0.98, 0.98, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = "20dp"
        self.radius = [15, 15, 15, 15]
        self.theme_bg_color = "Custom"
        self.md_bg_color = color

        self.add_widget(MDLabel(
            text=title,
            font_style="Title",
            role="medium",
            size_hint_y=None,
            height="35dp",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            bold=True
        ))
        self.content_label = MDLabel(
            text=content,
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            line_height=1.3,
            font_style="Body",
            role="large"
        )
        self.content_label.bind(texture_size=self.update_height)
        self.add_widget(self.content_label)

    def update_height(self, instance, value):
        instance.height = value[1]
        self.height = value[1] + dp(80)


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

        # 1. 状态提示 (放大字号，让老人看得更清楚)
        self.status_label = ElderLabel(
            text="准备就绪",
            halign="center",
            size_hint_y=None,
            height="80dp",
            font_style="Headline",
            role="small"
        )

        # 2. 图片预览
        self.image_preview = Image(
            size_hint_y=None,
            height="250dp",
            allow_stretch=True,
            keep_ratio=True
        )

        # 3. 结果卡片容器
        self.result_container = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            size_hint_y=None,
            adaptive_height=True
        )

        # 4. 底部操作栏
        btn_layout = MDBoxLayout(spacing="20dp", size_hint_y=None, height="90dp")
        btn_speak = ElderButton(text="🔊 播报")
        btn_speak.size_hint_x = 0.5
        btn_speak.bind(on_release=self.play_voice)

        btn_back = ElderButton(text="返回")
        btn_back.size_hint_x = 0.5
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
        """入口：接收图片路径，开始流水线"""
        self.current_image_path = file_path
        self.image_preview.source = file_path
        self.image_preview.reload()

        # 重置界面
        self.result_container.clear_widgets()
        self.analysis_result = None
        self.status_label.text = "⏳ 正在启动分析..."

        # 开始流程 (延迟1秒给UI渲染时间)
        Clock.schedule_once(self.pipeline_step_1_desensitize, 1.0)

    # --- 步骤 1: 本地脱敏 ---
    def pipeline_step_1_desensitize(self, dt):
        self.status_label.text = "🛡️ 正在处理隐私信息..."
        output_path = self.current_image_path.replace(".jpg", "_blur.jpg")

        # 本地操作，直接运行
        success = desensitizer.blur_image_region(self.current_image_path, output_path)

        if success:
            self.image_preview.source = output_path
            self.image_preview.reload()
            # 下一步：云端 OCR (耗时操作，需开启新线程)
            self.pipeline_step_2_ocr_async(output_path)
        else:
            self.status_label.text = "❌ 图片处理失败，请重试"

    # --- 步骤 2: 云端 OCR (异步) ---
    def pipeline_step_2_ocr_async(self, image_path):
        self.status_label.text = "☁️ 正在扫描文字 (百度云)..."
        # 开启线程
        threading.Thread(target=self._thread_ocr, args=(image_path,), daemon=True).start()

    def _thread_ocr(self, image_path):
        # [子线程] 执行网络请求
        ocr_result = cloud_ocr.recognize(image_path)

        # 回到主线程更新 UI
        if isinstance(ocr_result, dict) and "error" in ocr_result:
            Clock.schedule_once(lambda dt: self._show_error(ocr_result["error"]), 0)
        else:
            # 成功拿到文字，脱敏后传给 AI
            safe_text = desensitizer.desensitize_text(ocr_result)
            Clock.schedule_once(lambda dt: self.pipeline_step_3_ai_async(safe_text), 0)

    # --- 步骤 3: 双 AI 解读 (异步) ---
    def pipeline_step_3_ai_async(self, text):
        self.status_label.text = "🧠 双 AI 专家正在会诊..."
        # 开启线程
        threading.Thread(target=self._thread_ai, args=(text,), daemon=True).start()

    def _thread_ai(self, text):
        # [子线程] 调用 DeepSeek + 通义
        ai_result = cloud_ai.analyze(text)

        # 回到主线程展示结果
        Clock.schedule_once(lambda dt: self._show_final_result(ai_result), 0)

    # --- 步骤 4: 展示结果 & 存库 ---
    def _show_final_result(self, result):
        self.analysis_result = result
        self.status_label.text = "✅ 解读完成"

        # 1. 渲染卡片
        # 核心结论 (蓝色背景)
        self.result_container.add_widget(
            ResultCard("💡 核心结论", result.get('summary', '无'), color=(0.85, 0.93, 1, 1))
        )

        # 异常指标 (红色背景，仅当有异常时显示)
        anomalies = result.get('anomalies', [])
        if anomalies and "无" not in str(anomalies):
            content = "\n".join(anomalies)
            self.result_container.add_widget(
                ResultCard("⚠️ 异常指标", content, color=(1, 0.88, 0.88, 1))
            )

        # 生活建议 (绿色背景)
        advice = result.get('advice', [])
        if advice:
            content = "\n".join(advice)
            self.result_container.add_widget(
                ResultCard("❤️ 生活建议", content, color=(0.88, 1, 0.88, 1))
            )

        # 2. 自动播放语音
        self.play_voice(None)

        # 3. 保存到历史记录
        if self.current_image_path:
            db.add_history(
                result.get('summary', '自动解读'),
                result,
                self.current_image_path
            )

    def _show_error(self, error_msg):
        """通用报错显示"""
        self.status_label.text = "⚠️ 发生错误"
        self.result_container.add_widget(
            ResultCard("错误详情", error_msg, color=(1, 0.8, 0.8, 1))
        )
        voice_assistant.speak("很抱歉，处理过程中发生了错误。")

    def play_voice(self, instance):
        """语音播报逻辑"""
        if not self.analysis_result:
            return

        res = self.analysis_result
        text = "解读结果如下。"

        if res.get('summary'):
            text += f"核心结论：{res['summary']}。"

        anomalies = res.get('anomalies', [])
        if anomalies and "无" not in str(anomalies):
            text += "发现以下异常指标：" + "，".join(anomalies[:3]) + "。"  # 只读前3个防止太长

        advice = res.get('advice', [])
        if advice:
            text += "建议您：" + "，".join(advice[:2])  # 只读前2条

        text += "解读仅供参考，请以医生诊断为准。"
        voice_assistant.speak(text)

    def go_back(self, instance):
        voice_assistant.stop()
        if self.manager:
            self.manager.current = 'home'