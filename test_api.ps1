# Test the Drone Edge AI API

# Activate virtual environment
.\venv\Scripts\activate

# Test health endpoint
Write-Host "Testing /health..."
Invoke-WebRequest -Uri http://127.0.0.1:8000/health -Method Get -UseBasicParsing | Select-Object -ExpandProperty Content

# Test simulate endpoint
Write-Host "`nTesting /simulate..."
Invoke-WebRequest -Uri http://127.0.0.1:8000/simulate -Method Get -UseBasicParsing | Select-Object -ExpandProperty Content

# Test infer endpoint with sample JSON
Write-Host "`nTesting /infer..."
$jsonBody = Get-Content -Path .\sample_request.json -Raw
Invoke-WebRequest -Uri http://127.0.0.1:8000/infer -Method Post -ContentType "application/json" -Body $jsonBody -UseBasicParsing | Select-Object -ExpandProperty Content

# Test batch infer endpoint
Write-Host "`nTesting /batch_infer..."
$batchBody = Get-Content -Path .\batch_request.json -Raw
Invoke-WebRequest -Uri http://127.0.0.1:8000/batch_infer -Method Post -ContentType "application/json" -Body $batchBody -UseBasicParsing | Select-Object -ExpandProperty Content