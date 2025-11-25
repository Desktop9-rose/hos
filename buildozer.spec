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
# 关键修正：添加 ini 以便打包 config.ini，添加 xml 以便打包资源
source.include_exts = py,png,jpg,kv,atlas,otf,ttf,ini,xml

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
# 关键修正：
# 1. 新增 requests (用于调用云端 OCR/AI 接口)
# 2. 保留 KivyMD 2.0 全套依赖 (materialyoucolor, asynckivy, asyncgui)
requirements = python3,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,pillow,sqlite3,plyer,android,jnius,requests

# (str) Custom source folders for requirements
# requirements.source.kivymd = ../../kivymd

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# Android Specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #FFFFFF

# (list) Permissions
# 关键修正：包含 Android 13 媒体权限 和 网络权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,RECORD_AUDIO,READ_MEDIA_IMAGES

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 20

# (str) Android NDK version to use
# android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to exclude from the result.iles
# android.gradle_dependencies =

# (bool) Turn on the gradle build report
# android.gradle_build_report = False

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# android.add_jars = foo.jar,bar.jar

# (list) List of Java files to add to the android project
# android.add_src =

# (list) Android AAR archives to add
# android.add_aars =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (list) Java classes to add as activities to the manifest.
# android.add_activities = com.example.ExampleActivity

# (list) Java classes to add as services to the manifest.
# android.add_services = com.example.ExampleService

# (list) Java classes to add as receivers to the manifest.
# android.add_receivers = com.example.ExampleReceiver

# (list) Java classes to add as providers to the manifest.
# android.add_providers = com.example.ExampleProvider

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# android.manifest_placeholders = [:]

# (bool) disables the compilation of py to pyc/pyo (True = no compilation)
# android.no-compile-pyo = False

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

# -------------------------------------------------------------------------
# 关键修正 A：添加资源路径
# 将本地 res 目录打包进 APK，供 AndroidManifest 使用
# -------------------------------------------------------------------------
android.add_resources = res

# -------------------------------------------------------------------------
# 关键修正 B：注册 FileProvider
# 解决 Android 7.0+ 相机调用崩溃问题 (FileUriExposedException)
# authorities 必须匹配 package.domain + . + package.name + .fileprovider
# -------------------------------------------------------------------------
android.manifest_provider = <provider android:name="androidx.core.content.FileProvider" android:authorities="org.elderly.medical_helper.fileprovider" android:exported="false" android:grantUriPermissions="true"><meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/provider_paths" /></provider>


#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android local directory to use instead of git revision
# p4a.local_dir =

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port =


#
# iOS Specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output storage, absolute or relative to spec file
# bin_dir = ./bin