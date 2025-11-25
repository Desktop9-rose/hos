[app]
title = 医疗解读助手
package.name = medical_helper
package.domain = org.elderly
source.dir = .
# 包含 py, png, jpg, kv, atlas, otf, ttf, ini, xml
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml

version = 1.0.0

# 依赖列表 (保持 KivyMD 2.0 和 requests)
requirements = python3,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,pillow,sqlite3,plyer,android,jnius,requests

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

# 强制竖屏
orientation = portrait

fullscreen = 0
android.presplash_color = #FFFFFF

# 权限 (Android 13 适配)
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# API 设置 (参考成功案例，保持 API 33)
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# 资源路径 (虽然不用 FileProvider 了，但保留 res 也没坏处，防止误删其他资源)
android.add_resources = res

# ⚠️ 移除 android.manifest_provider 和 android.gradle_dependencies
# 因为我们不再需要与外部相机交互，内置相机不需要这些复杂的 Provider 配置

[buildozer]
log_level = 2
warn_on_root = 1