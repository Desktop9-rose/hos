[app]
title = 医疗解读助手
package.name = medical_helper
package.domain = org.elderly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml
version = 1.0.0

# -------------------------------------------------------------------------
# 🏆 绝对纯净的依赖列表 (Pure Python Strategy)
# 1. 移除了所有 C 语言重库 (pillow, openssl, requests) -> 杜绝编译报错
# 2. 只保留 UI 库 (KivyMD 2.0) 和 系统接口 (plyer, android, jnius)
# -------------------------------------------------------------------------
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,plyer,android,jnius

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png
orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# 权限 (保持不变)
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# API 设置 (锁定稳健版本)
android.api = 33
android.minapi = 21
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# AndroidX (KivyMD 2.0 必需)
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.6.0
android.add_resources = res
android.entrypoint = org.kivy.android.PythonActivity

# 修复 NDK 编译问题
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1