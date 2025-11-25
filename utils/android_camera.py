from kivy.utils import platform
from kivy.clock import Clock
import os


class AndroidCamera:
    def __init__(self):
        self.callback = None
        self.temp_path = None

        if platform == 'android':
            from jnius import autoclass, cast
            from android import activity

            # 获取 Android 核心类
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.FileProvider = autoclass('androidx.core.content.FileProvider')
            self.File = autoclass('java.io.File')
            self.Intent = autoclass('android.content.Intent')
            self.MediaStore = autoclass('android.provider.MediaStore')
            self.Uri = autoclass('android.net.Uri')

            # 绑定回调监听 (当相机关闭时触发)
            activity.bind(on_activity_result=self._on_activity_result)

    def take_picture(self, filename, on_complete):
        """
        启动系统相机拍照
        :param filename: 图片保存的绝对路径
        :param on_complete: 拍照完成后的回调函数 func(path)
        """
        self.callback = on_complete
        self.temp_path = filename

        if platform == 'android':
            try:
                # 1. 准备文件对象
                photo_file = self.File(filename)

                # ⚠️ 2. 获取 Content URI (关键步骤)
                # authority 必须与 buildozer.spec 中的 android.manifest_provider 一致
                authority = "org.elderly.medical_helper.fileprovider"

                context = self.PythonActivity.mActivity
                photo_uri = self.FileProvider.getUriForFile(
                    context,
                    authority,
                    photo_file
                )

                # 3. 创建 Intent
                intent = self.Intent(self.MediaStore.ACTION_IMAGE_CAPTURE)
                intent.putExtra(self.MediaStore.EXTRA_OUTPUT, photo_uri)

                # 4. 授予权限 (允许相机应用写入这个 URI)
                intent.addFlags(self.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                intent.addFlags(self.Intent.FLAG_GRANT_WRITE_URI_PERMISSION)

                # 5. 启动相机
                self.PythonActivity.mActivity.startActivityForResult(intent, 0x123)
                print(f"📸 [Camera] 相机已启动，URI: {photo_uri.toString()}")

            except Exception as e:
                print(f"❌ [Camera] 启动失败: {e}")
                import traceback
                traceback.print_exc()
                # 如果失败，直接回调 None
                if self.callback:
                    self.callback(None)
        else:
            # 电脑端模拟：直接回调（或调用文件选择）
            print("💻 [Camera] 电脑端无法调用相机，请使用相册选择")
            if self.callback:
                self.callback(None)

    def _on_activity_result(self, request_code, result_code, intent):
        """相机返回后的回调 (Java 线程)"""
        if request_code == 0x123:
            # 必须切回 Kivy 主线程处理 UI
            Clock.schedule_once(lambda dt: self._process_result(result_code), 0)

    def _process_result(self, result_code):
        """处理结果 (主线程)"""
        # Result Code -1 代表 OK (Activity.RESULT_OK)
        if result_code == -1:
            print(f"✅ [Camera] 拍照成功，保存至: {self.temp_path}")
            if self.callback and os.path.exists(self.temp_path):
                self.callback(self.temp_path)
            else:
                print("⚠️ [Camera] 文件未生成")
                if self.callback: self.callback(None)
        else:
            print("🚫 [Camera] 用户取消了拍照")
            if self.callback: self.callback(None)


# 单例
android_camera = AndroidCamera()