import numpy as np
import json

class NetworkLayout():

    def __init__(self):

        self.bestCarOnly = False

        # These layer sizes can be tweaked to create a better functioning Neural Network
        self.inputSize = 10
        self.hiddenLayerOneSize = 10
        self.hiddenLayerTwoSize = 7
        self.hiddenLayerThreeSize = 4
        self.outputLayerSize = 2
        
        # These will be the arrays of all weights and biases (more can be added or taken away to perfect layout)
        self.weightsOne = []
        self.biasesOne = []
        self.weightsTwo = []
        self.biasesTwo = []
        self.weightsThree = []
        self.biasesThree = []
        self.weightsFour = []
        self.biasesFour = []

        # This will be used to keep track of which NN we are currently using
        self.currentCar = 1
        self.generationSize = 50
        self.currentNotBetterThanBest = 0

        # Store current parent cars data for comparisons
        self.parentOne = {}
        self.parentTwo = {}

        # There will be 50 cars per generation (50 csv files) and 2 files for the parents of the current running generation (just incase something goes wrong while generating, we can do it again)
        # And there will be 1 file that holds the current best (most fit) NN
        # A total of 253 sheets

    def createRandomValues(self):
        print('Creating Networks...')
        # Create 50 networks, so that per generation there are 50 cars
        # Use index start of 1 for easy reading and understanding
        for i in range(1, self.generationSize + 1):
            weightsOne = []
            for j in range(0, self.hiddenLayerOneSize):
                weightsOne.append(np.random.uniform(-2, 2, self.inputSize).tolist())
            biasesOne = np.random.uniform(-2, 2, self.hiddenLayerOneSize)

            weightsTwo = []
            for j in range(0, self.hiddenLayerTwoSize):
                weightsTwo.append(np.random.uniform(-2, 2, self.hiddenLayerOneSize).tolist())
            biasesTwo = np.random.uniform(-2, 2, self.hiddenLayerTwoSize)

            weightsThree = []
            for j in range(0, self.hiddenLayerThreeSize):
                weightsThree.append(np.random.uniform(-2, 2, self.hiddenLayerTwoSize).tolist())
            biasesThree = np.random.uniform(-2, 2, self.hiddenLayerThreeSize)

            weightsFour = []
            for j in range(0, self.outputLayerSize):
                weightsFour.append(np.random.uniform(-2, 2, self.hiddenLayerThreeSize).tolist())
            biasesFour = np.random.uniform(-2, 2, self.outputLayerSize)

            carData = {
                "weightsOne": weightsOne,
                "biasesOne": biasesOne.tolist(),
                "weightsTwo": weightsTwo,
                "biasesTwo": biasesTwo.tolist(),
                "weightsThree": weightsThree,
                "biasesThree": biasesThree.tolist(),
                "weightsFour": weightsFour,
                "biasesFour": biasesFour.tolist(),
                "fitnessValue": 0
            }

            # Format json
            formattedCarObject = json.dumps(carData, indent = 4)
            with open('./Cars/car' + str(i) + '.json', 'w') as carFile:
                carFile.write(formattedCarObject)
            initGen = {
                "generation": 1
            }
            formattedInitGen = json.dumps(initGen, indent = 4)
            with open('./Cars/generations_counter.json', 'w') as genFile:
                genFile.write(formattedInitGen)
            initBest = {
                "fitnessValue": -1
            }
            formattedInitBest = json.dumps(initBest, indent = 4)
            with open('./Cars/BestCar.json', 'w') as bestFile:
                bestFile.write(formattedInitBest)
    
    '''
        loadNetwork loads a current network. All other Car/Generation handling (incrementing and if complete, starting crossover etc...) and checking for if the Car has alrady been evaluated
        will be completed in seperate functions
    '''
    def loadNetwork(self):
        fileName = ''
        if self.bestCarOnly == True:
            print('Loading BEST Network...')
            fileName = './Cars/BestCar.json'
        else:
            print('Loading New Network...', self.currentCar)
            fileName = './Cars/car' + str(self.currentCar) + '.json'
        
        with open(fileName) as carFile:
            carObject = json.load(carFile)

        self.weightsOne = np.array(carObject['weightsOne'])
        self.biasesOne = np.array(carObject['biasesOne'])
        self.weightsTwo = np.array(carObject['weightsTwo'])
        self.biasesTwo = np.array(carObject['biasesTwo'])
        self.weightsThree = np.array(carObject['weightsThree'])
        self.biasesThree = np.array(carObject['biasesThree'])
        self.weightsFour = np.array(carObject['weightsFour'])
        self.biasesFour = np.array(carObject['biasesFour'])

    def findParents(self):
        print('Finding Parents...')
        # Since we're finding parents, the locally stored need to be reset (the parents from the last round will be stored in file anyway)
        self.parentOne = {
            "weightsOne": [],
            "biasesOne": [],
            "weightsTwo": [],
            "biasesTwo": [],
            "weightsThree": [],
            "biasesThree": [],
            "weightsFour": [],
            "biasesFour": [],
            "fitnessValue": float('-inf')
        }
        self.parentTwo = {
            "weightsOne": [],
            "biasesOne": [],
            "weightsTwo": [],
            "biasesTwo": [],
            "weightsThree": [],
            "biasesThree": [],
            "weightsFour": [],
            "biasesFour": [],
            "fitnessValue": float('-inf')
        }
        
        # If the current car is better than both parents, move parent 1 to parent 2 and assign new best to parent 1
        # If its only better than parent 2, then only assign to parent two
        currentCar = {}
        for i in range(1, self.generationSize + 1):
            with open('./Cars/car' + str(i) + '.json') as carFile:
                currentCar = json.load(carFile)
            # If greater than one, its greater than both
            if float(currentCar['fitnessValue']) > self.parentOne['fitnessValue']:
                self.parentTwo = self.parentOne
                self.parentOne = currentCar
            elif float(currentCar['fitnessValue']) > self.parentTwo['fitnessValue']:
                self.parentTwo = currentCar
        
        # Save the parents to file
        formattedParentOne = json.dumps(self.parentOne, indent = 4)
        formatedParentTwo = json.dumps(self.parentTwo, indent = 4)
        with open('./Cars/parentOne.json', 'w') as carFile:
            carFile.write(formattedParentOne)
        with open('./Cars/parentTwo.json', 'w') as carFile:
            carFile.write(formatedParentTwo)
        
        # Compare parent 1 to the current best car yet
        self.compareToBest()

        if(self.currentNotBetterThanBest  == 5):
            print('Previous 5 generations did not produce a better car than the previous best. So we stop here')
            self.stopTraining = True

    def compareToBest(self):
        print('Comparing to Best...')
        bestCar = {}
        with open('./Cars/BestCar.json') as bestCarFile:
                bestCar = json.load(bestCarFile)
        # Should only need to compare parent 1 to current best
        # If file doesnt exist, auto save parent 1
        # Best car is init to -1 so its guarunteed to save the best on first run
        if float(bestCar['fitnessValue']) < self.parentOne['fitnessValue']:
            self.currentNotBetterThanBest = 0
            formattedNewBest = json.dumps(self.parentOne, indent = 4)
            with open('./Cars/BestCar.json', 'w') as newBestCarFile:
                newBestCarFile.write(formattedNewBest)
        else:
            self.currentNotBetterThanBest += 1

    def saveFitnessValue(self, fitness):
        print('Saving Fitness...')
        carData = {
            "weightsOne": self.weightsOne.tolist(),
            "biasesOne": self.biasesOne.tolist(),
            "weightsTwo": self.weightsTwo.tolist(),
            "biasesTwo": self.biasesTwo.tolist(),
            "weightsThree": self.weightsThree.tolist(),
            "biasesThree": self.biasesThree.tolist(),
            "weightsFour": self.weightsFour.tolist(),
            "biasesFour": self.biasesFour.tolist(),
            "fitnessValue": fitness
        }
        # Format json
        formattedCarObject = json.dumps(carData, indent = 4)
        with open('./Cars/car' + str(self.currentCar) + '.json', 'w') as carFile:
            carFile.write(formattedCarObject)

    def isEndOfGeneration(self):
        return self.currentCar == self.generationSize



# Run this file seperately to generate the initial random weights and biases
#NL = NetworkLayout()
#NL.loadNetwork()
#NL.createRandomValues()