# Quick Reference Card

## 🚀 Getting Started (3 Steps)

```bash
# 1. Install dependencies
py -m pip install -r requirements.txt

# 2. Run dashboard
py -m streamlit run dashboard.py

# 3. Open browser to http://localhost:8501
```

## 📊 Dashboard Pages

| Page | Purpose | Key Features |
|------|---------|--------------|
| **Overview** | Data summary | Metrics, dataset sizes, sample data |
| **Customers** | Demographics | Cities, segments, income analysis |
| **Properties** | Inventory | Types, locations, sizes |
| **Brokers** | Performance | Agencies, ratings, experience |
| **Deals** | Transactions | Status, prices, trends |
| **Analytics** | Insights | Price/sqft, success rates, trends |
| **Predictive Models** | ML Predictions | Price & status prediction |

## 🤖 Machine Learning Models

### Price Prediction
- **Simple Regression**: Area only → Quick estimate
- **Multiple Regression**: All features → Interpretable
- **Random Forest**: All features → Most accurate ⭐

### Status Prediction
- **Random Forest Classifier**: Predicts Closed/Pending/Cancelled

## 📈 Key Metrics

| Metric | Good Value | Meaning |
|--------|-----------|---------|
| **R² Score** | > 0.7 | Model explains variance |
| **RMSE** | Lower | Average error in ₹ |
| **MAPE** | < 20% | Percentage error |
| **Accuracy** | > 80% | Correct predictions |

## 🎯 Common Tasks

### Predict Property Price
1. Go to **Predictive Models** page
2. Click **Price Prediction** tab
3. Enter property details
4. Select model
5. Click **Predict Price**

### Predict Deal Status
1. Go to **Predictive Models** page
2. Click **Deal Status Prediction** tab
3. Scroll to prediction tool
4. Enter deal details
5. Click **Predict Deal Status**

### Compare Models
1. Go to **Predictive Models** page
2. Click **Model Comparison** tab
3. View metrics table and charts

### View Feature Importance
1. Go to **Predictive Models** page
2. Click **Feature Importance** tab
3. Select model
4. View chart and table

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard won't start | Check Python & dependencies |
| Data not loading | Verify Excel file in data/ folder |
| Models not training | Check data quality, run test_models.py |
| Slow performance | Reduce data size, use simpler models |
| Poor predictions | Check input ranges, try different model |

## 📁 File Structure

```
├── dashboard.py          # Main app
├── models.py            # ML models
├── test_models.py       # Testing
├── requirements.txt     # Dependencies
├── run_dashboard.bat    # Quick start
└── data/
    └── real_estate_curation_project.xlsx
```

## 💡 Pro Tips

1. **Best Model**: Use Random Forest for most accurate predictions
2. **Feature Importance**: Check which features matter most
3. **Residual Plot**: Look for patterns indicating model issues
4. **Status Probabilities**: Higher confidence = more reliable prediction
5. **Test First**: Run test_models.py before using dashboard

## 🎨 Customization Quick Wins

```python
# Change color scheme
color_continuous_scale='Blues'  # Try: Viridis, Reds, Greens

# Add new metric
st.metric("New Metric", value, delta)

# Add filter
selected = st.selectbox("Filter", options)
```

## 📊 Data Requirements

**Minimum Required Columns**:
- Deals: deal_id, customer_id, broker_id, property_id, offer_price, final_price, status
- Customers: customer_id, city, segment
- Brokers: broker_id, rating, experience_years
- Properties: property_id, area_sqft, bedrooms, bathrooms, year_built
- PropertyDetails: property_id, hoa_fee, school_score, walk_score

## 🎯 Model Selection Guide

| Scenario | Recommended Model |
|----------|------------------|
| Quick estimate | Simple Regression |
| Understand factors | Multiple Regression |
| Best accuracy | Random Forest Regression |
| Deal risk | Random Forest Classifier |

## 📞 Quick Help

```bash
# Test models
py test_models.py

# Check dependencies
py -m pip list

# Update packages
py -m pip install --upgrade -r requirements.txt
```

## 🔑 Keyboard Shortcuts (in browser)

- `Ctrl + R`: Refresh dashboard
- `Ctrl + Shift + R`: Hard refresh
- `F11`: Fullscreen mode

## 📈 Performance Benchmarks

- **Load Time**: < 10 seconds
- **Model Training**: < 2 minutes
- **Prediction**: Instant
- **Chart Rendering**: < 1 second

## ✅ Pre-Launch Checklist

- [ ] Dependencies installed
- [ ] Excel file in data/ folder
- [ ] test_models.py passes
- [ ] Dashboard loads
- [ ] All pages work
- [ ] Models train
- [ ] Predictions accurate

---

**Need More Help?**
- README.md - Setup guide
- PREDICTIVE_MODELS_GUIDE.md - ML details
- DASHBOARD_SUMMARY.md - Complete overview
