import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

class RealEstateModels:
    def __init__(self, df_transformed):
        self.df = df_transformed
        self.models = {}
        self.results = {}
        
    def prepare_regression_data(self):
        """Prepare data for price prediction"""
        numeric_features = [
            'area_sqft', 'bedrooms', 'bathrooms', 'property_age_at_deal',
            'experience_years', 'rating', 'hoa_fee', 'school_score', 
            'walk_score', 'offer_price', 'loan_rate'
        ]
        
        df_reg = self.df.dropna(subset=numeric_features + ['final_price'])
        X = df_reg[numeric_features]
        y = df_reg['final_price']
        
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train_simple_regression(self):
        """Simple Linear Regression using only area_sqft"""
        df_simple = self.df.dropna(subset=['area_sqft', 'final_price'])
        X = df_simple[['area_sqft']]
        y = df_simple['final_price']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        
        self.models['simple_regression'] = {
            'model': model,
            'scaler': scaler,
            'features': ['area_sqft']
        }
        
        self.results['simple_regression'] = {
            'r2': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': mean_absolute_percentage_error(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'X_test': X_test
        }
        
        return self.results['simple_regression']
    
    def train_multiple_regression(self):
        """Multiple Linear Regression with all features"""
        X_train, X_test, y_train, y_test = self.prepare_regression_data()
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        
        self.models['multiple_regression'] = {
            'model': model,
            'scaler': scaler,
            'features': X_train.columns.tolist()
        }
        
        # Feature importance (coefficients)
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'coefficient': model.coef_
        }).sort_values('coefficient', key=abs, ascending=False)
        
        self.results['multiple_regression'] = {
            'r2': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': mean_absolute_percentage_error(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'X_test': X_test,
            'feature_importance': feature_importance
        }
        
        return self.results['multiple_regression']
    
    def train_random_forest_regression(self):
        """Random Forest Regression for price prediction"""
        X_train, X_test, y_train, y_test = self.prepare_regression_data()
        
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        self.models['random_forest_regression'] = {
            'model': model,
            'features': X_train.columns.tolist()
        }
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.results['random_forest_regression'] = {
            'r2': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': mean_absolute_percentage_error(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'X_test': X_test,
            'feature_importance': feature_importance
        }
        
        return self.results['random_forest_regression']
    
    def prepare_classification_data(self):
        """Prepare data for deal status classification"""
        numeric_features = [
            'area_sqft', 'bedrooms', 'bathrooms', 'property_age_at_deal',
            'experience_years', 'rating', 'hoa_fee', 'school_score', 
            'walk_score', 'offer_price', 'loan_rate'
        ]
        
        df_class = self.df.dropna(subset=numeric_features + ['status'])
        X = df_class[numeric_features]
        y = df_class['status']
        
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    def train_deal_status_classifier(self):
        """Random Forest Classifier for deal status prediction"""
        X_train, X_test, y_train, y_test = self.prepare_classification_data()
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        self.models['status_classifier'] = {
            'model': model,
            'features': X_train.columns.tolist(),
            'classes': model.classes_.tolist()
        }
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.results['status_classifier'] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'X_test': X_test,
            'feature_importance': feature_importance,
            'classes': model.classes_
        }
        
        return self.results['status_classifier']
    
    def predict_price(self, model_name, features_dict):
        """Predict price using trained model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        
        model_info = self.models[model_name]
        model = model_info['model']
        features = model_info['features']
        
        # Create DataFrame with features
        X = pd.DataFrame([features_dict])[features]
        
        # Scale if needed
        if 'scaler' in model_info:
            X = model_info['scaler'].transform(X)
        
        prediction = model.predict(X)[0]
        return prediction
    
    def predict_status(self, features_dict):
        """Predict deal status"""
        if 'status_classifier' not in self.models:
            raise ValueError("Status classifier not trained yet")
        
        model_info = self.models['status_classifier']
        model = model_info['model']
        features = model_info['features']
        
        X = pd.DataFrame([features_dict])[features]
        
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        return {
            'predicted_status': prediction,
            'probabilities': dict(zip(model_info['classes'], probabilities))
        }
    
    def train_all_models(self):
        """Train all models"""
        print("Training Simple Linear Regression...")
        self.train_simple_regression()
        
        print("Training Multiple Linear Regression...")
        self.train_multiple_regression()
        
        print("Training Random Forest Regression...")
        self.train_random_forest_regression()
        
        print("Training Deal Status Classifier...")
        self.train_deal_status_classifier()
        
        print("All models trained successfully!")
        
        return self.results
    
    def get_model_comparison(self):
        """Compare regression models"""
        comparison = []
        
        for model_name in ['simple_regression', 'multiple_regression', 'random_forest_regression']:
            if model_name in self.results:
                result = self.results[model_name]
                comparison.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'R² Score': result['r2'],
                    'RMSE': result['rmse'],
                    'MAPE': result['mape'],
                    'Accuracy %': result['r2'] * 100
                })
        
        return pd.DataFrame(comparison)
