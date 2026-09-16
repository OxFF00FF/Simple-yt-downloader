@echo off
chcp 65001 >nul

:: Созданин ярлыка
set "PARSER_NAME=Youtube Video Downloader"
set "shortcutPath=%cd%\%PARSER_NAME%.lnk"
set "targetPath=%cd%\1. START_WT.bat"
set "iconPath=%cd%\icons\Icon.ico"
set "workingDir=%cd%"

powershell -Command ^
    "$ws = New-Object -ComObject WScript.Shell; " ^
    "$s = $ws.CreateShortcut('%shortcutPath%'); " ^
    "$s.TargetPath = '%targetPath%'; " ^
    "$s.IconLocation = '%iconPath%'; " ^
    "$s.WorkingDirectory = '%workingDir%'; " ^
    "$s.Save()"

if not exist "%shortcutPath%" (
    echo ✔️  Shortcut crated
    echo.
)

:: Открытие Windows терминала
if not defined WT_SESSION (
    wt.exe -p "Command Prompt" cmd /k "%~f0"
    exit /b
)

:: Установка папок
set "SCRIPT_DIR=%~dp0"
set "DIST_DIR=%SCRIPT_DIR%.wheels"

:: Проверка что зависимости уже установлены
if exist "%SCRIPT_DIR%.venv" (
    echo ✔️  Required dependencies already installed
    echo.
    pause
    exit
)

echo 📂  Current Location:  %cd%
echo 📂  Script Location:   %SCRIPT_DIR%
echo 📂  Wheels Location:   %DIST_DIR%
echo.

:: Поиск python 3.10
echo 🎛   Checking python availability in system . . .
echo.

:: Установленные версии python
echo 🐍  Installed Python versions:
py -0p
echo.

:: Проверка есть ли в системе python 3.10
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo ❌  Python 3.10 is NOT installed.
    echo 👉  Please install Python 3.10 from https://www.python.org/downloads/release/python-3100/
    pause
    exit /b 1
)
echo ✔️  Python 3.10 found

:: Python 3.10 exe
for /f "delims=" %%P in ('py -3.10 -c "import sys; print(sys.executable)"') do set "PY310_EXE=%%P"

:: Python 3.10 папка
for /f "delims=" %%D in ('py -3.10 -c "import sys; print(sys.base_prefix)"') do set "PY310_ROOT=%%D"

:: Scripts папка
set "PY310_SCRIPTS=%PY310_ROOT%\Scripts"

echo  - %PY310_ROOT%
echo  - %PY310_SCRIPTS%
echo.

:: Создание виртуального окружения
if not exist "%SCRIPT_DIR%.venv" (
    echo 🔄  Creating virtual environment . . .
    py -3.10 -m venv "%SCRIPT_DIR%.venv"
    echo ✔️  Virtual environment created
) else (
    echo ✔️  Virtual environment already exists
)
echo.

:: Активация виртуального окружения
echo 🔄  Activating virtual environment . . .
call "%SCRIPT_DIR%.venv\Scripts\activate"
echo ✔️  Virtual environment activated
for /f "delims=" %%i in ('python -c "import site; print(site.getsitepackages()[0])"') do echo 📂  Venv Location: %%i
echo.

if exist "%SCRIPT_DIR%requirements.txt" (
    echo 🔄  Installing from requirements.txt . . .
    pip install -r "%SCRIPT_DIR%requirements.txt"
    echo ✔️  Required dependencies installed
    echo.
    exit /b 0
)