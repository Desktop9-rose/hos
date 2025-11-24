from kivy.utils import platform


def check_permissions():
    """
    检查并申请必要的权限 (仅 Android 有效)
    """
    if platform == 'android':
        from android.permissions import request_permissions, Permission

        # 申请 相机、存储读写 权限
        request_permissions([
            Permission.CAMERA,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])