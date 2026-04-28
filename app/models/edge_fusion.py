from app.schemas import InferenceRequest, InferenceOutput, InferenceResponse


class EdgeFusionModel:
    def __init__(self):
        self.weights = {
            "rgb": 0.3,
            "thermal": 0.4,
            "human": 0.3,
        }

    def predict(self, request: InferenceRequest) -> InferenceResponse:
        fused_score = (
            request.rgb_anomaly_score * self.weights["rgb"]
            + min(request.thermal_heat_index / 100.0, 1.0) * self.weights["thermal"]
            + request.human_signature_score * self.weights["human"]
        )
        event, confidence = self._decode_event(request, fused_score)
        return InferenceResponse(
            drone_id=request.drone_id,
            timestamp=request.timestamp,
            output=InferenceOutput(event=event, confidence=confidence),
        )

    def _decode_event(self, request: InferenceRequest, fused_score: float):
        heat = request.thermal_heat_index
        human = request.human_signature_score

        if heat > 70 and request.environmental.co_ppm > 100:
            event = "fire"
            confidence = min(0.75 + heat / 200 + request.rgb_anomaly_score * 0.2, 0.99)
        elif request.rgb_anomaly_score > 0.7 and request.environmental.pressure_hpa < 980:
            event = "structural_damage"
            confidence = min(0.45 + fused_score, 0.95)
        elif human > 0.6:
            event = "human_presence"
            confidence = min(0.4 + human * 0.5 + request.rgb_anomaly_score * 0.1, 0.95)
        else:
            event = "normal"
            confidence = 1.0 - min(fused_score, 0.8)

        return event, round(confidence, 2)
