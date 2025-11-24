from kivy.utils import platform
import threading
import time


class VoiceAssistant:
    def __init__(self):
        self.engine = None
        # 仅在非安卓平台初始化 pyttsx3
        if platform != 'android':
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                # 尝试设置中文语音
                try:
                    voices = self.engine.getProperty('voices')
                    for v in voices:
                        # 优先找中文语音包 (Windows通常是 Huihui 或 Yaoyao)
                        if 'chinese' in v.name.lower() or 'cn' in v.id.lower():
                            self.engine.setProperty('voice', v.id)
                            break
                except:
                    pass
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 1.0)  # 确保最大音量
            except ImportError:
                print("未安装 pyttsx3")

    def speak(self, text):
        """启动语音播报线程"""
        # 先停止之前的播报（防止重叠）
        self.stop()
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()

    def _speak_thread(self, text):
        print(f"DEBUG [Voice]: 正在播报 -> {text[:10]}...")

        if platform == 'android':
            from plyer import tts
            try:
                tts.speak(text)
            except Exception as e:
                print(f"Android TTS Error: {e}")

        elif self.engine:
            try:
                # Windows 上的特殊处理：
                # 每次播报前重新初始化一下循环，防止阻塞
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"PC TTS Error: {e}")
                # 备用方案：如果 runAndWait 失败，尝试直接 print
                print("\a")  # 响铃一声提示

    def stop(self):
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass


voice_assistant = VoiceAssistant()