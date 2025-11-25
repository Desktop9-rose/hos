import os
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivy.utils import platform
from kivy.clock import Clock
from plyer import filechooser, camera

from ui.components import ElderButton, ElderLabel
from utils.file_handler import file_handler
from privacy.permission import check_permissions


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.build_ui()
        # 延迟申请权限
        Clock.schedule_once(lambda dt: check_permissions(), 1)

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=[40, 60, 40, 40], spacing=40,
                             md_bg_color=(0.96, 0.96, 0.96, 1))
        title = ElderLabel(text="医疗报告解读助手", halign="center", size_hint_y=None, height="100dp",
                           font_style="Headline", role="medium")

        btn_camera = ElderButton(text="📷 拍照解读")
        btn_camera.bind(on_release=self.go_camera)

        btn_gallery = ElderButton(text="🖼️ 相册选择")
        btn_gallery.bind(on_release=self.go_gallery)

        btn_history = ElderButton(text="📜 历史记录")
        btn_history.bind(on_release=self.go_history)

        layout.add_widget(title)
        layout.add_widget(btn_camera)
        layout.add_widget(btn_gallery)
        layout.add_widget(btn_history)
        layout.add_widget(MDWidget(size_hint_y=1))
        self.add_widget(layout)

    # --- 核心逻辑：拍照 ---
    def go_camera(self, instance):
        print("DEBUG [Home]: 尝试启动相机...")
        filename = datetime.now().strftime("CAM_%Y%m%d_%H%M%S.jpg")
        # 构造临时存储路径
        save_path = os.path.join(file_handler.app_dir, filename)

        try:
            # 调用原生相机
            camera.take_picture(filename=save_path, on_complete=self._on_camera_complete)
        except NotImplementedError:
            print("DEBUG [Home]: 当前环境不支持相机 (可能是电脑)")
            # 电脑端回退到选图
            self.open_file_chooser()
        except Exception as e:
            print(f"DEBUG [Home]: 相机启动失败 -> {e}")

    def _on_camera_complete(self, path):
        # 相机回调
        print(f"DEBUG [Home]: 拍照完成，路径 -> {path}")
        if path and os.path.exists(path):
            # 必须在主线程跳转
            Clock.schedule_once(lambda dt: self._switch_to_result(path), 0)
        else:
            print("DEBUG [Home]: 未找到拍摄的图片")

    # --- 核心逻辑：选图 ---
    def go_gallery(self, instance):
        self.open_file_chooser()

    def open_file_chooser(self):
        try:
            filechooser.open_file(on_selection=self._on_file_selected, filters=[("Images", "*.jpg", "*.jpeg", "*.png")])
        except Exception as e:
            print(f"DEBUG [Home]: 打开相册失败 -> {e}")

    def _on_file_selected(self, selection):
        if not selection: return
        file_path = selection[0]

        # 复制图片到私有目录
        saved_path = file_handler.save_selected_image(file_path)
        if saved_path:
            Clock.schedule_once(lambda dt: self._switch_to_result(saved_path), 0)

    def _switch_to_result(self, path):
        self.manager.get_screen('result').set_image(path)
        self.manager.current = 'result'

    def go_history(self, instance):
        # 切换前刷新数据
        self.manager.get_screen('history').load_data()
        self.manager.current = 'history'