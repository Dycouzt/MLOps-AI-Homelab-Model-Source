# Copy this content into tests/test_model.py:

"""
test_model.py - Unit tests for the ML model and inference server
"""
import pytest
import numpy as np
from sklearn.datasets import load_iris

def test_iris_dataset_loads():
    """Test that the Iris dataset can be loaded"""
    iris = load_iris()
    assert iris.data.shape[0] == 150, "Iris dataset should have 150 samples"
    assert iris.data.shape[1] == 4, "Iris dataset should have 4 features"
    assert len(np.unique(iris.target)) == 3, "Iris dataset should have 3 classes"

def test_feature_dimensions():
    """Test that feature dimensions are correct"""
    iris = load_iris()
    assert iris.data.shape[1] == 4, "Expected 4 features"
    
def test_target_classes():
    """Test that target classes are valid"""
    iris = load_iris()
    unique_classes = np.unique(iris.target)
    assert len(unique_classes) == 3, "Expected 3 classes"
    assert set(unique_classes) == {0, 1, 2}, "Classes should be 0, 1, 2"

def test_data_types():
    """Test that data types are correct"""
    iris = load_iris()
    assert iris.data.dtype == np.float64, "Features should be float64"
    assert iris.target.dtype == np.int64, "Targets should be int64"

# Flask app tests (would require the app to be running)
# These are placeholder tests - in a real CI pipeline, you'd use a test client
def test_app_structure():
    """Test that app.py has the required structure"""
    import ast
    with open('app.py', 'r') as f:
        tree = ast.parse(f.read())
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    assert 'health' in function_names, "app.py should have a health() function"
    assert 'predict' in function_names, "app.py should have a predict() function"
    assert 'metrics' in function_names, "app.py should have a metrics() function"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])