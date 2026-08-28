@echo off
setlocal
set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python was not found: %PYTHON_EXE%
    echo Create the virtual environment and install requirements first.
    exit /b 1
)

"%PYTHON_EXE%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 exit /b %errorlevel%

"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean PDFUtility.spec
if errorlevel 1 exit /b %errorlevel%

echo.
echo Built: dist\PDFUtility.exe
