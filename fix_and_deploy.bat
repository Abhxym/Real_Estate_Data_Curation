@echo off
echo ==========================================
echo Streamlit Cloud Deployment Fix
echo ==========================================
echo.

echo Checking git status...
git status

echo.
echo Adding fixed files...
git add packages.txt requirements.txt STREAMLIT_CLOUD_FIX.md

echo.
echo Committing changes...
git commit -m "Fix packages.txt for Streamlit Cloud deployment"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ==========================================
echo Done! Your app will auto-deploy now.
echo ==========================================
echo.
echo Check deployment status at:
echo https://share.streamlit.io/
echo.
echo The app should be live in 2-3 minutes!
echo.
pause
