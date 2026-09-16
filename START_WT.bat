@echo off

call ".venv\Scripts\activate.bat" && python main.py

taskkill /IM cmd.exe /F

pause