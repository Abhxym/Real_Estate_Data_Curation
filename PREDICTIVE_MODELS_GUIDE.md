# Predictive Models Guide

## Overview

This dashboard includes advanced machine learning models for real estate price prediction and deal status classification. The models are trained on your cleaned and transformed data.

## Available Models

### 1. Price Prediction Models

#### Simple Linear Regression
- **Purpose**: Baseline model for price prediction
- **Features Used**: Only `area_sqft`
- **Use Case**: Quick estimates based on property size
- **Pros**: Fast, interpretable
- **Cons**: Limited accuracy due to single feature

#### Multiple Linear Regression
- **Purpose**: Improved price prediction using all features
- **Features Used**: 
  - area_sqft
  - bedrooms
  - bathrooms
  - property_age_at_deal
  - experience_years (broker)
  - rating (broker)
  - hoa_fee
  - school_score
  - walk_score
  - offer_price
  - loan_rate
- **Use Case**: Understanding linear relationships between features and price
- **Pros**: Interpretable coefficients, shows feature impact
- **Cons**: Assumes linear relationships

#### Random Forest Regression
- **Purpose**: Best accuracy for price prediction
- **Features Used**: Same as Multiple Linear Regression
- **Use Case**: Most accurate price predictions
- **Pros**: 
  - Handles non-linear relationships
  - Robust to outliers
  - Provides feature importance
- **Cons**: Less interpretable than linear models

### 2. Deal Status Classification

#### Random Forest Classifier
- **Purpose**: Predict whether a deal will close, be pending, or cancelled
- **Output**: 
  - Predicted status (Closed/Pending/Cancelled)
  - Probability for each status
- **Features Used**: Same as regression models
- **Use Case**: Risk assessment, deal prioritization
- **Metrics**:
  - Overall accuracy
  - Precision, Recall, F1-score per class
  - Confusion matrix

## How to Use the Dashboard

### 1. Model Comparison Tab
- View performance metrics for all regression models
- Compare R² scores, RMSE, and MAPE
- Identify the best performing model

### 2. Price Prediction Tab
- Enter property details in the form
- Select a model (Simple, Multiple, or Random Forest)
- Click "Predict Price" to get instant prediction
- See price per square foot calculation

### 3. Feature Importance Tab
- Understand which features impact predictions most
- View coefficients (Linear Regression) or importance scores (Random Forest)
- Use insights to focus on key property attributes

### 4. Deal Status Prediction Tab
- View classifier performance metrics
- See confusion matrix showing prediction accuracy
- Use interactive tool to predict deal status
- Get probability scores for each possible status

### 5. Model Performance Tab
- Visualize actual vs predicted prices
- Analyze residuals (prediction errors)
- Check for model bias or patterns in errors
- View scatter plots with trend lines

## Understanding Model Metrics

### R² Score (R-squared)
- Range: -∞ to 1.0
- Interpretation: Proportion of variance explained by the model
- Good: > 0.7
- Excellent: > 0.9

### RMSE (Root Mean Squared Error)
- Unit: Same as target variable (₹)
- Interpretation: Average prediction error
- Lower is better
- Compare across models to find best performer

### MAPE (Mean Absolute Percentage Error)
- Range: 0% to ∞
- Interpretation: Average percentage error
- Good: < 10%
- Acceptable: < 20%

### Accuracy (Classification)
- Range: 0% to 100%
- Interpretation: Percentage of correct predictions
- Good: > 80%
- Excellent: > 90%

## Feature Importance Interpretation

### High Importance Features
Features with high importance scores have the most impact on predictions:
- **offer_price**: Usually the strongest predictor of final price
- **area_sqft**: Property size is crucial
- **location factors**: school_score, walk_score
- **property characteristics**: bedrooms, bathrooms, age

### Using Feature Importance
1. **For Sellers**: Focus on improving high-importance features
2. **For Buyers**: Prioritize properties with good scores on important features
3. **For Brokers**: Highlight key features in listings

## Best Practices

### When to Use Each Model

**Simple Regression**
- Quick estimates
- When only area is known
- Baseline comparisons

**Multiple Regression**
- Understanding feature relationships
- When interpretability is important
- Linear pricing strategies

**Random Forest**
- Most accurate predictions
- Complex pricing scenarios
- When accuracy is critical

### Prediction Reliability

Predictions are most reliable when:
- Input values are within training data range
- Property characteristics are typical
- All features are provided

Predictions may be less reliable for:
- Luxury properties (outliers)
- Very old or very new properties
- Properties with unusual features

## Technical Details

### Model Training
- **Train/Test Split**: 80/20
- **Random State**: 42 (for reproducibility)
- **Scaling**: StandardScaler for linear models
- **Random Forest Parameters**:
  - n_estimators: 100
  - max_depth: 15 (regression), 10 (classification)
  - min_samples_split: 5

### Data Preparation
1. Merge all datasets (Deals, Customers, Brokers, Properties, PropertyDetails)
2. Calculate derived features (property_age_at_deal)
3. Handle missing values
4. Remove outliers (flagged but not removed)
5. Split into train/test sets

### Model Validation
- Cross-validation on training set
- Performance evaluation on held-out test set
- Residual analysis for regression
- Confusion matrix for classification

## Troubleshooting

### "Model not trained yet" Error
- Wait for models to finish training
- Check console for error messages
- Verify data is loaded correctly

### Poor Predictions
- Check if input values are realistic
- Ensure all features are provided
- Try different models
- Review feature importance

### Low Model Accuracy
- May indicate data quality issues
- Consider collecting more data
- Check for missing or incorrect values
- Review feature engineering

## Future Enhancements

Potential improvements:
1. **More Models**: XGBoost, Neural Networks
2. **Hyperparameter Tuning**: Grid search for optimal parameters
3. **Feature Engineering**: Create interaction terms, polynomial features
4. **Time Series**: Predict price trends over time
5. **Ensemble Methods**: Combine multiple models
6. **Explainability**: SHAP values for individual predictions

## Support

For issues or questions:
1. Check the README.md file
2. Review this guide
3. Test models using test_models.py
4. Check console output for errors
