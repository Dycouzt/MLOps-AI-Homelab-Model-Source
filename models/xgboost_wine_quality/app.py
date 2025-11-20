"""
app.py - XGBoost inference server for Wine Quality prediction
"""
import pickle
import numpy as np
from flask import Flask, request, jsonify
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model and scaler at startup
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    logger.info("✅ Model and scaler loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model/scaler: {e}")
    model = None
    scaler = None

# Wine quality class names
CLASS_NAMES = {0: "class_0", 1: "class_1", 2: "class_2"}

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    if model is None or scaler is None:
        return jsonify({"status": "unhealthy", "reason": "model/scaler not loaded"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict wine quality class
    Expects JSON: {"features": [13.2, 2.3, 2.6, ...]} (13 features)
    Returns: {"prediction": 1, "class_name": "class_1", "inference_time_ms": 2.5}
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        if 'features' not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Validate input shape (13 features for wine dataset)
        if features.shape[1] != 13:
            return jsonify({"error": f"Expected 13 features, got {features.shape[1]}"}), 400
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get class name
        class_name = CLASS_NAMES.get(int(prediction), "unknown")
        
        # Calculate inference time
        inference_time_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Prediction: {prediction} ({class_name}), Time: {inference_time_ms:.2f}ms")
        
        return jsonify({
            "prediction": int(prediction),
            "class_name": class_name,
            "inference_time_ms": round(inference_time_ms, 2)
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return """# HELP model_predictions_total Total predictions
# TYPE model_predictions_total counter
model_predictions_total 0
""", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)