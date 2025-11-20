"""
test_model.py - Unit tests for TensorFlow Fashion MNIST model
"""
import pytest
import numpy as np
import tensorflow as tf
from tensorflow import keras

def test_fashion_mnist_loads():
    """Test Fashion MNIST dataset loads"""
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    assert x_train.shape == (60000, 28, 28), "Training set should be 60000 28x28 images"
    assert x_test.shape == (10000, 28, 28), "Test set should be 10000 28x28 images"
    assert len(np.unique(y_train)) == 10, "Should have 10 classes"

def test_image_dimensions():
    """Test image dimensions"""
    (x_train, _), _ = keras.datasets.fashion_mnist.load_data()
    assert x_train[0].shape == (28, 28), "Each image should be 28x28"

def test_pixel_values():
    """Test pixel value range"""
    (x_train, _), _ = keras.datasets.fashion_mnist.load_data()
    assert x_train.min() >= 0, "Pixels should be >= 0"
    assert x_train.max() <= 255, "Pixels should be <= 255"

def test_normalization():
    """Test normalization"""
    (x_train, _), _ = keras.datasets.fashion_mnist.load_data()
    x_normalized = x_train.astype('float32') / 255.0
    assert x_normalized.min() >= 0.0, "Normalized pixels should be >= 0"
    assert x_normalized.max() <= 1.0, "Normalized pixels should be <= 1"

def test_app_structure():
    """Test app.py structure"""
    import ast
    with open('app.py', 'r') as f:
        tree = ast.parse(f.read())
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    assert 'health' in function_names, "app.py should have health() function"
    assert 'predict' in function_names, "app.py should have predict() function"
    assert 'metrics' in function_names, "app.py should have metrics() function"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])