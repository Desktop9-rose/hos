import os
import shutil
from datetime import datetime
from kivy.utils import platform


class FileHandler:
    def __init__(self):
        self.app_dir = self._get_app_dir()
        # 创建图片存储子目录
        self.images_dir = os.path.join(self.app_dir, 'report_images')
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

    def _get_app_dir(self):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity
            # 获取 APP 私有文件目录: /data/user/0/xxx/files/
            return context.getExternalFilesDir(None).getAbsolutePath()
        else:
            # PC 端
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, 'app_data_storage')
            if not os.path.exists(data_dir): os.makedirs(data_dir)
            return data_dir

    def save_selected_image(self, source_path):
        """
        将用户选择的图片复制到私有目录，并重命名
        返回：新路径
        """
        try:
            # 生成唯一文件名: 20251124_102030.jpg
            filename = datetime.now().strftime("REPORT_%Y%m%d_%H%M%S.jpg")
            target_path = os.path.join(self.images_dir, filename)

            # 复制文件
            shutil.copy(source_path, target_path)
            return target_path
        except Exception as e:
            print(f"保存图片失败: {e}")
            return None


file_handler = FileHandler()