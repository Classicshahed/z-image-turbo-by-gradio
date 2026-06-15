@echo off
setlocal EnableDelayedExpansion

title Setup and Run Z-Image
echo ==============================================
echo Z-Image Automatic Setup and Run Script
echo ==============================================

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 2. Create Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: 3. Activate Virtual Environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: 4. Install Dependencies
echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: 5. Create Model Directories
echo [INFO] Ensuring directories exist...
if not exist "models\zimage" mkdir "models\zimage"
if not exist "models\llm" mkdir "models\llm"
if not exist "models\vae" mkdir "models\vae"
if not exist "loras" mkdir "loras"
if not exist "outputs" mkdir "outputs"

:: 6. Check for Models (Manual Download)
echo [INFO] Checking for required models...
set "MISSING_MODELS=0"

set "ZIMAGE_MODEL=models\zimage\z_image_turbo_Q6_K.gguf"
if not exist "%ZIMAGE_MODEL%" (
    echo [WARNING] Missing Z-Image model. Please download and place it at: %ZIMAGE_MODEL%
    set "MISSING_MODELS=1"
)

set "LLM_MODEL=models\llm\Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
if not exist "%LLM_MODEL%" (
    echo [WARNING] Missing LLM model. Please download and place it at: %LLM_MODEL%
    set "MISSING_MODELS=1"
)

set "VAE_MODEL=models\vae\ae.safetensors"
if not exist "%VAE_MODEL%" (
    echo [WARNING] Missing VAE model. Please download and place it at: %VAE_MODEL%
    set "MISSING_MODELS=1"
)

if "!MISSING_MODELS!"=="1" (
    echo.
    echo [ERROR] One or more required models are missing.
    echo Please download them manually and place them in the specified directories.
    pause
    exit /b 1
)

:: 7. Run Application
echo.
echo [INFO] Setup complete! Starting the application...
python app.py

pause
