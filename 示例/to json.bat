@echo off
setlocal enabledelayedexpansion

:: 定义文件夹路径
set "input_dir=rpy"
set "output_dir=json"

:: 如果 json 文件夹不存在，创建它
if not exist "%output_dir%" (
    mkdir "%output_dir%"
)

:: 遍历 rpy 文件夹中的所有 .rpy 文件
for %%f in (%input_dir%\*.rpy) do (
    set "input_file=%%f"
    set "output_file=%output_dir%\%%~nf.json"
    
    :: 调用 parsejson.py 脚本
    echo Processing %%f...
    python parsejson.py "!input_file!" "!output_file!"
)

echo All files have been processed.
pause
