import os
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivy.utils import platform
from kivy.clock import Clock
from plyer import filechooser

from ui.components import ElderButton, ElderLabel
from utils.file_handler import file_handler
from utils.android_camera import android_camera  # 导入新写的相机类
from privacy.permission import check_permissions


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.build_ui()
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

    # --- 📸 修复后的拍照逻辑 ---
    def go_camera(self, instance):
        # 生成保存路径 (Android 私有目录)
        filename = datetime.now().strftime("CAM_%Y%m%d_%H%M%S.jpg")
        save_path = os.path.join(file_handler.app_dir, filename)

        print(f"DEBUG [Home] 准备拍照，目标路径: {save_path}")

        # 调用原生相机
        android_camera.take_picture(
            filename=save_path,
            on_complete=self._on_image_ready  # 拍照完成后的回调
        )

    # --- 🖼️ 修复后的相册逻辑 ---
    def go_gallery(self, instance):
        print("DEBUG [Home] 打开相册")
        try:
            # filters 只在电脑端有效，安卓端主要靠 MIME type (image/*)
            # plyer 在安卓上默认会打开最近文件或图库
            filechooser.open_file(
                on_selection=self._on_gallery_selection,
                filters=[("Images", "*.jpg", "*.jpeg", "*.png")]
            )
        except Exception as e:
            print(f"DEBUG [Home] 打开相册异常: {e}")

    def _on_gallery_selection(self, selection):
        """相册回调"""
        if not selection:
            print("DEBUG [Home] 用户未选择")
            return

        src_path = selection[0]
        print(f"DEBUG [Home] 用户选择了: {src_path}")

        # 将图片复制到私有目录 (解决 Android 10+ 权限问题)
        saved_path = file_handler.save_selected_image(src_path)
        if saved_path:
            self._on_image_ready(saved_path)
        else:
            print("DEBUG [Home] 图片复制失败")

    # --- 通用跳转逻辑 ---
    def _on_image_ready(self, file_path):
        """无论拍照还是选图，最终都走这里跳转"""
        if not file_path:
            print("DEBUG [Home] 获取图片失败")
            return

        print(f"DEBUG [Home] 图片准备就绪，跳转结果页: {file_path}")
        self.manager.get_screen('result').set_image(file_path)
        self.manager.current = 'result'

    def go_history(self, instance):
        # 切换前刷新列表
        self.manager.get_screen('history').load_data()
        self.manager.current = 'history'