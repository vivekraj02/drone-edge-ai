import random
from datetime import datetime, timezone

from app.schemas import EnvironmentalReadings, InferenceRequest


class SensorSimulator:
    def generate(self) -> InferenceRequest:
        payload = {
            "drone_id": f"drone-{random.randint(1, 12):02d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rgb_anomaly_score": round(random.uniform(0.0, 1.0), 2),
            "thermal_heat_index": round(random.uniform(15.0, 120.0), 1),
            "human_signature_score": round(random.uniform(0.0, 1.0), 2),
            "environmental": {
                "temperature_celsius": round(random.uniform(10.0, 55.0), 1),
                "humidity_pct": round(random.uniform(15.0, 95.0), 1),
                "co_ppm": round(random.uniform(0.0, 250.0), 1),
                "pressure_hpa": round(random.uniform(920.0, 1050.0), 1),
            },
        }
        return InferenceRequest(**payload)
