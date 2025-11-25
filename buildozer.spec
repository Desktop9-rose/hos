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
# 包含配置文件和资源
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml

# (str) Application versioning (method 1)
version = 1.0.3

# (list) Application requirements
# 融合策略：
# 1. Kivy 2.2.1 (稳定基石)
# 2. KivyMD 2.0 + 全套隐形依赖 (materialyoucolor, asynckivy, asyncgui)
# 3. requests (云端能力)
# 4. pillow (虽然之前说移除，但既然成功案例用了NDK 25b，Pillow其实是可以兼容的，加上防万一)
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,pillow,sqlite3,plyer,android,jnius,requests

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
# 🏆 核心“抄作业”配置：锁定构建工具链版本
# 这能解决 90% 的莫名其妙构建失败问题
# -------------------------------------------------------------------------
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support. (KivyMD 2.0 必须)
android.enable_androidx = True

# (list) Gradle dependencies to add (确保 FileProvider 类存在)
android.gradle_dependencies = androidx.core:core:1.6.0

# (str) Android add resources (映射 XML 配置)
android.add_resources = res

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1