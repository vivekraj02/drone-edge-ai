from pprint import pprint

from app.models.edge_fusion import EdgeFusionModel
from app.simulation import SensorSimulator


def main():
    simulator = SensorSimulator()
    model = EdgeFusionModel()
    sample = simulator.generate()
    result = model.predict(sample)

    print("Simulated sensor frame:")
    pprint(sample.dict())
    print("\nInference result:")
    pprint(result.dict())


if __name__ == "__main__":
    main()
