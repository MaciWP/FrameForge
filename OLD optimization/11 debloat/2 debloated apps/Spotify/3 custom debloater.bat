@echo off
set "SPOTIFY_PATH=%USERPROFILE%\AppData\Roaming\Spotify"

del "%SPOTIFY_PATH%\chrome_100_percent.pak"
del "%SPOTIFY_PATH%\chrome_200_percent.pak"
del "%SPOTIFY_PATH%\crash_reporter.cfg"
del "%SPOTIFY_PATH%\d3dcompiler_47.dll"
del "%SPOTIFY_PATH%\Apps\xpui.bak"
del "%SPOTIFY_PATH%\Apps\login.spa"
del "%SPOTIFY_PATH%\libcef.dll.sig"
del "%SPOTIFY_PATH%\libEGL.dll"
del "%SPOTIFY_PATH%\libGLESv2.dll"
del "%SPOTIFY_PATH%\Spotify.exe.sig"
del "%SPOTIFY_PATH%\Spotify.bak"
del "%SPOTIFY_PATH%\vk_swiftshader.dll"
del "%SPOTIFY_PATH%\vk_swiftshader_icd.json"
del "%SPOTIFY_PATH%\vulkan-1.dll"
echo Deletion completed.
pause
