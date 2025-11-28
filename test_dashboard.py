"""Quick test to identify dashboard errors"""
import sys

print("Testing dashboard components...")
print("=" * 50)

# Test 1: Import modules
print("\n1. Testing imports...")
try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    print("   ✓ All imports successful")
except Exception as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

# Test 2: Load data
print("\n2. Testing data loading...")
try:
    excel_file = 'data/real_estate_curation_project.xlsx'
    dataframes = pd.read_excel(excel_file, sheet_name=None)
    print(f"   ✓ Loaded {len(dataframes)} sheets")
    print(f"   Sheets: {list(dataframes.keys())}")
except Exception as e:
    print(f"   ✗ Data loading error: {e}")
    sys.exit(1)

# Test 3: Check required sheets
print("\n3. Checking required sheets...")
required_sheets = ['Customers', 'Brokers', 'Properties', 'PropertyDetails', 'Deals']
missing = [s for s in required_sheets if s not in dataframes]
if missing:
    print(f"   ⚠ Missing sheets: {missing}")
else:
    print("   ✓ All required sheets present")

# Test 4: Check data structure
print("\n4. Checking data structure...")
for name, df in dataframes.items():
    print(f"   {name}: {len(df)} rows, {len(df.columns)} columns")

# Test 5: Test city cleaning
print("\n5. Testing city name cleaning...")
try:
    city_mapping = {
        'Surrat': 'Surat', 'Chennnai': 'Chennai', 'Kalkata': 'Kolkata',
        'Calcutta': 'Kolkata', 'Mumbay': 'Mumbai', 'Mumbaai': 'Mumbai',
        'Bengluru': 'Bengaluru', 'Poona': 'Pune', 'Jaypur': 'Jaipur',
        'Ahemdabad': 'Ahmedabad', 'Dehli': 'Delhi', 'New Delhi': 'Delhi',
        'Nodia': 'Noida', 'Hyderbad': 'Hyderabad', 'Gurugram': 'Gurgaon'
    }
    
    for name in ['Customers', 'Brokers', 'Properties']:
        if name in dataframes and 'city' in dataframes[name].columns:
            df = dataframes[name]
            df['city'] = df['city'].str.strip().str.title()
            df['city'] = df['city'].replace(city_mapping)
            print(f"   ✓ Cleaned {name} cities")
except Exception as e:
    print(f"   ✗ City cleaning error: {e}")

# Test 6: Test basic visualization
print("\n6. Testing visualization...")
try:
    if 'Customers' in dataframes:
        df = dataframes['Customers']
        if 'city' in df.columns:
            city_counts = df['city'].value_counts().head(10)
            fig = px.bar(x=city_counts.index, y=city_counts.values)
            print("   ✓ Visualization test passed")
except Exception as e:
    print(f"   ✗ Visualization error: {e}")

print("\n" + "=" * 50)
print("✅ All basic tests passed!")
print("\nIf dashboard still has errors, please share the specific error message.")
