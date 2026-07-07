@echo off
echo ========================================
echo   Data Warehouse Dashboard Launcher
echo ========================================
echo.

echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly numpy

echo.
echo Iniciando Dashboard...
python -m streamlit run "%~dp0dashboard_dw.py"

pause