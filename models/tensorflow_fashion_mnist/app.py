"""
app.py - TensorFlow inference server for Fashion MNIST
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np
from flask import Flask, request, jsonify
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Fashion MNIST class names
CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

# Load model at startup
try:
    model = keras.models.load_model('model.h5')
    logger.info("✅ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    if model is None:
        return jsonify({"status": "unhealthy", "reason": "model not loaded"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict fashion item class
    Expects JSON: {"image": [[pixel_values]]} - 28x28 array or flattened 784 array
    Returns: {"prediction": 5, "class_name": "Sandal", "confidence": 0.95, "inference_time_ms": 10.5}
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "Missing 'image' in request"}), 400
        
        image = np.array(data['image'])
        
        # Handle both flattened (784,) and 2D (28, 28) input
        if image.shape == (784,):
            image = image.reshape(28, 28)
        elif image.shape != (28, 28):
            return jsonify({"error": f"Invalid image shape: {image.shape}. Expected (28, 28) or (784,)"}), 400
        
        # Normalize if not already (assume 0-255 range if max > 1)
        if image.max() > 1.0:
            image = image / 255.0
        
        # Reshape for model input (add batch and channel dimensions)
        image = image.reshape(1, 28, 28, 1)
        
        # Make prediction
        predictions = model.predict(image, verbose=0)[0]
        predicted_class = int(np.argmax(predictions))
        confidence = float(predictions[predicted_class])
        
        # Get class name
        class_name = CLASS_NAMES[predicted_class]
        
        # Calculate inference time
        inference_time_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Prediction: {predicted_class} ({class_name}), Confidence: {confidence:.2f}, Time: {inference_time_ms:.2f}ms")
        
        return jsonify({
            "prediction": predicted_class,
            "class_name": class_name,
            "confidence": round(confidence, 4),
            "all_probabilities": [round(float(p), 4) for p in predictions],
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