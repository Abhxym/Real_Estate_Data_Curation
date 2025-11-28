"""
Quick test script to verify models work correctly
"""
import pandas as pd
import sys

print("Testing Real Estate Predictive Models...")
print("=" * 50)

# Load data
try:
    print("\n1. Loading data...")
    dataframes = pd.read_excel('data/real_estate_curation_project.xlsx', sheet_name=None)
    print(f"   ✓ Loaded {len(dataframes)} sheets")
except Exception as e:
    print(f"   ✗ Error loading data: {e}")
    sys.exit(1)

# Prepare data
try:
    print("\n2. Preparing transformed data...")
    deals = dataframes['Deals'].copy()
    customers = dataframes['Customers'].copy()
    brokers = dataframes['Brokers'].copy()
    properties = dataframes['Properties'].copy()
    prop_details = dataframes['PropertyDetails'].copy()
    
    df = deals.merge(customers, on='customer_id', how='left', suffixes=('', '_cust'))
    df = df.merge(brokers, on='broker_id', how='left', suffixes=('', '_broker'))
    df = df.merge(properties, on='property_id', how='left', suffixes=('', '_prop'))
    df = df.merge(prop_details, on='property_id', how='left', suffixes=('', '_detail'))
    
    df['deal_date'] = pd.to_datetime(df['deal_date'], errors='coerce')
    df['property_age_at_deal'] = df['deal_date'].dt.year - df['year_built']
    
    numeric_cols = ['area_sqft', 'bedrooms', 'bathrooms', 'property_age_at_deal',
                   'experience_years', 'rating', 'hoa_fee', 'school_score', 
                   'walk_score', 'offer_price', 'loan_rate', 'final_price', 'status']
    
    available_cols = [col for col in numeric_cols if col in df.columns]
    df_transformed = df[available_cols].copy()
    
    print(f"   ✓ Prepared data with {len(df_transformed)} rows and {len(df_transformed.columns)} columns")
except Exception as e:
    print(f"   ✗ Error preparing data: {e}")
    sys.exit(1)

# Test models
try:
    print("\n3. Importing models...")
    from models import RealEstateModels
    print("   ✓ Models imported successfully")
    
    print("\n4. Initializing model trainer...")
    re_models = RealEstateModels(df_transformed)
    print("   ✓ Model trainer initialized")
    
    print("\n5. Training models (this may take a minute)...")
    
    print("   - Training Simple Linear Regression...")
    re_models.train_simple_regression()
    print("     ✓ Simple regression trained")
    
    print("   - Training Multiple Linear Regression...")
    re_models.train_multiple_regression()
    print("     ✓ Multiple regression trained")
    
    print("   - Training Random Forest Regression...")
    re_models.train_random_forest_regression()
    print("     ✓ Random Forest regression trained")
    
    print("   - Training Deal Status Classifier...")
    re_models.train_deal_status_classifier()
    print("     ✓ Status classifier trained")
    
    print("\n6. Model Performance Summary:")
    print("-" * 50)
    comparison = re_models.get_model_comparison()
    print(comparison.to_string(index=False))
    
    print("\n7. Testing predictions...")
    
    # Test price prediction
    test_features = {
        'area_sqft': 1500,
        'bedrooms': 3,
        'bathrooms': 2,
        'property_age_at_deal': 5,
        'experience_years': 10,
        'rating': 4.0,
        'hoa_fee': 5000,
        'school_score': 75,
        'walk_score': 70,
        'offer_price': 5000000,
        'loan_rate': 9.5
    }
    
    predicted_price = re_models.predict_price('random_forest_regression', test_features)
    print(f"   ✓ Predicted price for test property: ₹{predicted_price:,.2f}")
    
    # Test status prediction
    status_pred = re_models.predict_status(test_features)
    print(f"   ✓ Predicted deal status: {status_pred['predicted_status']}")
    print(f"     Confidence: {max(status_pred['probabilities'].values()):.2%}")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed successfully!")
    print("=" * 50)
    print("\nYou can now run the dashboard:")
    print("  py -m streamlit run dashboard.py")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
