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
version = 1.0.2

# (list) Application requirements
# 核心组合：
# 1. kivy==2.2.1 (稳定)
# 2. kivymd (master分支，2.0版本)
# 3. 移除了 pillow (防闪退)
# 4. 添加了 requests (云端API)
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,sqlite3,plyer,android,jnius,requests

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

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support.
# 【关键修正】KivyMD 2.0 必须开启此选项，否则构建失败
android.enable_androidx = True

# (list) Gradle dependencies to add
# 【关键修正】确保 AndroidX 核心库存在
android.gradle_dependencies = androidx.core:core:1.6.0

# (str) Android add resources
android.add_resources = res

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1