from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivy.utils import platform
from plyer import filechooser

from ui.components import ElderButton, ElderLabel
from utils.file_handler import file_handler
from privacy.permission import check_permissions


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.build_ui()
        # 启动时尝试申请权限
        check_permissions()

    def build_ui(self):
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[40, 60, 40, 40],
            spacing=40,
            md_bg_color=(0.96, 0.96, 0.96, 1)
        )

        title = ElderLabel(
            text="医疗报告解读助手",
            halign="center",
            size_hint_y=None,
            height="100dp",
            font_style="Headline",
            role="medium"
        )

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

    def go_camera(self, instance):
        """
        拍照功能
        注：在PC上我们用文件选择模拟，在Android上理想情况调用相机Intent。
        为了简化开发，这里统一先调文件选择器，
        后续阶段我们可以集成 Kivy Camera 组件。
        """
        print("启动相机逻辑...")
        if platform == 'android':
            # 安卓端通常调用原生相机比较复杂，暂时复用选图，
            # 或者后续集成专用 Camera Screen
            self.open_file_chooser()
        else:
            self.open_file_chooser()

    def go_gallery(self, instance):
        print("启动相册逻辑...")
        self.open_file_chooser()

    def go_history(self, instance):
        if self.manager:
            self.manager.current = 'history'

    def open_file_chooser(self):
        """调用 plyer 选择文件"""
        # 注意：on_selection 是一个回调函数
        filechooser.open_file(on_selection=self._on_file_selected, filters=[("Images", "*.jpg", "*.jpeg", "*.png")])

    def _on_file_selected(self, selection):
        """文件选择回调"""
        if selection and len(selection) > 0:
            file_path = selection[0]
            print(f"用户选择了图片: {file_path}")

            # 1. 保存图片到私有目录
            saved_path = file_handler.save_selected_image(file_path)

            if saved_path:
                # 2. 跳转到结果页进行处理 (传递图片路径)
                self.switch_to_result(saved_path)
            else:
                print("图片保存失败")

    def switch_to_result(self, image_path):
        if self.manager:
            # 获取 ResultScreen 实例并传递数据
            result_screen = self.manager.get_screen('result')
            result_screen.set_image(image_path)
            self.manager.current = 'result'