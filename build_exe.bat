@echo off
setlocal
set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
set "OUTPUT_EXE=%~dp0dist\Folimeld.exe"

if not exist "%PYTHON_EXE%" (
    echo Python was not found: %PYTHON_EXE%
    echo Create the virtual environment and install requirements first.
    exit /b 1
)

if exist "%OUTPUT_EXE%" (
    del /f /q "%OUTPUT_EXE%" 2>nul
    if exist "%OUTPUT_EXE%" (
        echo ERROR: dist\Folimeld.exe is in use and cannot be replaced.
        echo Close Folimeld and try the build again.
        exit /b 1
    )
)

"%PYTHON_EXE%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 exit /b %errorlevel%

"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean Folimeld.spec
if errorlevel 1 exit /b %errorlevel%

echo.
echo Built: dist\Folimeld.exe
