@echo off
title Z-Image Gradio Interface

echo Creating Python 3.10 Virtual Environment...
py -3.10 -m venv venv

echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting the application...
python app.py

pause
