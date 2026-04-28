# Drone Edge AI Simulation

This is a lightweight Python-based simulation of a multi-sensor edge inference system for UAV disaster monitoring.

## Tech stack

- Python 3.11+
- FastAPI for local API
- Uvicorn as ASGI server
- NumPy for numeric simulation
- Pydantic for request validation
- Jinja2 for templates

## Project structure

- `app/` — application code
- `app/main.py` — FastAPI application entry point
- `app/routes.py` — API routes
- `app/schemas.py` — request/response models
- `app/models/edge_fusion.py` — simple edge-fusion inference logic
- `app/simulation.py` — simulated multi-sensor inputs
- `run_demo.py` — local CLI demo
- `test_api.ps1` — PowerShell API testing script
- `requirements.txt` — dependencies

## Features

- **Multi-sensor fusion**: Combines RGB anomaly, thermal heat index, and human signature scores
- **Environmental monitoring**: Tracks temperature, humidity, CO levels, and pressure
- **Event classification**: Detects fire, structural damage, human presence, or normal conditions
- **Batch processing**: Process multiple sensor frames simultaneously
- **Web dashboard**: Interactive UI with animations and real-time API testing
- **Simulation**: Generate realistic sensor data for testing

## Install and run

1. Create a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the API server:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open the dashboard:

Navigate to `http://localhost:8000/dashboard` in your browser to access the interactive web interface.

## API Endpoints

- `GET /health` — Service health check
- `GET /simulate` — Generate and process simulated sensor data
- `POST /infer` — Single inference with custom sensor data
- `POST /batch_infer` — Batch processing of multiple sensor frames
- `GET /dashboard` — Interactive web dashboard

## Testing

Run the included PowerShell test script:

```powershell
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

Or run the local demo:

```powershell
python run_demo.py
```

```powershell
curl -X GET http://127.0.0.1:8000/simulate
```

```powershell
curl -X POST http://127.0.0.1:8000/infer -H "Content-Type: application/json" -d @sample_request.json
```

```powershell
curl -X POST http://127.0.0.1:8000/batch_infer -H "Content-Type: application/json" -d @batch_request.json
```

## Dashboard

Open `http://127.0.0.1:8000/dashboard` in your browser for a simple web interface.

## Demo

Run the local demo without starting the server:

```powershell
python run_demo.py
```

## Notes

- This project uses simulated sensor input rather than a real dataset.
- The model logic is lightweight and designed for edge-style inference.
- You can extend the model later to load actual pre-trained models or add more sensor fusion rules.
