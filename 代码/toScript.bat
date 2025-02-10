@echo off
setlocal enabledelayedexpansion

:: 定义文件夹路径
set "input_dir=rpy"
set "json_dir=trans_json"
set "output_dir=trans_rpy"

:: 如果 trans_rpy 文件夹不存在，创建它
if not exist "%output_dir%" (
    mkdir "%output_dir%"
)

:: 遍历 rpy 文件夹中的所有 .rpy 文件
for %%f in (%input_dir%\*.rpy) do (
    set "input_file=%%f"
    set "json_file=%json_dir%\%%~nf.json"
    set "output_file=%output_dir%\%%~nf.rpy"
    
    :: 检查对应的 json 文件是否存在
    if exist "!json_file!" (
        echo Processing %%f with %%~nf.json...
        python toScript.py "!input_file!" "!json_file!" "!output_file!"
    ) else (
        echo Warning: Corresponding JSON file for %%f not found.
    )
)

echo All files have been processed.
pause
