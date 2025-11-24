"""
app.py - Flask inference server for the Iris classifier
Exposes REST API endpoints for model predictions and health checks
"""
import pickle
import numpy as np
from flask import Flask, request, jsonify
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model at startup
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info("✅ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    if model is None:
        return jsonify({"status": "unhealthy", "reason": "model not loaded"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    Expects JSON: {"features": [5.1, 3.5, 1.4, 0.2]}
    Returns JSON: {"prediction": 0, "class_name": "setosa", "inference_time_ms": 1.23}
    """
    start_time = time.time()
    
    try:
        # Parse request
        data = request.get_json()
        if 'features' not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Validate input shape
        if features.shape[1] != 4:
            return jsonify({"error": "Expected 4 features, got {}".format(features.shape[1])}), 400
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Map prediction to class name
        class_names = {0: "setosa", 1: "versicolor", 2: "virginica"}
        class_name = class_names.get(int(prediction), "unknown")
        
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
    """
    Prometheus metrics endpoint
    Returns metrics in Prometheus exposition format
    """
    # In a real system, you'd track these metrics properly
    # For now, return dummy metrics
    metrics_text = """# HELP model_predictions_total Total number of predictions
# TYPE model_predictions_total counter
model_predictions_total 0

# HELP model_inference_duration_seconds Time spent processing predictions
# TYPE model_inference_duration_seconds histogram
model_inference_duration_seconds_bucket{le="0.005"} 0
model_inference_duration_seconds_bucket{le="0.01"} 0
model_inference_duration_seconds_bucket{le="0.025"} 0
model_inference_duration_seconds_bucket{le="0.05"} 0
model_inference_duration_seconds_bucket{le="0.1"} 0
model_inference_duration_seconds_bucket{le="+Inf"} 0
model_inference_duration_seconds_sum 0
model_inference_duration_seconds_count 0
"""
    return metrics_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)