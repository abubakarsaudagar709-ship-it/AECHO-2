[app]
title = AECHO
package.name = aecho
package.domain = com.abubakarsaudagar

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1

requirements = python3,kivy,speechrecognition,pyaudio,plyer,requests,pygame

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

# Android permissions AECHO needs
android.permissions = INTERNET,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS

# Minimum/target Android API levels
android.minapi = 21
android.api = 33
android.ndk = 25b

# Architecture - covers most modern Android phones
android.archs = arm64-v8a,armeabi-v7a

# Keeps wake word listener alive when app isn't in foreground
# (actual service wiring will be added once wakeword.py needs it running in background)
android.allow_backup = 1

[buildozer]
log_level = 2
warn_on_root = 1
