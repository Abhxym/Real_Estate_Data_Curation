# Real Estate Analytics Dashboard

An interactive dashboard for visualizing and analyzing real estate data with machine learning predictions.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

## 🌐 Live Demo

**Deploy your own:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## Features

- **Overview**: Key metrics and dataset summaries
- **Customers**: Customer demographics, income analysis, and city distribution
- **Properties**: Property types, area analysis, and location insights
- **Brokers**: Broker performance, ratings, and experience analysis
- **Deals**: Deal status, pricing trends, and mortgage analysis
- **Analytics**: Advanced insights including price per sq ft, broker success rates, and trends
- **Predictive Models**: Machine learning models for price prediction and deal status classification
  - Simple Linear Regression
  - Multiple Linear Regression
  - Random Forest Regression
  - Random Forest Classification for deal status
  - Interactive prediction tools
  - Feature importance analysis
  - Model performance visualizations

## Installation

1. Install dependencies:
```bash
py -m pip install pandas openpyxl streamlit plotly scikit-learn seaborn
```

Or use the requirements file:
```bash
py -m pip install -r requirements.txt
```

## Running the Dashboard

1. Make sure the Excel file is in the `data` folder
2. Run the dashboard:
```bash
py -m streamlit run dashboard.py
```

3. The dashboard will open in your browser at `http://localhost:8501`

## Data Requirements

The dashboard expects an Excel file named `real_estate_curation_project.xlsx` in the `data` folder with the following sheets:
- Customers
- Brokers
- Properties
- PropertyDetails
- Deals

## Navigation

Use the sidebar to navigate between different pages:
- **Overview**: High-level summary of all datasets
- **Customers**: Customer analytics and segmentation
- **Properties**: Property characteristics and distribution
- **Brokers**: Broker performance metrics
- **Deals**: Transaction analysis
- **Analytics**: Advanced insights and trends
- **Predictive Models**: Machine learning models and predictions
  - Model Comparison: Compare performance of different regression models
  - Price Prediction: Interactive tool to predict property prices
  - Feature Importance: Understand which features impact predictions most
  - Deal Status Prediction: Predict whether a deal will close
  - Model Performance: Visualize actual vs predicted values, residuals, etc.

## Predictive Models Details

### Regression Models (Price Prediction)
1. **Simple Linear Regression**: Uses only area_sqft to predict price
2. **Multiple Linear Regression**: Uses all available features
3. **Random Forest Regression**: Ensemble model for better accuracy

### Classification Model (Deal Status)
- **Random Forest Classifier**: Predicts deal status (Closed, Pending, Cancelled)
- Provides probability scores for each status
- Shows feature importance for status prediction

### Model Metrics
- **R² Score**: Measures how well the model explains variance
- **RMSE**: Root Mean Squared Error (lower is better)
- **MAPE**: Mean Absolute Percentage Error
- **Accuracy**: For classification model
- **Confusion Matrix**: Shows prediction accuracy by class
