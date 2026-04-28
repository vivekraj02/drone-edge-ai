from fastapi import FastAPI

from app.routes import router
from app.models.edge_fusion import EdgeFusionModel
from app.simulation import SensorSimulator


app = FastAPI(
    title="Drone Edge AI Simulation",
    version="0.1.0",
    description="Multi-sensor fusion edge inference API for UAV disaster monitoring.",
)


@app.on_event("startup")
async def startup_event():
    app.state.model = EdgeFusionModel()
    app.state.simulator = SensorSimulator()


app.include_router(router)
