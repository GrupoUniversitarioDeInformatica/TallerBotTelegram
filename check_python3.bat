@echo off

python --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3 is not installed.
    set /p choice="Do you want to install Python 3? (y/n): "
    
    if /i "%choice%"=="y" (
        echo Please install Python 3 from the official website: https://www.python.org/
        exit /b 1
    ) else (
        echo Python 3 is not installed. Exiting...
        exit /b 1
    )
) else (
    echo Python 3 is installed.
)

:: Create directories
mkdir src/json/

echo Directories created successfully.
SET URL=https://pytba.readthedocs.io/en/latest/quick_start.html
start %URL%
exit /b 0

