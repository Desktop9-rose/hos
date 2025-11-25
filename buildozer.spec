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
version = 1.0.4

# (list) Application requirements
# -------------------------------------------------------------------------
# 🏆 优化后的依赖列表
# 1. 新增 'openssl'：确保 requests 能正常处理 HTTPS (百度云 API 需要)
# 2. 移除 'pillow'：防止闪退
# 3. 保留 KivyMD 2.0 全家桶
# -------------------------------------------------------------------------
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,plyer,android,jnius,requests,openssl

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
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# -------------------------------------------------------------------------
# 🛠️ 构建工具链锁定 (最稳健组合)
# -------------------------------------------------------------------------
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True

# -------------------------------------------------------------------------
# ⚡️ 提速关键：只构建 arm64-v8a
# 现在的安卓手机(小米/华为等)都支持 64 位，没必要构建 v7a，这能节省 50% 时间并防止空间不足
# -------------------------------------------------------------------------
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Gradle dependencies to add
android.gradle_dependencies = androidx.core:core:1.6.0

# (str) Android add resources
android.add_resources = res

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]

# -------------------------------------------------------------------------
# 📉 降噪关键：设置为 1 (Info)
# 防止日志过大被 GitHub 截断，从而看不到真正的报错
# -------------------------------------------------------------------------
log_level = 1

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1