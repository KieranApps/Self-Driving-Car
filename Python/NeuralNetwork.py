import json
import numpy as np

import NetworkLayout as NL

class NeuralNetwork():

    def __init__(self):
        self.networkLayout = NL.NetworkLayout()
    
    def reset(self, time, distance, DELIMITER):
        # Find fitness of current Car in the generation, and save this to file

        # Increase the car/Load a new network, OR, run crossover for a new generation (this includes picking parents and comparing the current best NN)
        if(self.networkLayout.currentCar == 50):
            print('Generation Finished. Perform Crossover.')
        else:
            self.networkLayout.currentCar += 1

        status = {
            "finishedReset": True
        }
        return json.dumps(status) + DELIMITER

    def processInputs(self, jsonData, DELIMITER):
        carInputs = {
            "acceleratorInput": 1,
            "turnInput": 0
        }
        return json.dumps(carInputs) + DELIMITER


    def forwardPass(self):
        print()

    def findFitness(self):
        print()

    def performCrossover(self):
        print()