import json
from random import random
import numpy as np
import math

import NetworkLayout as NL

POTENTIAL_MAX_SPEED = 65
POTENTIAL_MAX_FRONT = 400 # Longest straights
POTENTIAL_MAX_LEFT_RIGHT = 10 # Track width
POTENTIAL_MAX_23 = 250 # Max distance will be hit going around a corner, and onto a long straight
POTENTIAL_MAX_45 = 250 # Max distance will be hit going around a corner, and onto a long straight
POTENTIAL_MAX_68 = 250 # Max distance will be hit going around a corner, and onto a long straight

class NeuralNetwork():
    def __init__(self):
        self.networkLayout = NL.NetworkLayout()
        # self.networkLayout.findFirstNotRunCar()
        self.networkLayout.loadNetwork()

    def reset(self, time, distance, DELIMITER):
        # Find fitness of current Car in the generation, and save this to file

        # Increase the car/Load a new network, OR, run crossover for a new generation (this includes picking parents and comparing the current best NN)
        if(self.networkLayout.isEndOfGeneration()):
            print('Generation Finished. Find Parents.')
            self.networkLayout.findParents()
            if self.networkLayout.stopTraining == True:
                return True

            self.performCrossover()
        else:
            self.findFitness(time, distance)
            self.networkLayout.currentCar += 1
            self.networkLayout.loadNetwork()

        status = {
            "finishedReset": True
        }

        return json.dumps(status) + DELIMITER

    def processInputs(self, jsonData, DELIMITER):
        inputsArray = self.forwardPass(jsonData)
        carInputs = {
            "acceleratorInput": inputsArray[0],
            "turnInput": inputsArray[1]
        }
        return json.dumps(carInputs) + DELIMITER


    def forwardPass(self,  jsonData):
        # Pull jsonData out into variables.
        # Normalize inputs
        speed = jsonData['speed'] / POTENTIAL_MAX_SPEED
        distanceToFront = jsonData['distanceInFront'] / POTENTIAL_MAX_FRONT
        distanceToLeft = jsonData['distanceToLeft'] / POTENTIAL_MAX_LEFT_RIGHT
        distance23Left = jsonData['distance23Left'] / POTENTIAL_MAX_23
        distance45Left = jsonData['distance45Left'] / POTENTIAL_MAX_45
        distance68Left = jsonData['distance68Left'] / POTENTIAL_MAX_68
        distanceToRight = jsonData['distanceToRight'] / POTENTIAL_MAX_LEFT_RIGHT
        distance23Right = jsonData['distance23Right'] / POTENTIAL_MAX_23
        distance45Right = jsonData['distance45Right'] / POTENTIAL_MAX_45
        distance68Right = jsonData['distance68Right'] / POTENTIAL_MAX_68
        

        inputArray = np.array([speed, distanceToFront, distanceToLeft, distance23Left, distance45Left, distance68Left, distanceToRight, distance23Right, distance45Right, distance68Right])
        
        resultsOne = []
        # Calculate the first layer
        for i in range(0, self.networkLayout.hiddenLayerOneSize):
            combinedArray =  np.array([self.networkLayout.weightsOne[i], inputArray])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) * self.networkLayout.biasesOne[i]
            sigmoidResult = 1/(1 + math.e**(-result))
            resultsOne.append(sigmoidResult)

        resultsTwo = []
        for i in range(self.networkLayout.hiddenLayerTwoSize):
            combinedArray =  np.array([self.networkLayout.weightsTwo[i], resultsOne])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) * self.networkLayout.biasesTwo[i]
            sigmoidResult = 1/(1 + math.e**(-result))
            resultsTwo.append(sigmoidResult)
        
        resultsThree = []
        for i in range(self.networkLayout.hiddenLayerThreeSize):
            combinedArray =  np.array([self.networkLayout.weightsThree[i], resultsTwo])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) * self.networkLayout.biasesThree[i]
            sigmoidResult = 1/(1 + math.e**(-result))
            resultsThree.append(sigmoidResult)
        
        resultsFour = []
        for i in range(self.networkLayout.hiddenLayerFourSize):
            combinedArray =  np.array([self.networkLayout.weightsFour[i], resultsThree])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) * self.networkLayout.biasesFour[i]
            sigmoidResult = 1/(1 + math.e**(-result))
            resultsFour.append(sigmoidResult)
        
        # Calculate the output
        resultsForInput = []
        for i in range(0, self.networkLayout.outputLayerSize):
            combinedArray =  np.array([self.networkLayout.weightsFive[i], resultsFour])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) * self.networkLayout.biasesFive[i]
            resultProcessedForCarInput = 2*((1/(1 + math.e**(-result))) - 0.5)
            resultsForInput.append(resultProcessedForCarInput)
        
        return resultsForInput

    def findFitness(self, time, distance):
        # The higher the speed, the better the 'fitness'
        # Make the distance slightly more valuable than the speed (a car that makes it further, but slightly slower, is better than a fast car that doesnt get that far)
        # These values will be large since the distance measures up to and above 30000
        carFitness = (distance*1.5)/(time*1.25)
        self.networkLayout.saveFitnessValue(carFitness)

    def performCrossover(self):
        print('Performing Crossover...')
        # This function will be the one to run the genetic algorithm of mixing other NNs when implemented
        # Only need two parents, from the network layout (can use local variable, or load in from file)
        parentOne = {}
        parentTwo = {}
        with open('./Cars/parentOne.json') as parentOneFile:
                parentOne = json.load(parentOneFile)
        with open('./Cars/parentTwo.json') as parentTwoFile:
                parentTwo = json.load(parentTwoFile)
        for i in range(1, self.generationSize + 1):
            print('Get the parents and crossover')
            layerChoseToSplit = random.randrange(1, 6) # Needs to be 6, so 5 can be chosen. Just how python works
            biasesOrWeightsToSplit = random.randrange(1, 3)

            # After, then select a ranum number up to the size of the layer chosen 
                # i.e 10 for biases on One, or 10*10 for weightsOne, or 10*7 for weightsTwo etc
                # Should be able to use array lengths to find exacts. i.e, length of array of arrays, length of each array within array. Times together
                # Or can use same way as used for generation, should work also. Just means more changes if layout changes

            
            # Then pick either parent to be slit for first half, other parent split for second 


            # Split the parents along this set. Randomly pick either parent 1 or 2 to be the first 'half' and second 'half'?
            # OR Pick the parent One to be the bigger side

            # Merge the two sets

            # Randomly generate a number, to determine weather we mutate a value