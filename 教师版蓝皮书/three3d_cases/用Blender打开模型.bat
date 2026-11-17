@echo off
setlocal enabledelayedexpansion
title Blender 3D 模型浏览器

set "BLENDER=D:\Program\blender-portable\blender-5.2.1-windows-x64\blender.exe"
set "SCRIPT=%~dp0_open_glb.py"

if not exist "%BLENDER%" goto :noblender
if not exist "%SCRIPT%" goto :noscript

if not "%~1"=="" goto :dropfile

echo.
echo  ============================================================
echo     Blender 3D 模型浏览器
echo  ============================================================
echo.
echo   可用模型：
echo.

set n=0
for /r "%~dp0" %%F in (*.glb) do (
    set /a n+=1
    set "f!n!=%%F"
    for %%D in ("%%~dpF.") do echo    !n! .  %%~nxF    [%%~nxD]
)

if %n%==0 goto :noflie

echo.
echo  ------------------------------------------------------------
echo   输入编号后回车，用 Blender 打开对应模型。
echo   （会自动清空默认场景、导入模型、摆好相机和灯光）
echo   直接关掉本窗口则取消。
echo  ------------------------------------------------------------
set "pick="
set /p pick=   编号: 

if not defined pick goto :badpick
call set "target=%%f%pick%%%"
if not defined target goto :badpick

echo.
echo   正在打开：%target%
echo.
start "" "%BLENDER%" --python "%SCRIPT%" -- "%target%"
exit /b 0


:dropfile
echo.
echo   正在用 Blender 打开：%~nx1
echo   （会自动清空默认场景、导入模型、摆好相机和灯光）
echo.
start "" "%BLENDER%" --python "%SCRIPT%" -- %*
exit /b 0


:noblender
echo.
echo   [X] 找不到 Blender：
echo       %BLENDER%
echo   请确认便携版解压位置，或修改本文件里的 BLENDER 路径。
echo.
pause
exit /b 1

:noscript
echo.
echo   [X] 找不到 _open_glb.py，请确认它和本文件在同一个文件夹里。
echo.
pause
exit /b 1

:noflie
echo   （这个文件夹里没有找到 .glb 文件）
echo.
pause
exit /b 1

:badpick
echo.
echo   [X] 编号无效，请重新运行本文件。
echo.
pause
exit /b 1
