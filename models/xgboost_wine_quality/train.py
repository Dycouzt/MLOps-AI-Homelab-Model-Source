"""
train.py - XGBoost Wine Quality Classifier
Trains an XGBoost model on the Wine Quality dataset
"""
import os
import pickle
import mlflow
import mlflow.xgboost
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

# Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = "wine-quality-xgboost"
MIN_ACCURACY_THRESHOLD = 0.65  # Wine quality is harder to predict

def load_wine_data():
    """Load Wine Quality dataset from sklearn"""
    from sklearn.datasets import load_wine
    wine = load_wine()
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = wine.target
    return X, y, wine.feature_names

def train_model():
    """Train XGBoost model"""
    print("Loading Wine Quality dataset...")
    X, y, feature_names = load_wine_data()
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Number of classes: {len(np.unique(y))}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Set MLflow tracking
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("wine-quality-classification")
    
    with mlflow.start_run():
        # Hyperparameters
        params = {
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'objective': 'multi:softmax',
            'num_class': 3,
            'random_state': 42,
            'eval_metric': 'mlogloss'
        }
        
        print("Training XGBoost model...")
        model = xgb.XGBClassifier(**params)
        model.fit(
            X_train_scaled, 
            y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=False
        )
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\n{'='*50}")
        print(f"XGBoost Model Performance:")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"{'='*50}\n")
        
        # Log parameters
        mlflow.log_params(params)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Validation check
        if accuracy < MIN_ACCURACY_THRESHOLD:
            print(f"❌ FAILED: Accuracy {accuracy:.4f} below threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "FAILED")
            exit(1)
        else:
            print(f"✅ PASSED: Accuracy {accuracy:.4f} meets threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "PASSED")
        
        # Log model
        mlflow.xgboost.log_model(
            model,
            "model",
            registered_model_name=MODEL_NAME
        )
        
        # Save model and scaler locally
        with open("model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open("scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
        
        print(f"Model and scaler saved locally")
        
        return accuracy, model

if __name__ == "__main__":
    print("Starting XGBoost Wine Quality training pipeline...")
    accuracy, model = train_model()
    print(f"\n🎉 Training completed! Final accuracy: {accuracy:.4f}")