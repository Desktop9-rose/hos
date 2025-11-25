import os
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from kivy.clock import Clock
from plyer import filechooser

from ui.components import ElderButton, ElderLabel
from utils.file_handler import file_handler
from privacy.permission import check_permissions


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.build_ui()

        # 启动时延迟申请权限 (Android 13 适配)
        Clock.schedule_once(lambda dt: check_permissions(), 1)

    def build_ui(self):
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[40, 60, 40, 40],
            spacing=40,
            md_bg_color=(0.96, 0.96, 0.96, 1)
        )

        # 标题
        title = ElderLabel(
            text="医疗报告解读助手",
            halign="center",
            size_hint_y=None,
            height="100dp",
            font_style="Headline",
            role="medium"
        )

        # 三大核心功能按钮
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

        # 底部弹簧占位
        layout.add_widget(MDWidget(size_hint_y=1))

        self.add_widget(layout)

    # --- 📸 拍照逻辑 (新) ---
    def go_camera(self, instance):
        """
        点击拍照：跳转到 APP 内置的相机页面
        不再调用容易崩溃的系统外部相机
        """
        print("DEBUG [Home] 跳转到内置相机页面")
        self.manager.current = 'camera'

    # --- 🖼️ 相册逻辑 ---
    def go_gallery(self, instance):
        """点击相册：调用系统文件选择器"""
        print("DEBUG [Home] 打开相册选择器")
        try:
            filechooser.open_file(
                on_selection=self._on_gallery_selection,
                filters=[("Images", "*.jpg", "*.jpeg", "*.png")]
            )
        except Exception as e:
            print(f"DEBUG [Home] 打开相册异常: {e}")

    def _on_gallery_selection(self, selection):
        """文件选择回调"""
        if not selection:
            print("DEBUG [Home] 用户取消选择或无权限")
            return

        src_path = selection[0]
        print(f"DEBUG [Home] 用户选择了: {src_path}")

        # 将图片复制到 APP 私有目录 (解决 Android 10+ 权限问题)
        try:
            saved_path = file_handler.save_selected_image(src_path)
            if saved_path:
                # 必须在主线程执行跳转
                Clock.schedule_once(lambda dt: self._switch_to_result(saved_path), 0)
            else:
                print("DEBUG [Home] 图片复制/保存失败")
        except Exception as e:
            print(f"DEBUG [Home] 处理图片异常: {e}")

    # --- 通用逻辑 ---
    def _switch_to_result(self, path):
        """跳转到结果页并开始处理"""
        print(f"DEBUG [Home] 准备处理图片: {path}")
        # 获取结果页屏幕对象
        result_screen = self.manager.get_screen('result')
        # 传递图片路径
        result_screen.set_image(path)
        # 切换屏幕
        self.manager.current = 'result'

    def go_history(self, instance):
        """跳转到历史记录页"""
        # 切换前刷新列表数据
        history_screen = self.manager.get_screen('history')
        if hasattr(history_screen, 'load_data'):
            history_screen.load_data()
        self.manager.current = 'history'