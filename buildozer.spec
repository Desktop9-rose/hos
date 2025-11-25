[app]

# (str) Title of your application
title = 医疗解读助手

# (str) Package name
package.name = medical_helper

# (str) Package domain (needed for android/ios packaging)
package.domain = org.elderly

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# -------------------------------------------------------------------------
# 🏆 终极修正依赖列表
# 1. 移除 'pillow'：导致编译失败的罪魁祸首 (代码已适配无Pillow模式)
# 2. 移除 'sqlite3'：安卓 Python 环境内置，无需声明
# 3. 保留 'requests'：用于百度云/AI 接口
# 4. 保留 KivyMD 2.0 及其隐形依赖
# -------------------------------------------------------------------------
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,plyer,android,jnius,requests

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #FFFFFF

# (list) Permissions
# Android 13 适配
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# -------------------------------------------------------------------------
# 🛠️ 构建工具链锁定 (参考成功案例)
# -------------------------------------------------------------------------
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support (KivyMD 2.0 必需)
android.enable_androidx = True

# (list) Gradle dependencies to add
android.gradle_dependencies = androidx.core:core:1.6.0

# (str) Android add resources
android.add_resources = res

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2
warn_on_root = 1