@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
echo ========================================
echo    B站账号清理工具 - 单文件版本
echo ========================================
echo.
echo 提示：双击 run.bat 自动进入交互菜单
echo 提示：运行 python bilibili_cleaner_onefile.py --auto 可直接执行全部清理
echo.
echo 正在启动...
call venv\Scripts\activate.bat
python bilibili_cleaner_onefile.py --config config/config.yaml
echo.
echo 程序执行完毕！
pause
