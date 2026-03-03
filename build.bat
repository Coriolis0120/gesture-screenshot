@echo off
chcp 65001 >nul
echo ========================================
echo  Gesture Screenshot - Build EXE
echo ========================================
echo.

REM 安装依赖
echo [1/2] Installing dependencies...
pip install -r requirements.txt
echo.

REM 打包（包含所有 src 模块）
echo [2/2] Building executable...
pyinstaller --onefile --windowed ^
    --name "GestureScreenshot" ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --add-data "src;src" ^
    --hidden-import gesture_detector ^
    --hidden-import logger ^
    --hidden-import screenshot ^
    --hidden-import ui_overlay ^
    src\main.py
echo.

if exist dist\GestureScreenshot.exe (
    echo ========================================
    echo  Build successful!
    echo  Output: dist\GestureScreenshot.exe
    echo ========================================
    echo.
    echo  You can copy GestureScreenshot.exe to any location.
) else (
    echo Build failed!
)

pause
