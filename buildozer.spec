[app]
title = 医疗解读助手
package.name = medical_helper
package.domain = org.elderly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml

version = 1.1.0

# 关键修正：
# 1. 降级 kivy==2.2.1 (配合 GitHub Actions 中的 cython<3，确保编译通过)
# 2. 移除 pillow (响应你的“成功代码包”经验，防止架构冲突闪退)
# 3. 保留 KivyMD 2.0 及其依赖
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,sqlite3,plyer,android,jnius,requests

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png
orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# 权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# API 设置 (保持 33)
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# 资源
android.add_resources = res

[buildozer]
log_level = 2
warn_on_root = 1