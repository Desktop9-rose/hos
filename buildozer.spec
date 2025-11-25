[app]
title = 医疗解读助手
package.name = medical_helper
package.domain = org.elderly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml
version = 1.0.0

# -------------------------------------------------------------------------
# 🏆 依赖列表 (保持纯净版)
# -------------------------------------------------------------------------
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,plyer,android,jnius,libffi

# -------------------------------------------------------------------------
# ⚠️ 关键修复：注释掉自定义图标
# 因为你的仓库里可能缺少这两个文件，导致打包最后一步失败。
# 注释后将使用 Kivy 默认图标，保证构建成功。
# -------------------------------------------------------------------------
# presplash.filename = %(source.dir)s/assets/presplash.png
# icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# 权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# API 设置
android.api = 33
android.minapi = 21
android.build_tools_version = 34.0.0
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# AndroidX
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.6.0
android.add_resources = res
android.entrypoint = org.kivy.android.PythonActivity

# p4a 设置
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1