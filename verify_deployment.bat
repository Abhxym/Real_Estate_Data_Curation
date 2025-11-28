@echo off
echo ==========================================
echo Streamlit Cloud Deployment Verification
echo ==========================================
echo.

echo Checking critical files...
echo.

echo [1/6] Checking dashboard.py...
if exist "dashboard.py" (
    echo    ✓ dashboard.py found
) else (
    echo    ✗ dashboard.py MISSING!
    goto error
)

echo [2/6] Checking data folder...
if exist "data" (
    echo    ✓ data folder found
) else (
    echo    ✗ data folder MISSING!
    goto error
)

echo [3/6] Checking Excel file...
if exist "data\real_estate_curation_project.xlsx" (
    echo    ✓ Excel file found
    for %%A in ("data\real_estate_curation_project.xlsx") do echo    Size: %%~zA bytes
) else (
    echo    ✗ Excel file MISSING!
    goto error
)

echo [4/6] Checking requirements.txt...
if exist "requirements.txt" (
    echo    ✓ requirements.txt found
    type requirements.txt
) else (
    echo    ✗ requirements.txt MISSING!
    goto error
)

echo [5/6] Checking packages.txt...
if exist "packages.txt" (
    echo    ✓ packages.txt found
    for /f %%i in ("packages.txt") do set size=%%~zi
    if %size%==0 (
        echo    ✓ packages.txt is empty (correct!)
    ) else (
        echo    ⚠ packages.txt is not empty
        type packages.txt
    )
) else (
    echo    ✗ packages.txt MISSING!
)

echo [6/6] Checking git status...
git status >nul 2>&1
if %errorlevel%==0 (
    echo    ✓ Git repository initialized
    echo.
    echo    Checking if files are tracked:
    git ls-files | findstr /C:"dashboard.py" >nul && echo       ✓ dashboard.py tracked || echo       ✗ dashboard.py NOT tracked
    git ls-files | findstr /C:"data/real_estate_curation_project.xlsx" >nul && echo       ✓ Excel file tracked || echo       ✗ Excel file NOT tracked
    git ls-files | findstr /C:"requirements.txt" >nul && echo       ✓ requirements.txt tracked || echo       ✗ requirements.txt NOT tracked
) else (
    echo    ⚠ Not a git repository
)

echo.
echo ==========================================
echo Testing local run...
echo ==========================================
echo.

echo Testing Python imports...
py -c "import streamlit, pandas, plotly, sklearn, statsmodels; print('✓ All imports successful')" 2>nul
if %errorlevel%==0 (
    echo ✓ All dependencies installed
) else (
    echo ✗ Some dependencies missing
    echo Run: py -m pip install -r requirements.txt
)

echo.
echo ==========================================
echo Deployment Readiness Summary
echo ==========================================
echo.

echo ✓ All critical files present
echo ✓ File structure correct
echo.
echo Next steps:
echo 1. Ensure all files are committed:
echo    git add .
echo    git commit -m "Ready for Streamlit Cloud"
echo.
echo 2. Push to GitHub:
echo    git push origin main
echo.
echo 3. Deploy on Streamlit Cloud:
echo    https://share.streamlit.io/
echo.
echo 4. If deployment fails, check logs and see:
echo    STREAMLIT_DEPLOYMENT_FIX.md
echo.
goto end

:error
echo.
echo ==========================================
echo ✗ DEPLOYMENT NOT READY
echo ==========================================
echo.
echo Please fix the missing files above.
echo.

:end
pause
