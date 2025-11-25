[app]
title = 医疗解读助手
package.name = medical_helper
package.domain = org.elderly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml
version = 1.0.8

# -------------------------------------------------------------------------
# 🏆 黄金稳定版依赖 (The Golden Stable Combo)
# 1. kivy==2.2.1 (最稳定的 Kivy 版本)
# 2. kivymd==1.1.1 (最稳定的 UI 版本，不需要 github 链接)
# 3. 移除了 materialyoucolor, asynckivy, asyncgui (这些是 2.0 的垃圾依赖)
# 4. 移除了 pillow (防止闪退)
# 5. 移除了 openssl/requests (防止编译失败，使用 UrlRequest)
# -------------------------------------------------------------------------
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,android,jnius,libffi

# 暂时注释掉图标，防止因为文件缺失导致打包最后一步报错
# presplash.filename = %(source.dir)s/assets/presplash.png
# icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# 权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# API 设置 (Android 13)
android.api = 33
android.minapi = 21
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# AndroidX (KivyMD 1.1.1 也建议开启)
android.enable_androidx = True
# 基础依赖
android.gradle_dependencies = androidx.core:core:1.6.0
android.add_resources = res
android.entrypoint = org.kivy.android.PythonActivity

# P4A 配置
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1