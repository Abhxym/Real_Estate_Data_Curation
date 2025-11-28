Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Streamlit Cloud Deployment Verification" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking critical files..." -ForegroundColor Yellow
Write-Host ""

# Check dashboard.py
if (Test-Path "dashboard.py") {
    Write-Host "[✓] dashboard.py found" -ForegroundColor Green
} else {
    Write-Host "[✗] dashboard.py MISSING!" -ForegroundColor Red
    exit 1
}

# Check data folder
if (Test-Path "data") {
    Write-Host "[✓] data folder found" -ForegroundColor Green
} else {
    Write-Host "[✗] data folder MISSING!" -ForegroundColor Red
    exit 1
}

# Check Excel file
if (Test-Path "data\real_estate_curation_project.xlsx") {
    $size = (Get-Item "data\real_estate_curation_project.xlsx").Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "[✓] Excel file found ($sizeMB MB)" -ForegroundColor Green
    
    if ($sizeMB -gt 100) {
        Write-Host "[⚠] WARNING: File is larger than 100MB - may need Git LFS" -ForegroundColor Yellow
    }
} else {
    Write-Host "[✗] Excel file MISSING!" -ForegroundColor Red
    exit 1
}

# Check requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "[✓] requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "[✗] requirements.txt MISSING!" -ForegroundColor Red
    exit 1
}

# Check packages.txt
if (Test-Path "packages.txt") {
    $size = (Get-Item "packages.txt").Length
    if ($size -eq 0) {
        Write-Host "[✓] packages.txt is empty (correct!)" -ForegroundColor Green
    } else {
        Write-Host "[⚠] packages.txt is not empty" -ForegroundColor Yellow
    }
} else {
    Write-Host "[⚠] packages.txt missing (optional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Checking git status..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "[✓] Git repository initialized" -ForegroundColor Green
    
    # Check if files are tracked
    $tracked = git ls-files
    
    if ($tracked -match "dashboard.py") {
        Write-Host "  [✓] dashboard.py tracked" -ForegroundColor Green
    } else {
        Write-Host "  [✗] dashboard.py NOT tracked" -ForegroundColor Red
    }
    
    if ($tracked -match "data/real_estate_curation_project.xlsx") {
        Write-Host "  [✓] Excel file tracked" -ForegroundColor Green
    } else {
        Write-Host "  [✗] Excel file NOT tracked - THIS IS THE PROBLEM!" -ForegroundColor Red
        Write-Host "  Run: git add data/real_estate_curation_project.xlsx" -ForegroundColor Yellow
    }
    
    if ($tracked -match "requirements.txt") {
        Write-Host "  [✓] requirements.txt tracked" -ForegroundColor Green
    } else {
        Write-Host "  [✗] requirements.txt NOT tracked" -ForegroundColor Red
    }
} else {
    Write-Host "[⚠] Not a git repository" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing Python environment..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

try {
    py -c "import streamlit, pandas, plotly, sklearn, statsmodels; print('All imports successful')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[✓] All dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[✗] Some dependencies missing" -ForegroundColor Red
        Write-Host "Run: py -m pip install -r requirements.txt" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[✗] Python test failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Deployment Readiness Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure Excel file is tracked:" -ForegroundColor White
Write-Host "   git add data/real_estate_curation_project.xlsx" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Commit all changes:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Fix Streamlit Cloud deployment'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Push to GitHub:" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Deploy on Streamlit Cloud:" -ForegroundColor White
Write-Host "   https://share.streamlit.io/" -ForegroundColor Gray
Write-Host ""
Write-Host "5. If deployment fails, check:" -ForegroundColor White
Write-Host "   STREAMLIT_DEPLOYMENT_FIX.md" -ForegroundColor Gray
Write-Host ""
