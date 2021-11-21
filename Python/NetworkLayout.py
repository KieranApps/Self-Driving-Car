import pandas as pd
import numpy as np
import math

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

        # This will be used to keep track of which NN we are currently using
        self.currentCar = 1

        # There will be 250 cars per generation (250 csv files) and 2 files for the parents of the current running generation (just incase something goes wrong while generating, we can do it again)
        # And there will be 1 file that holds the current best (most fit) NN
        # A total of 253 sheets

    def createRandomValues(self):
        print('Creating Networks...')
        
        # There are 10 inputs, and the first hidden layer has to have layerSize^10 connections, and then layerSize^prevLayerSize
        # Create 250 networks, so that per generation there are 250 cars
        # Use index start of 1 for easy reading and understanding
        for i in range(1, 251):
            # Since its easier to store and read multiple 1D arrays in a csv, they will be used, rather than a 2d array for the hidden nodes
            # These could potentially be converted into a 2d array upon loading and for use in processing, however, depending on performance gains

            # 2d/3d array example
            # [
            #   [ <-- Denotes layer 1
            #       [bias, weight, weight], <- bias of current node, one weight for each node in the next layer (could split biases out and just have 2d of weights for easier understanding)
            #       [bias, weight, weight], <- same as above, node bias with weights to all next layer nodes
            #   ],
            #   [...Layer 2...],
            #   []...
            # ]
            weightsOne = np.random.rand(self.inputSize * self.hiddenLayerOneSize)
            biasesOne = np.random.rand(self.hiddenLayerOneSize)

            weightsTwo = np.random.rand(self.hiddenLayerOneSize * self.hiddenLayerTwoSize)
            biasesTwo = np.random.rand(self.hiddenLayerTwoSize)

            weightsThree = np.random.rand(self.hiddenLayerTwoSize * self.hiddenLayerThreeSize)
            biasesThree = np.random.rand(self.hiddenLayerThreeSize)

            weightsFour = np.random.rand(self.hiddenLayerThreeSize * self.hiddenLayerFourSize)
            biasesFour = np.random.rand(self.hiddenLayerFourSize)

            # Output will be of two so that there is the acceleration value turn angle
            weightsFive = np.random.rand(self.hiddenLayerFourSize * 2)

            data = pd.DataFrame([
                weightsOne, biasesOne, weightsTwo, biasesTwo,
                weightsThree, biasesThree, weightsFour, biasesFour,
                weightsFive, ['']
            ])
            data.index = ['Weights_1','Biases_1','Weights_2','Biases_2','Weights_3','Biases_3','Weights_4','Biases_4','Weights_5','FitnessValue']
            # All car networks are stored in the Car directory
            data.to_csv('./Cars/car' + str(i) + '.txt')
    
    '''
        loadNetwork loads a current network. All other Car/Generation handling (incrementing and if complete, starting crossover etc...) and checking for if the Car has alrady been evaluated
        will be completed in seperate functions
    '''
    def loadNetwork(self):
        # Remove the index tag, and all NaN values
        def returnOnlyNumericValues(value):
            valueAsFloat = ''
            try:
                valueAsFloat = float(value)
            except:
                valueAsFloat = math.nan
            
            return not math.isnan(valueAsFloat)

        print('Loading New Network...')
        network = pd.read_csv('./Cars/car' + str(self.currentCar) + '.txt')

        for entry in np.asarray(network):
            if entry[0] == 'Weights_1':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.weightsOne = filteredValues

            elif entry[0] == 'Biases_1':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.biasesOne = filteredValues

            elif entry[0] == 'Weights_2':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.weightsTwo = filteredValues

            elif entry[0] == 'Biases_2':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.biasesTwo = filteredValues

            elif entry[0] == 'Weights_3':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.weightsThree = filteredValues

            elif entry[0] == 'Biases_3':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.biasesThree = filteredValues

            elif entry[0] == 'Weights_4':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.weightsFour = filteredValues

            elif entry[0] == 'Biases_4':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.biasesFour = filteredValues

            elif entry[0] == 'Weights_5':
                filteredValues = list(filter(returnOnlyNumericValues, entry))
                self.weightsFive = filteredValues

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

    def isEndOfGeneration(self):
        return self.currentCar == 250



# Run this file seperately to generate the initial random weights and biases
NL = NetworkLayout()
NL.loadNetwork()
# NL.createRandomValues()