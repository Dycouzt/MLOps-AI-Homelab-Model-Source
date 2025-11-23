"""
train.py - TensorFlow Fashion MNIST Classifier
Trains a simple CNN on Fashion MNIST dataset
"""
import os
import mlflow
import mlflow.tensorflow
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = "fashion-mnist-cnn"
MIN_ACCURACY_THRESHOLD = 0.85

def load_fashion_mnist():
    """Load Fashion MNIST dataset"""
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    
    # Normalize pixel values to 0-1
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Reshape for CNN (add channel dimension)
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    
    return (x_train, y_train), (x_test, y_test)

def create_model():
    """Create simple CNN model"""
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    """Train the model"""
    print("Loading Fashion MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_fashion_mnist()
    
    print(f"Training set size: {len(x_train)}")
    print(f"Test set size: {len(x_test)}")
    print(f"Image shape: {x_train[0].shape}")
    print(f"Number of classes: {len(np.unique(y_train))}")
    
    # Set MLflow tracking
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("fashion-mnist-classification")
    
    with mlflow.start_run():
        # Hyperparameters
        batch_size = 128
        epochs = 5  # Keep it fast for CI/CD
        
        print("Creating CNN model...")
        model = create_model()
        model.summary()
        
        print("\nTraining model...")
        history = model.fit(
            x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.1,
            verbose=1
        )
        
        # Evaluate on test set
        print("\nEvaluating on test set...")
        test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
        
        print(f"\n{'='*50}")
        print(f"CNN Model Performance:")
        print(f"{'='*50}")
        print(f"Test Loss:     {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"{'='*50}\n")
        
        # Log parameters
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("optimizer", "adam")
        
        # Log metrics
        mlflow.log_metric("test_loss", test_loss)
        mlflow.log_metric("test_accuracy", test_accuracy)
        mlflow.log_metric("final_train_accuracy", history.history['accuracy'][-1])
        
        # Validation check
        if test_accuracy < MIN_ACCURACY_THRESHOLD:
            print(f"❌ FAILED: Accuracy {test_accuracy:.4f} below threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "FAILED")
            exit(1)
        else:
            print(f"✅ PASSED: Accuracy {test_accuracy:.4f} meets threshold {MIN_ACCURACY_THRESHOLD}")
            mlflow.log_param("validation_status", "PASSED")
        
        # Log model
        mlflow.tensorflow.log_model(
            model,
            "model",
            registered_model_name=MODEL_NAME
        )
        
        # Save model locally
        model.save("model.h5")
        print("Model saved as model.h5")
        
        return test_accuracy, model

if __name__ == "__main__":
    print("Starting TensorFlow Fashion MNIST training pipeline...")
    accuracy, model = train_model()
    print(f"\n🎉 Training completed! Test accuracy: {accuracy:.4f}")