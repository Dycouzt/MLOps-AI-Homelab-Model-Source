# Iris Classifier ML Model

A simple RandomForest classifier for the Iris dataset, demonstrating the full MLOps pipeline.

## Project Structure
- `train.py` - Model training script with MLflow integration
- `app.py` - Flask inference server
- `Dockerfile` - Container image definition
- `tests/` - Unit tests
- `.github/workflows/` - CI/CD pipeline

## Local Development

### Train the model
```bash
pip install -r requirements.txt
export MLFLOW_TRACKING_URI=http://34.145.47.22:30500
python train.py
```

### Run inference server
```bash
python app.py
```

### Test prediction
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```
