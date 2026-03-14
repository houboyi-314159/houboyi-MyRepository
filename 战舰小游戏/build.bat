@echo off
chcp 65001 >nul
setlocal
cd /d D:\eclipse\eclipse\workspace\project_\_客户项目\01
D:\eclipse\eclipse\workspace\venv_\flask_venv\Scripts\pyinstaller.exe --onefile --add-data "templates;templates" app.py
if exist build rmdir /s /q build
echo
echo ========================================
echo 打包完成！exe 在 dist\app.exe
echo ========================================
pause
endlocal