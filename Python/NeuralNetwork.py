import json
import random
import numpy as np
import math

import NetworkLayout as NL

MUTATE_PERCENTAGE = 101
POTENTIAL_MAX_SPEED = 65
POTENTIAL_MAX_FRONT = 400 # Longest straights
POTENTIAL_MAX_LEFT_RIGHT = 10 # Track width
POTENTIAL_MAX_23 = 250 # Max distance will be hit going around a corner, and onto a long straight
POTENTIAL_MAX_45 = 250 # Max distance will be hit going around a corner, and onto a long straight
POTENTIAL_MAX_68 = 250 # Max distance will be hit going around a corner, and onto a long straight

class NeuralNetwork():
    def __init__(self):
        self.networkLayout = NL.NetworkLayout()
        self.networkLayout.loadNetwork()

    def reset(self, time, distance, DELIMITER):
        # Find fitness of current Car in the generation, and save this to file

        if self.networkLayout.bestCarOnly == True:
            ## Dont bother with anything, just keep the best network only
            status = {
                "finishedReset": True
            }
            return json.dumps(status) + DELIMITER

        # Increase the car/Load a new network, OR, run crossover for a new generation (this includes picking parents and comparing the current best NN)
        if(self.networkLayout.isEndOfGeneration()):
            print('Generation Finished. Find Parents.')
            self.networkLayout.findParents()

            self.performCrossover()
            self.networkLayout.currentCar = 1
            self.networkLayout.loadNetwork()
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
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) + self.networkLayout.biasesOne[i]
            sigmoidResult = 2*((1/(1 + math.e**(-result))) - 0.5)
            resultsOne.append(sigmoidResult)

        resultsTwo = []
        for i in range(self.networkLayout.hiddenLayerTwoSize):
            combinedArray =  np.array([self.networkLayout.weightsTwo[i], resultsOne])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) + self.networkLayout.biasesTwo[i]
            sigmoidResult = 2*((1/(1 + math.e**(-result))) - 0.5)
            resultsTwo.append(sigmoidResult)

        resultsThree = []
        for i in range(self.networkLayout.hiddenLayerThreeSize):
            combinedArray =  np.array([self.networkLayout.weightsThree[i], resultsTwo])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) + self.networkLayout.biasesThree[i]
            sigmoidResult = 2*((1/(1 + math.e**(-result))) - 0.5)
            resultsThree.append(sigmoidResult)
        
        resultsForInput = []
        for i in range(self.networkLayout.outputLayerSize):
            combinedArray =  np.array([self.networkLayout.weightsFour[i], resultsThree])
            result = np.sum(combinedArray.prod(axis=0, dtype=np.float32)) + self.networkLayout.biasesFour[i]
            sigmoidResult = 2*((1/(1 + math.e**(-result))) - 0.5)
            resultsForInput.append(sigmoidResult)
        
        return resultsForInput

    def findFitness(self, time, distance):
        distanceFitness = (distance/10 - time) # This fitness was used for the fitness of distance
        speedFitness = (distance/10)/time # This fitness is used for speed fitness
        carFitness = distanceFitness + speedFitness # Combine them both
        self.networkLayout.saveFitnessValue(carFitness)

    def performCrossover(self):
        print('Performing Crossover...')
        parentOne = {}
        parentTwo = {}
        with open('./Cars/parentOne.json') as parentOneFile:
                parentOne = json.load(parentOneFile)
        with open('./Cars/parentTwo.json') as parentTwoFile:
                parentTwo = json.load(parentTwoFile)

        # Use Uniform Crossover
        # 50/50 Probability if the current individual weight or bias is taken from parent one or two
        for i in range(1, self.networkLayout.generationSize + 1):            
            weightsOne = [[-1 for n in range(self.networkLayout.inputSize)] for m in range(self.networkLayout.hiddenLayerOneSize)]
            weightsTwo = [[-1 for n in range(self.networkLayout.hiddenLayerOneSize)] for m in range(self.networkLayout.hiddenLayerTwoSize)]
            weightsThree = [[-1 for n in range(self.networkLayout.hiddenLayerTwoSize)] for m in range(self.networkLayout.hiddenLayerThreeSize)]
            weightsFour = [[-1 for n in range(self.networkLayout.hiddenLayerThreeSize)] for m in range(self.networkLayout.outputLayerSize)]

            biasesOne = []
            biasesTwo = []
            biasesThree = []
            biasesFour = []

            # First Layer
            for j in range(0, self.networkLayout.hiddenLayerOneSize):
                mutateProbBias = random.randrange(1, MUTATE_PERCENTAGE)
                if mutateProbBias == 1:
                    # We use an extension of the bit flip mutation to be a 'Random Reset' of a randomly chosen gene
                    newNum = np.random.uniform(-2, 2, 1)[0]
                    biasesOne.append(newNum)
                else:
                    biasProb = random.randrange(1, 11)
                    if biasProb > 5:
                        # Take parent 1
                        biasesOne.append(parentOne['biasesOne'][j])
                    else:
                        # Take parent 2
                        biasesOne.append(parentTwo['biasesOne'][j])

                # Create the weights array
                for k in range(0, self.networkLayout.inputSize):
                    mutateProbWeight = random.randrange(1, MUTATE_PERCENTAGE)
                    if mutateProbWeight == 1:
                        newNum = np.random.uniform(-2, 2, 1)[0]
                        weightsOne[j][k] = newNum
                    else:
                        weightsProb = random.randrange(1, 11)
                        if weightsProb > 5:
                            #Take parent 1
                            weightsOne[j][k] = parentOne['weightsOne'][j][k]
                        else:
                            #Take parent 2
                            weightsOne[j][k] = parentTwo['weightsOne'][j][k]
            
            # Second Layer
            for j in range(0, self.networkLayout.hiddenLayerTwoSize):
                mutateProbBias = random.randrange(1, MUTATE_PERCENTAGE)
                if mutateProbBias == 1:
                    newNum = np.random.uniform(-2, 2, 1)[0]
                    biasesTwo.append(newNum)
                else:
                    biasProb = random.randrange(1, 11)
                    if biasProb > 5:
                        biasesTwo.append(parentOne['biasesTwo'][j])
                    else:
                        biasesTwo.append(parentTwo['biasesTwo'][j])

                for k in range(0, self.networkLayout.hiddenLayerOneSize):
                    mutateProbWeight = random.randrange(1, MUTATE_PERCENTAGE)
                    if mutateProbWeight == 1:
                        newNum = np.random.uniform(-2, 2, 1)[0]
                        weightsTwo[j][k] = newNum
                    else:
                        weightsProb = random.randrange(1, 11)
                        if weightsProb > 5:
                            weightsTwo[j][k] = parentOne['weightsTwo'][j][k]
                        else:
                            weightsTwo[j][k] = parentTwo['weightsTwo'][j][k]

            # Third Layer
            for j in range(0, self.networkLayout.hiddenLayerThreeSize):
                mutateProbBias = random.randrange(1, MUTATE_PERCENTAGE)
                if mutateProbBias == 1:
                    newNum = np.random.uniform(-2, 2, 1)[0]
                    biasesThree.append(newNum)
                else:
                    biasProb = random.randrange(1, 11)
                    if biasProb > 5:
                        biasesThree.append(parentOne['biasesThree'][j])
                    else:
                        biasesThree.append(parentTwo['biasesThree'][j])

                for k in range(0, self.networkLayout.hiddenLayerTwoSize):
                    mutateProbWeight = random.randrange(1, MUTATE_PERCENTAGE)
                    if mutateProbWeight == 1:
                        newNum = np.random.uniform(-2, 2, 1)[0]
                        weightsThree[j][k] = newNum
                    else:
                        weightsProb = random.randrange(1, 11)
                        if weightsProb > 5:
                            weightsThree[j][k] = parentOne['weightsThree'][j][k]
                        else:
                            weightsThree[j][k] = parentTwo['weightsThree'][j][k]
                
                # Fourth Layer
                # Third Layer
            for j in range(0, self.networkLayout.outputLayerSize):
                mutateProbBias = random.randrange(1, MUTATE_PERCENTAGE)
                if mutateProbBias == 1:
                    newNum = np.random.uniform(-2, 2, 1)[0]
                    biasesFour.append(newNum)
                else:
                    biasProb = random.randrange(1, 11)
                    if biasProb > 5:
                        biasesFour.append(parentOne['biasesFour'][j])
                    else:
                        biasesFour.append(parentTwo['biasesFour'][j])

                for k in range(0, self.networkLayout.hiddenLayerThreeSize):
                    mutateProbWeight = random.randrange(1, MUTATE_PERCENTAGE)
                    if mutateProbWeight == 1:
                        newNum = np.random.uniform(-2, 2, 1)[0]
                        weightsFour[j][k] = newNum
                    else:
                        weightsProb = random.randrange(1, 11)
                        if weightsProb > 5:
                            weightsFour[j][k] = parentOne['weightsFour'][j][k]
                        else:
                            weightsFour[j][k] = parentTwo['weightsFour'][j][k]
            
            carData = {
                "weightsOne": weightsOne,
                "biasesOne": biasesOne,
                "weightsTwo": weightsTwo,
                "biasesTwo": biasesTwo,
                "weightsThree": weightsThree,
                "biasesThree": biasesThree,
                "weightsFour": weightsFour,
                "biasesFour": biasesFour,
                "fitnessValue": 0
            }

            # Format json
            formattedCarObject = json.dumps(carData, indent = 4)
            with open('./Cars/car' + str(i) + '.json', 'w') as carFile:
                carFile.write(formattedCarObject)
        
        # Update generation number
        with open('./Cars/generations_counter.json') as genCountFile:
                countObj = json.load(genCountFile)
        newGen = countObj['generation'] + 1
        newGenCount = {
            "generation": newGen
        }
        formattedNewGenCount = json.dumps(newGenCount, indent = 4)
        with open('./Cars/generations_counter.json', 'w') as newGenFile:
                newGenFile.write(formattedNewGenCount)