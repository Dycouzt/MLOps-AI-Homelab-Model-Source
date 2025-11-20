"""
test_model.py - Unit tests for XGBoost Wine Quality model
"""
import pytest
import numpy as np
from sklearn.datasets import load_wine

def test_wine_dataset_loads():
    """Test wine dataset loads correctly"""
    wine = load_wine()
    assert wine.data.shape[0] == 178, "Wine dataset should have 178 samples"
    assert wine.data.shape[1] == 13, "Wine dataset should have 13 features"
    assert len(np.unique(wine.target)) == 3, "Wine dataset should have 3 classes"

def test_feature_dimensions():
    """Test feature dimensions"""
    wine = load_wine()
    assert wine.data.shape[1] == 13, "Expected 13 features"

def test_target_classes():
    """Test target classes"""
    wine = load_wine()
    unique_classes = np.unique(wine.target)
    assert len(unique_classes) == 3, "Expected 3 classes"
    assert set(unique_classes) == {0, 1, 2}, "Classes should be 0, 1, 2"

def test_data_types():
    """Test data types"""
    wine = load_wine()
    assert wine.data.dtype == np.float64, "Features should be float64"
    assert wine.target.dtype in [np.int64, np.int32], "Targets should be int"

def test_app_structure():
    """Test that app.py has required structure"""
    import ast
    with open('app.py', 'r') as f:
        tree = ast.parse(f.read())
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    assert 'health' in function_names, "app.py should have health() function"
    assert 'predict' in function_names, "app.py should have predict() function"
    assert 'metrics' in function_names, "app.py should have metrics() function"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])