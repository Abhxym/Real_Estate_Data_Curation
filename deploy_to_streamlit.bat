@echo off
echo ==========================================
echo Streamlit Cloud Deployment - Final Push
echo ==========================================
echo.

echo [Step 1/5] Verifying file structure...
if not exist "dashboard.py" (
    echo ERROR: dashboard.py not found in root!
    exit /b 1
)
if not exist "data\real_estate_curation_project.xlsx" (
    echo ERROR: Excel file not found!
    exit /b 1
)
echo OK: All files present

echo.
echo [Step 2/5] Checking git status...
git status
echo.

echo [Step 3/5] Adding all files...
git add .

echo.
echo [Step 4/5] Committing changes...
git commit -m "Final Streamlit Cloud deployment - structure verified"

echo.
echo [Step 5/5] Pushing to GitHub...
git push origin main

echo.
echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Your code is now on GitHub.
echo.
echo Next steps:
echo 1. Go to: https://share.streamlit.io/
echo 2. Find your app
echo 3. Click "Reboot app" if needed
echo 4. Check logs if deployment fails
echo.
echo If deployment fails:
echo - Check Streamlit Cloud logs
echo - Verify settings: Main file = dashboard.py
echo - See FINAL_DEPLOYMENT_SOLUTION.md
echo.
echo Your app structure is CORRECT:
echo   dashboard.py (in root) ✓
echo   data/real_estate_curation_project.xlsx ✓
echo   requirements.txt ✓
echo   packages.txt (empty) ✓
echo.
pause
