from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.schemas import BatchInferenceRequest, BatchInferenceResponse, InferenceRequest, InferenceResponse, SimulationResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "drone-edge-ai"}


@router.post("/infer", response_model=InferenceResponse)
def infer(request: InferenceRequest, req: Request):
    model = req.app.state.model
    result = model.predict(request)
    return result


@router.post("/batch_infer", response_model=BatchInferenceResponse)
def batch_infer(request: BatchInferenceRequest, req: Request):
    model = req.app.state.model
    responses = [model.predict(req) for req in request.requests]
    return BatchInferenceResponse(responses=responses)


@router.get("/simulate", response_model=SimulationResponse)
def simulate(req: Request):
    simulator = req.app.state.simulator
    model = req.app.state.model
    sample = simulator.generate()
    prediction = model.predict(sample)
    return SimulationResponse(input=sample, output=prediction)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drone Edge AI Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                overflow-x: hidden;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                overflow: hidden;
                animation: slideIn 0.8s ease-out;
            }
            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="20" cy="30" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="70" r="1.5" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
                animation: twinkle 4s linear infinite;
            }
            @keyframes twinkle {
                0% { transform: translateX(-100px); }
                100% { transform: translateX(100px); }
            }
            h1 {
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
                position: relative;
                z-index: 1;
            }
            .drone-icon {
                display: inline-block;
                width: 40px;
                height: 40px;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>') no-repeat center;
                background-size: contain;
                margin-right: 10px;
                animation: float 3s ease-in-out infinite;
            }
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            .subtitle {
                opacity: 0.9;
                font-size: 1.1em;
                position: relative;
                z-index: 1;
            }
            .content {
                padding: 30px;
            }
            .button-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            button {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                border: none;
                padding: 18px 25px;
                border-radius: 12px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
            }
            button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            button:hover::before {
                left: 100%;
            }
            button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
            }
            button:active {
                transform: translateY(-1px);
            }
            .output-section {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 25px;
                border-left: 5px solid #3498db;
                animation: fadeIn 0.5s ease-in;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .output-title {
                font-weight: bold;
                margin-bottom: 15px;
                color: #2c3e50;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            pre {
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Fira Code', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
                margin: 0;
                white-space: pre-wrap;
                word-wrap: break-word;
                animation: codeHighlight 0.3s ease-in;
            }
            @keyframes codeHighlight {
                0% { background: #4a5568; }
                100% { background: #2d3748; }
            }
            .loading {
                display: none;
                text-align: center;
                color: #666;
                font-style: italic;
                animation: pulse 1.5s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .status {
                text-align: center;
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
                animation: bounceIn 0.6s ease-out;
            }
            @keyframes bounceIn {
                0% { transform: scale(0.3); opacity: 0; }
                50% { transform: scale(1.05); }
                70% { transform: scale(0.9); }
                100% { transform: scale(1); opacity: 1; }
            }
            .status.success { color: #27ae60; }
            .status.error { color: #e74c3c; }
            @media (max-width: 768px) {
                .button-grid {
                    grid-template-columns: 1fr;
                }
                h1 {
                    font-size: 2em;
                }
                .drone-icon {
                    width: 30px;
                    height: 30px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1><span class="drone-icon"></span>Drone Edge AI Dashboard</h1>
                <div class="subtitle">Multi-Sensor Fusion for UAV Disaster Monitoring</div>
            </header>
            <div class="content">
                <div class="button-grid">
                    <button onclick="callAPI('/health', 'GET')">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        Health Check
                    </button>
                    <button onclick="callAPI('/simulate', 'GET')">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        Simulate
                    </button>
                    <button onclick="callAPI('/infer', 'POST', getSampleData())">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M15.5 14l-3.5-7-3.5 7h2.5v3h1.5v-3z"/>
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        Single Inference
                    </button>
                    <button onclick="callAPI('/batch_infer', 'POST', getBatchData())">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/>
                        </svg>
                        Batch Inference
                    </button>
                </div>
                <div class="output-section">
                    <div class="output-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                        </svg>
                        API Response:
                    </div>
                    <div id="loading" class="loading">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor" style="animation: spin 1s linear infinite;">
                            <path d="M12 2v4m0 12v4m4.5-14.5l-3.086 3.086M5.5 5.5l3.086 3.086M2 12h4m12 0h4m-3.086-8.914L18.5 5.5M5.5 18.5l3.086-3.086"/>
                        </svg>
                        Loading...
                    </div>
                    <pre id="output">Click a button above to test the API</pre>
                </div>
                <div id="status" class="status"></div>
            </div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        <script>
            async function callAPI(endpoint, method = 'GET', body = null) {
                const output = document.getElementById('output');
                const loading = document.getElementById('loading');
                const status = document.getElementById('status');

                loading.style.display = 'block';
                status.textContent = '';
                status.className = 'status';

                try {
                    const options = { method };
                    if (body) {
                        options.headers = { 'Content-Type': 'application/json' };
                        options.body = JSON.stringify(body, null, 2);
                    }
                    const response = await fetch(endpoint, options);
                    const data = await response.json();

                    output.textContent = JSON.stringify(data, null, 2);
                    status.textContent = `✅ Success (${response.status})`;
                    status.classList.add('success');
                } catch (error) {
                    output.textContent = `Error: ${error.message}`;
                    status.textContent = '❌ Error';
                    status.classList.add('error');
                } finally {
                    loading.style.display = 'none';
                }
            }

            function getSampleData() {
                return {
                    "drone_id": "drone-01",
                    "timestamp": new Date().toISOString(),
                    "rgb_anomaly_score": 0.78,
                    "thermal_heat_index": 85.0,
                    "human_signature_score": 0.12,
                    "environmental": {
                        "temperature_celsius": 43.5,
                        "humidity_pct": 31.2,
                        "co_ppm": 145.0,
                        "pressure_hpa": 975.0
                    }
                };
            }

            function getBatchData() {
                return {
                    "requests": [
                        {
                            "drone_id": "drone-01",
                            "timestamp": new Date().toISOString(),
                            "rgb_anomaly_score": 0.78,
                            "thermal_heat_index": 85.0,
                            "human_signature_score": 0.12,
                            "environmental": {
                                "temperature_celsius": 43.5,
                                "humidity_pct": 31.2,
                                "co_ppm": 145.0,
                                "pressure_hpa": 975.0
                            }
                        },
                        {
                            "drone_id": "drone-02",
                            "timestamp": new Date(Date.now() + 300000).toISOString(),
                            "rgb_anomaly_score": 0.9,
                            "thermal_heat_index": 20.0,
                            "human_signature_score": 0.8,
                            "environmental": {
                                "temperature_celsius": 25.0,
                                "humidity_pct": 60.0,
                                "co_ppm": 10.0,
                                "pressure_hpa": 1010.0
                            }
                        },
                        {
                            "drone_id": "drone-03",
                            "timestamp": new Date(Date.now() + 600000).toISOString(),
                            "rgb_anomaly_score": 0.1,
                            "thermal_heat_index": 30.0,
                            "human_signature_score": 0.05,
                            "environmental": {
                                "temperature_celsius": 20.0,
                                "humidity_pct": 80.0,
                                "co_ppm": 5.0,
                                "pressure_hpa": 1020.0
                            }
                        }
                    ]
                };
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)