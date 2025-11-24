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
source.include_exts = py,png,jpg,kv,atlas,otf,ttf

# (list) Application requirements
# 关键依赖：kivy, kivymd, pillow (图片), plyer (相册/TTS), sqlite3
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3,plyer,android,jnius

# (str) Icon of the application (这里先注释掉，如果你有 icon.png 可以解开)
# icon.filename = %(source.dir)s/assets/icon.png

# (list) Permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO

# (int) Target Android API
android.api = 33
android.minapi = 21

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #FFFFFF

# (list) Services to declare
# android.services =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1