from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.scatterlayout import ScatterLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivy.clock import Clock
from kivy.metrics import dp
import os
from datetime import datetime

from ui.components import ElderButton, ElderLabel
from utils.file_handler import file_handler


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'camera'
        self.camera_obj = None
        self.scatter_wrapper = None
        self.build_ui()

    def build_ui(self):
        # 主布局
        self.layout = MDBoxLayout(orientation='vertical', md_bg_color=(0, 0, 0, 1))

        # 1. 顶部提示
        self.header = ElderLabel(
            text="请将报告对准屏幕",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height="60dp"
        )
        self.layout.add_widget(self.header)

        # 2. 相机容器 (使用 RelativeLayout 确保居中)
        from kivy.uix.relativelayout import RelativeLayout
        self.cam_container = RelativeLayout(size_hint_y=1)
        self.layout.add_widget(self.cam_container)

        # 3. 底部按钮区
        action_bar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="100dp",
            padding="20dp",
            spacing="20dp",
            md_bg_color=(0.1, 0.1, 0.1, 1)
        )

        btn_back = ElderButton(text="取消")
        btn_back.bind(on_release=self.go_back)

        btn_snap = ElderButton(text="📷 拍照")
        btn_snap.md_bg_color = (0.2, 0.8, 0.2, 1)  # 绿色按钮
        btn_snap.bind(on_release=self.capture)

        btn_rotate = ElderButton(text="🔄 旋转")
        btn_rotate.bind(on_release=self.rotate_camera)

        action_bar.add_widget(btn_back)
        action_bar.add_widget(btn_snap)
        action_bar.add_widget(btn_rotate)

        self.layout.add_widget(action_bar)
        self.add_widget(self.layout)

    def on_enter(self):
        """进入页面时初始化相机"""
        self.init_camera()

    def on_leave(self):
        """离开页面时销毁相机（释放资源）"""
        self.stop_camera()

    def init_camera(self):
        try:
            self.cam_container.clear_widgets()

            # 核心逻辑：ScatterLayout 包裹 Camera
            self.scatter_wrapper = ScatterLayout(
                do_translation=False,
                do_rotation=False,
                do_scale=False,
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )

            # 初始化相机 (index=0 通常是后置)
            self.camera_obj = Camera(index=0, resolution=(640, 480), play=True)
            self.camera_obj.allow_stretch = True
            self.camera_obj.keep_ratio = False  # 充满屏幕

            self.scatter_wrapper.add_widget(self.camera_obj)
            self.cam_container.add_widget(self.scatter_wrapper)

            # 默认旋转 270度 (根据你的参考代码)
            self.scatter_wrapper.rotation = 270

        except Exception as e:
            self.header.text = f"相机启动失败: {str(e)}"

    def stop_camera(self):
        if self.camera_obj:
            self.camera_obj.play = False
            self.camera_obj = None
            self.cam_container.clear_widgets()

    def rotate_camera(self, instance):
        if self.scatter_wrapper:
            self.scatter_wrapper.rotation += 90
            self.header.text = f"当前角度: {int(self.scatter_wrapper.rotation)}°"

    def capture(self, instance):
        if not self.scatter_wrapper: return

        self.header.text = "正在保存..."
        try:
            # 生成文件名
            filename = datetime.now().strftime("IMG_%Y%m%d_%H%M%S.png")
            save_path = os.path.join(file_handler.app_dir, filename)

            # 核心逻辑：截图保存 (所见即所得)
            self.scatter_wrapper.export_to_png(save_path)

            if os.path.exists(save_path):
                print(f"DEBUG [Camera] 拍照保存成功: {save_path}")
                # 跳转到结果页
                self.manager.get_screen('result').set_image(save_path)
                self.manager.current = 'result'
            else:
                self.header.text = "保存失败，请重试"

        except Exception as e:
            print(f"Capture Error: {e}")
            self.header.text = "拍照出错"

    def go_back(self, instance):
        self.manager.current = 'home'