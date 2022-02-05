import numpy as np
import json

class NetworkLayout():

    def __init__(self):
        # These layer sizes can be tweaked to create a better functioning Neural Network
        self.inputSize = 10
        self.hiddenLayerOneSize = 10
        self.hiddenLayerTwoSize = 7
        self.hiddenLayerThreeSize = 5
        self.hiddenLayerFourSize = 3

        # These will be the arrays of all weights and biases (more can be added or taken away to perfect layout)
        self.weightsOne = []
        self.biasesOne = []
        self.weightsTwo = []
        self.biasesTwo = []
        self.weightsThree = []
        self.biasesThree = []
        self.weightsFour = []
        self.biasesFour = []
        self.weightsFive = []
        self.biasesFive = []

        # This will be used to keep track of which NN we are currently using
        self.currentCar = 1

        # There will be 50 cars per generation (50 csv files) and 2 files for the parents of the current running generation (just incase something goes wrong while generating, we can do it again)
        # And there will be 1 file that holds the current best (most fit) NN
        # A total of 253 sheets

    def createRandomValues(self):
        print('Creating Networks...')
        
        # There are 10 inputs, and the first hidden layer has to have layerSize^10 connections, and then layerSize^prevLayerSize
        # Create 50 networks, so that per generation there are 50 cars
        # Use index start of 1 for easy reading and understanding
        for i in range(1, 51):
            weightsOne = []
            for j in range(0, self.hiddenLayerOneSize - 1):
                weightsOne.append(np.random.rand(self.inputSize).tolist())
            biasesOne = np.random.rand(self.hiddenLayerOneSize)

            weightsTwo = []
            for j in range(0, self.hiddenLayerTwoSize - 1):
                weightsTwo.append(np.random.rand(self.hiddenLayerOneSize).tolist())
            biasesTwo = np.random.rand(self.hiddenLayerTwoSize)

            weightsThree = []
            for j in range(0, self.hiddenLayerThreeSize - 1):
                weightsThree.append(np.random.rand(self.hiddenLayerTwoSize).tolist())
            biasesThree = np.random.rand(self.hiddenLayerThreeSize)

            weightsFour = []
            for j in range(0, self.hiddenLayerFourSize - 1):
                weightsFour.append(np.random.rand(self.hiddenLayerThreeSize).tolist())
            biasesFour = np.random.rand(self.hiddenLayerFourSize)

            # Output will be of two so that there is the acceleration value turn angle
            weightsFive = []
            for j in range(0, 2):
                weightsFive.append(np.random.rand(self.hiddenLayerFourSize).tolist())
            biasesFive = np.random.rand(2)

            carData = {
                "weightsOne": weightsOne,
                "biasesOne": biasesOne.tolist(),
                "weightsTwo": weightsTwo,
                "biasesTwo": biasesTwo.tolist(),
                "weightsThree": weightsThree,
                "biasesThree": biasesThree.tolist(),
                "weightsFour": weightsFour,
                "biasesFour": biasesFour.tolist(),
                "weightsFive": weightsFive,
                "biasesFive": biasesFive.tolist(),
                "fitnessValue": None
            }

            # Format json 
            formattedCarObject = json.dumps(carData, indent = 4)
            with open('./Cars/car' + str(i) + '.json', 'w') as carFile:
                carFile.write(formattedCarObject)
    
    '''
        loadNetwork loads a current network. All other Car/Generation handling (incrementing and if complete, starting crossover etc...) and checking for if the Car has alrady been evaluated
        will be completed in seperate functions
    '''
    def loadNetwork(self):
        print('Loading New Network...')
        with open('./Cars/car' + str(self.currentCar) + '.json') as carFile:
            carObject = json.load(carFile)

        self.weightsOne = carObject['weightsOne']
        self.weightsTwo = carObject['weightsTwo']
        self.biasesTwo = carObject['biasesTwo']
        self.weightsThree = carObject['weightsThree']
        self.biasesThree = carObject['biasesThree']
        self.weightsFour = carObject['weightsFour']
        self.biasesFour = carObject['biasesFour']
        self.weightsFive = carObject['weightsFive']

    def findFirstNotRunCar(self):
        print('Finding Car to Start With...')

    def findParents(self):
        print('Finding Parents...')

    def compareToBest(self):
        print('Comparing to Best...')

    def saveParentNetworks(self):
        print('Saving Parent Networks...')

    def saveBestNetwork(self):
        print('Saving Best Network...')

    def saveNewGenerationCar(self, carNumber):
        print('Saving New Car...')

    def saveFitnessValue(self, car, fitnessValue):
        print('Saving Fitness...')

    def loadAllNetworks(self):
        print('Loading all Networks for Crossover...')
        # Return all as Large JSON Object with key being file name (car number)

    def isEndOfGeneration(self):
        return self.currentCar == 50



# Run this file seperately to generate the initial random weights and biases
NL = NetworkLayout()
NL.loadNetwork()
#NL.createRandomValues()