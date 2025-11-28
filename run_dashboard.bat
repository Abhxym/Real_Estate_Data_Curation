@echo off
echo ========================================
echo Real Estate Analytics Dashboard
echo ========================================
echo.
echo Checking dependencies...
py -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Dependencies not installed!
    echo.
    echo Installing required packages...
    py -m pip install -r requirements.txt
    echo.
)
echo.
echo Starting dashboard...
echo.
echo The dashboard will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.
py -m streamlit run dashboard.py
pause
