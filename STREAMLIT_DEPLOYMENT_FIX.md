# 🔧 Streamlit Cloud Deployment - Complete Fix

## 🚨 Current Issue

**Error:** `connection refused on port 8501`
**Cause:** App crashes on startup before Streamlit can start

## ✅ Root Cause Analysis

Based on your project structure, the issue is likely:

### 1. Excel File Not in Git Repository
The file `data/real_estate_curation_project.xlsx` must be committed to GitHub.

**Check file size:**
```bash
# Windows
dir data\real_estate_curation_project.xlsx

# Should be under 100MB for GitHub
```

If file is too large (>100MB), you need Git LFS or alternative hosting.

### 2. File Path Issue
Dashboard looks for: `data/real_estate_curation_project.xlsx`
File exists at: `data/real_estate_curation_project.xlsx` ✓

## 🔧 Complete Fix Steps

### Step 1: Verify Excel File is Committed

```bash
# Check if file is tracked
git ls-files data/

# If not listed, add it
git add data/real_estate_curation_project.xlsx
git commit -m "Add Excel data file"
```

### Step 2: Check File Size

```bash
# Windows PowerShell
(Get-Item "data\real_estate_curation_project.xlsx").Length / 1MB

# If > 100MB, see "Large File Solution" below
```

### Step 3: Add Debug Logging

Add this at the very top of `main()` function in dashboard.py:

```python
def main():
    # Debug: Show startup status
    st.write("🔄 Dashboard starting...")
    
    import os
    st.write(f"📁 Current directory: {os.getcwd()}")
    st.write(f"📂 Files in data/: {os.listdir('data') if os.path.exists('data') else 'data folder not found'}")
    
    st.title("🏠 Real Estate Analytics Dashboard")
    # ... rest of code
```

### Step 4: Push and Redeploy

```bash
git add dashboard.py
git commit -m "Add debug logging for Streamlit Cloud"
git push origin main
```

## 📊 File Structure Verification

Your structure should be:
```
your-repo/
├── .streamlit/
│   └── config.toml
├── data/
│   └── real_estate_curation_project.xlsx  ← MUST BE HERE
├── dashboard.py                            ← MUST BE IN ROOT
├── models.py
├── requirements.txt
├── packages.txt (empty)
└── runtime.txt
```

## 🔍 Common Issues & Solutions

### Issue 1: Excel File Too Large (>100MB)

**Solution A: Use Git LFS**
```bash
git lfs install
git lfs track "*.xlsx"
git add .gitattributes
git add data/real_estate_curation_project.xlsx
git commit -m "Add large Excel file with LFS"
git push
```

**Solution B: Host File Externally**
```python
# In dashboard.py, change load_data():
import requests
from io import BytesIO

@st.cache_data
def load_data():
    try:
        # Option 1: Google Drive (make file public)
        url = "YOUR_GOOGLE_DRIVE_DIRECT_LINK"
        
        # Option 2: Dropbox
        # url = "YOUR_DROPBOX_DIRECT_LINK"
        
        response = requests.get(url)
        dataframes = pd.read_excel(BytesIO(response.content), sheet_name=None)
        return dataframes
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
```

### Issue 2: Import Errors

Check all imports work:
```bash
py -c "import streamlit, pandas, plotly, sklearn, statsmodels; print('All imports OK')"
```

### Issue 3: Model Training Timeout

If models take too long to train on Streamlit Cloud (1GB RAM limit):

```python
# Add to dashboard.py
import streamlit as st

# Reduce data size for cloud
@st.cache_data
def prepare_transformed_data(dataframes):
    # ... existing code ...
    
    # For Streamlit Cloud, sample data if too large
    if len(df_transformed) > 10000:
        st.warning("Using sampled data for faster performance on Streamlit Cloud")
        df_transformed = df_transformed.sample(n=10000, random_state=42)
    
    return df_transformed
```

## 🧪 Local Testing Before Deploy

**Test 1: Run locally**
```bash
streamlit run dashboard.py
```
Should work without errors.

**Test 2: Test with clean environment**
```bash
# Create new virtual environment
python -m venv test_env
test_env\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py
```

**Test 3: Check file paths**
```python
# Run this Python script
import os
print("Current dir:", os.getcwd())
print("Data folder exists:", os.path.exists('data'))
print("Excel file exists:", os.path.exists('data/real_estate_curation_project.xlsx'))
```

## 📋 Deployment Checklist

Before pushing to GitHub:

- [ ] Excel file in `data/` folder
- [ ] Excel file committed to git
- [ ] File size < 100MB (or using Git LFS)
- [ ] `dashboard.py` in root directory
- [ ] `requirements.txt` has all dependencies
- [ ] `packages.txt` is empty
- [ ] Local test passes: `streamlit run dashboard.py`
- [ ] No absolute file paths in code
- [ ] All imports work

## 🚀 Quick Fix Commands

```bash
# 1. Ensure data file is tracked
git add data/real_estate_curation_project.xlsx

# 2. Commit everything
git add .
git commit -m "Fix Streamlit Cloud deployment - add data file"

# 3. Push
git push origin main

# 4. Check Streamlit Cloud logs
# Go to https://share.streamlit.io/
# Click your app → Manage app → Logs
```

## 📊 Expected Streamlit Cloud Logs

**Success looks like:**
```
[manager] Starting up repository...
[manager] Cloning repository...
[manager] Installing Python dependencies...
[manager] Successfully installed pandas-2.x.x streamlit-1.x.x ...
[manager] Starting Streamlit...
[manager] Streamlit server started on port 8501
```

**Failure looks like:**
```
[manager] Starting Streamlit...
[manager] Error: connection refused on port 8501
```

If you see the failure, scroll up to find the actual Python error.

## 🔧 Alternative: Simplified Dashboard for Testing

Create `dashboard_test.py`:

```python
import streamlit as st
import pandas as pd
import os

st.title("🧪 Deployment Test")

# Check environment
st.write("✅ Streamlit working!")
st.write(f"📁 Current directory: {os.getcwd()}")
st.write(f"📂 Contents: {os.listdir('.')}")

# Check data folder
if os.path.exists('data'):
    st.write(f"📂 Data folder contents: {os.listdir('data')}")
else:
    st.error("❌ Data folder not found!")

# Try loading Excel
try:
    df = pd.read_excel('data/real_estate_curation_project.xlsx', sheet_name='Deals')
    st.success(f"✅ Excel loaded! {len(df)} rows")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error loading Excel: {e}")
```

Deploy this first to verify file access works.

## 💡 Pro Tips

1. **Use Streamlit Secrets for sensitive data**
   - Create `.streamlit/secrets.toml` locally
   - Add secrets in Streamlit Cloud dashboard
   - Never commit secrets to git

2. **Monitor Resource Usage**
   - Streamlit Cloud free tier: 1GB RAM
   - Your ML models should fit
   - If not, reduce data size or upgrade

3. **Enable Better Error Messages**
   ```python
   import traceback
   
   try:
       # your code
   except Exception as e:
       st.error(f"Error: {e}")
       st.code(traceback.format_exc())
   ```

## 🆘 Still Not Working?

1. **Check Streamlit Cloud Logs**
   - Go to app dashboard
   - Click "Manage app"
   - Click "Logs"
   - Copy the full error message

2. **Verify Git Repository**
   ```bash
   git ls-files | grep -E "(dashboard.py|data/|requirements.txt)"
   ```

3. **Test File Access**
   ```python
   # Add to dashboard.py temporarily
   import os
   st.write("Files:", os.listdir('.'))
   st.write("Data files:", os.listdir('data') if os.path.exists('data') else 'No data folder')
   ```

## ✅ Final Verification

After deployment succeeds:
1. Dashboard loads ✓
2. Data loads without errors ✓
3. All 7 pages work ✓
4. ML models train ✓
5. Predictions work ✓

---

**Need the exact error message from Streamlit Cloud logs to provide specific fix!**
