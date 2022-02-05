import json
import numpy as np
import math

import NetworkLayout as NL

class NeuralNetwork():

    def __init__(self):
        self.networkLayout = NL.NetworkLayout()
        # self.networkLayout.findFirstNotRunCar()
        self.networkLayout.loadNetwork()
            
    def reset(self, time, distance, DELIMITER):
        # Find fitness of current Car in the generation, and save this to file

        # Increase the car/Load a new network, OR, run crossover for a new generation (this includes picking parents and comparing the current best NN)
        if(self.networkLayout.currentCar == 50):
            print('Generation Finished. Perform Crossover.')
        else:
            self.networkLayout.currentCar += 1
            self.networkLayout.loadNetwork()

        status = {
            "finishedReset": True
        }
        return json.dumps(status) + DELIMITER

    def processInputs(self, jsonData, DELIMITER):
        self.forwardPass(jsonData)
        carInputs = {
            "acceleratorInput": 1,
            "turnInput": 0
        }
        return json.dumps(carInputs) + DELIMITER


    def forwardPass(self,  jsonData):
        # Pull jsonData out into variables.
        speed = round(jsonData['speed'], 3)
        distanceToFront = round(jsonData['distanceInFront'])
        distanceToLeft = round(jsonData['distanceToLeft'])
        distance23Left = round(jsonData['distance23Left'])
        distance45Left = round(jsonData['distance45Left'])
        distance68Left = round(jsonData['distance68Left'])
        distanceToRight = round(jsonData['distanceToRight'])
        distance23Right = round(jsonData['distance23Right'])
        distance45Right = round(jsonData['distance45Right'])
        distance68Right = round(jsonData['distance68Right'])
        inputArray = [speed, distanceToFront, distanceToLeft, distance23Left, distance45Left, distance68Left, distanceToRight, distance23Right, distance45Right, distance68Right]
        resultsOne = []
        weightNumber = 0

        # Calculate the first layer
        # Use matrix multiplication??? Using numpy????

        for i in range(0, self.networkLayout.hiddenLayerOneSize - 1):
            result = inputArray.dot(self.networkLayout.weightsOne[weightNumber]) # CHAGE WEIGHTS TO BE 2D ARRAYS [[first set], [second set]...]
            weightNumber += 1
            result = result * self.networkLayout.biasesOne[i]
            finalResult = 2*((1/(1 + np.exp(-result))) - 0.5)  # Applies forward pass formula
            resultsOne.append(finalResult)

        # Reset weight number for next layer
        weightNumber = 0
        for i in range(self.networkLayout.hiddenLayerTwoSize  - 1):
            print()

        # Reset weight number for next layer
        weightNumber = 0
        for i in range(self.networkLayout.hiddenLayerThreeSize  - 1):
            print()

        # Reset weight number for next layer
        weightNumber = 0
        for i in range(self.networkLayout.hiddenLayerFourSize  - 1):
            print()

        # Calculate the output

        # Use the weights and biases from layout and these variables to process

    def findFitness(self):
        print()

    def performCrossover(self):
        allNetworks = self.networkLayout.loadAllNetworks()
        print()