import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

class FraudDetectionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Try to load existing model
        if os.path.exists('fraud_model.pkl') and os.path.exists('scaler.pkl'):
            self.load_model()
        else:
            self.train_model()
    
    def generate_sample_data(self, n_samples=10000):
        """Generate synthetic credit card transaction data"""
        np.random.seed(42)
        
        # Generate features
        data = {
            'amount': np.random.lognormal(3, 1.5, n_samples),
            'merchant_category': np.random.randint(1, 20, n_samples),
            'hour': np.random.randint(0, 24, n_samples),
            'day_of_week': np.random.randint(1, 8, n_samples),
            'is_weekend': np.random.randint(0, 2, n_samples),
            'transaction_count_1h': np.random.poisson(2, n_samples),
            'avg_amount_1h': np.random.lognormal(2.5, 1, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Generate fraud labels (5% fraud rate)
        fraud_probability = (
            (df['amount'] > 1000) * 0.3 +
            (df['hour'].isin([2, 3, 4])) * 0.2 +
            (df['transaction_count_1h'] > 5) * 0.4 +
            np.random.random(n_samples) * 0.1
        )
        
        df['is_fraud'] = (fraud_probability > 0.4).astype(int)
        
        return df
    
    def train_model(self):
        """Train the fraud detection model"""
        print("Training fraud detection model...")
        
        # Generate synthetic data
        df = self.generate_sample_data()
        
        # Prepare features and target
        feature_columns = ['amount', 'merchant_category', 'hour', 'day_of_week', 
                          'is_weekend', 'transaction_count_1h', 'avg_amount_1h']
        X = df[feature_columns]
        y = df['is_fraud']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        print("Model Performance:")
        print(classification_report(y_test, y_pred))
        
        # Save model
        self.save_model()
        self.is_trained = True
        print("Model trained and saved successfully!")
    
    def predict(self, features):
        """Predict fraud for given features"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)
    
    def predict_proba(self, features):
        """Get prediction probabilities"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        features_scaled = self.scaler.transform(features)
        return self.model.predict_proba(features_scaled)
    
    def save_model(self):
        """Save the trained model and scaler"""
        joblib.dump(self.model, 'fraud_model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')
    
    def load_model(self):
        """Load the trained model and scaler"""
        self.model = joblib.load('fraud_model.pkl')
        self.scaler = joblib.load('scaler.pkl')
        self.is_trained = True
        print("Model loaded successfully!")

if __name__ == "__main__":
    # Train model if run directly
    model = FraudDetectionModel()