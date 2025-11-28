"""
Minimal test version to identify deployment issues
Rename this to dashboard.py to test
"""
import streamlit as st

st.set_page_config(
    page_title="Real Estate Dashboard - Test",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Analytics Dashboard")
st.success("✅ App started successfully!")

# Test 1: Check file system
import os
st.subheader("📁 File System Check")
st.write(f"Current directory: {os.getcwd()}")
st.write(f"Files in root: {os.listdir('.')[:10]}")

if os.path.exists('data'):
    st.write(f"Files in data/: {os.listdir('data')}")
else:
    st.error("data/ folder not found!")

# Test 2: Try loading Excel
st.subheader("📊 Data Loading Test")
try:
    import pandas as pd
    excel_file = 'data/real_estate_curation_project.xlsx'
    
    if os.path.exists(excel_file):
        st.info(f"Excel file found at: {excel_file}")
        
        # Try to load
        with st.spinner("Loading Excel..."):
            dataframes = pd.read_excel(excel_file, sheet_name=None)
        
        st.success(f"✅ Loaded {len(dataframes)} sheets!")
        
        for name, df in dataframes.items():
            st.write(f"- {name}: {len(df)} rows, {len(df.columns)} columns")
    else:
        st.error(f"Excel file NOT found at: {excel_file}")
        
except Exception as e:
    st.error(f"Error loading Excel: {e}")
    import traceback
    st.code(traceback.format_exc())

# Test 3: Try importing models
st.subheader("🤖 Models Import Test")
try:
    from models import RealEstateModels
    st.success("✅ Models imported successfully!")
except Exception as e:
    st.error(f"Error importing models: {e}")
    import traceback
    st.code(traceback.format_exc())

st.info("If you see this message, the app is working! The issue is in the main dashboard code.")
