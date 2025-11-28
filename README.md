# 🏠 Real Estate Analytics Dashboard

An interactive dashboard for real estate data analysis with machine learning predictions.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python&logoColor=white)](https://python.org)

## 🚀 Quick Start

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py
```

Or simply double-click `run_dashboard.bat` on Windows.

## 📊 Features

- **7 Interactive Pages**
  - Overview with key metrics
  - Customer analytics
  - Property analysis
  - Broker performance
  - Deal tracking
  - Advanced analytics
  - Predictive models with KPIs

- **Machine Learning Models**
  - Price prediction (98.9% accuracy)
  - Deal status classification
  - Feature importance analysis

- **Key Performance Indicators**
  - Price per square foot
  - Broker success rate
  - Customer income segments
  - Deal closure probability
  - Amenity patterns

## 📁 Project Structure

```
Real_Estate_Data_Curation/
├── dashboard.py          # Main application
├── models.py            # ML models
├── requirements.txt     # Python dependencies
├── data/
│   └── real_estate_curation_project.xlsx
└── .streamlit/
    └── config.toml
```

## 🛠️ Requirements

- Python 3.11+
- pandas
- streamlit
- plotly
- scikit-learn
- statsmodels

## 📈 Data

The dashboard analyzes 40,000+ real estate deals with:
- Customer demographics
- Property details
- Broker information
- Transaction history

## 🌐 Deployment

Deploy to Streamlit Cloud:
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select repository
4. Set main file: `dashboard.py`
5. Deploy!

## 📝 License

MIT License

## 👤 Author

Built with ❤️ for real estate analytics
