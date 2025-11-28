@echo off
echo ==========================================
echo Real Estate Dashboard Deployment Script
echo ==========================================
echo.

echo Select deployment option:
echo 1) Local deployment (test)
echo 2) Docker deployment
echo 3) Prepare for Streamlit Cloud
echo 4) Check deployment readiness
echo 5) Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto streamlit
if "%choice%"=="4" goto check
if "%choice%"=="5" goto exit
goto invalid

:local
echo.
echo Starting local deployment...
py -m pip install -r requirements.txt
echo.
echo Testing models...
py test_models.py
echo.
echo Starting dashboard...
py -m streamlit run dashboard.py
goto end

:docker
echo.
echo Docker deployment...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    goto end
)

echo Building Docker image...
docker build -t real-estate-dashboard .

echo.
echo Starting container...
docker run -p 8503:8503 real-estate-dashboard
goto end

:streamlit
echo.
echo Preparing for Streamlit Cloud deployment...

if not exist ".git" (
    echo Initializing git repository...
    git init
)

echo Adding files...
git add .

echo.
set /p commit_msg="Enter commit message: "
git commit -m "%commit_msg%"

echo.
echo Repository prepared!
echo.
echo Next steps:
echo 1. Create a GitHub repository
echo 2. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
echo 3. Run: git branch -M main
echo 4. Run: git push -u origin main
echo 5. Go to https://share.streamlit.io/
echo 6. Click 'New app' and select your repository
echo 7. Set main file: dashboard.py
echo 8. Click 'Deploy'
echo.
pause
goto end

:check
echo.
echo Checking deployment readiness...
echo.

echo Checking Python...
py --version
if %errorlevel% neq 0 (
    echo Python not found!
) else (
    echo Python: OK
)

echo.
echo Checking Git...
git --version
if %errorlevel% neq 0 (
    echo Git not found!
) else (
    echo Git: OK
)

echo.
echo Checking required files...
if exist "dashboard.py" (echo dashboard.py: OK) else (echo dashboard.py: MISSING)
if exist "models.py" (echo models.py: OK) else (echo models.py: MISSING)
if exist "requirements.txt" (echo requirements.txt: OK) else (echo requirements.txt: MISSING)
if exist "data\real_estate_curation_project.xlsx" (echo Excel file: OK) else (echo Excel file: MISSING)

echo.
echo Testing imports...
py -c "import streamlit; import pandas; import plotly; import sklearn; print('All imports: OK')"

echo.
echo Running model test...
py test_models.py

echo.
echo Deployment readiness check complete!
pause
goto end

:invalid
echo Invalid choice. Exiting...
goto end

:exit
echo Exiting...
goto end

:end
