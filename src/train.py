"""
train.py - Training script for Iris classification model
This script trains a RandomForest classifier on the Iris dataset,
logs metrics to MLflow, and saves the model artifact.
"""
import os
import pickle
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

# Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = "iris-classifier"
MIN_ACCURACY_THRESHOLD = 0.85  # Pipeline fails if accuracy < 85%

def train_model():
    """Train the Iris classification model"""
    print("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("iris-classification")
    
    with mlflow.start_run():
        # Hyperparameters
        n_estimators = 100
        max_depth = 10
        random_state = 42
        
        print("Training RandomForest model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\n{'='*50}")
        print(f"Model Performance Metrics:")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"{'='*50}\n")
        
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Validation check
        if accuracy < MIN_ACCURACY_THRESHOLD:
            print(f"❌ FAILED: Accuracy {accuracy:.4f} is below threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "FAILED")
            exit(1)
        else:
            print(f"✅ PASSED: Accuracy {accuracy:.4f} meets threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "PASSED")
        
        # Log model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name=MODEL_NAME
        )
        
        # Save model locally for containerization
        model_path = "model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved to {model_path}")
        
        return accuracy, model

if __name__ == "__main__":
    print("Starting model training pipeline...")
    accuracy, model = train_model()
    print(f"\n🎉 Training completed successfully! Final accuracy: {accuracy:.4f}")