import json

class NeuralNetwork():
    def __init__(self):
        pass
    
    def reset(self, DELIMITER):
        # Load a new network OR perform cross over as part of the Genetic Algorithm at the end of the generation
        status = {
            "reset": True
        }
        return json.dumps(status) + DELIMITER

    def processInputs(self, jsonData, DELIMITER):
        carInputs = {
            "acceleratorInput": 1,
            "turnInput": 0
        }
        return json.dumps(carInputs) + DELIMITER