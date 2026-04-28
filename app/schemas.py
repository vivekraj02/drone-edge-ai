from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class EnvironmentalReadings(BaseModel):
    temperature_celsius: float = Field(..., ge=-40, le=85)
    humidity_pct: float = Field(..., ge=0, le=100)
    co_ppm: float = Field(..., ge=0)
    pressure_hpa: float = Field(..., ge=300, le=1200)


class InferenceRequest(BaseModel):
    drone_id: str
    timestamp: str
    rgb_anomaly_score: float = Field(..., ge=0, le=1)
    thermal_heat_index: float = Field(..., ge=0, le=150)
    human_signature_score: float = Field(..., ge=0, le=1)
    environmental: EnvironmentalReadings


class InferenceOutput(BaseModel):
    event: Literal["fire", "structural_damage", "human_presence", "normal"]
    confidence: float


class InferenceResponse(BaseModel):
    drone_id: str
    timestamp: str
    output: InferenceOutput


class SimulationResponse(BaseModel):
    input: InferenceRequest
    output: InferenceResponse


class BatchInferenceRequest(BaseModel):
    requests: list[InferenceRequest]


class BatchInferenceResponse(BaseModel):
    responses: list[InferenceResponse]
