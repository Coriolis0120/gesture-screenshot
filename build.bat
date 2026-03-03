@echo off
chcp 65001 >nul
echo ========================================
echo  Gesture Screenshot - Build EXE
echo ========================================
echo.

REM 清理旧的构建文件
echo [0/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GestureScreenshot.spec del /q GestureScreenshot.spec
echo Cleaned.
echo.

REM 安装依赖
echo [1/3] Installing dependencies...
pip install -r requirements.txt
echo.

REM 打包（包含所有依赖）
echo [2/3] Building executable...
pyinstaller --onefile --windowed ^
    --name "GestureScreenshot" ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --hidden-import gesture_detector ^
    --hidden-import logger ^
    --hidden-import screenshot ^
    --hidden-import ui_overlay ^
    --hidden-import mediapipe ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import google.protobuf ^
    --hidden-import google.protobuf.descriptor ^
    --hidden-import PIL ^
    --hidden-import pyautogui ^
    --collect-all mediapipe ^
    --collect-all cv2 ^
    src\main.py
echo.

if exist dist\GestureScreenshot.exe (
    echo ========================================
    echo [3/3] Build successful!
    echo  Output: dist\GestureScreenshot.exe
    echo ========================================
    echo.
    echo  You can copy GestureScreenshot.exe to any location.
) else (
    echo Build failed!
)

pause
