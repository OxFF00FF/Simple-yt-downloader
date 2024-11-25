@echo off

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    
    echo Activating virtual environment...
    call venv\Scripts\activate
    echo.

    echo Installing dependencies...
    pip install -r requirements.txt
    echo.

    echo Required dependencies installed
    echo.
    echo.
)

set "shortcutPath=%cd%\Youtube Video Downloader.lnk"
set "targetPath=%cd%\Src\START_WT.bat"
set "iconPath=%cd%\Images\Icon.ico"
set "workingDir=%cd%\Src"

powershell "$ws = New-Object -COMObject WScript.Shell; $shortcut = $ws.CreateShortcut('%shortcutPath%'); $shortcut.TargetPath = '%targetPath%'; $shortcut.IconLocation = '%iconPath%'; $shortcut.WorkingDirectory = '%workingDir%'; $shortcut.Save()"