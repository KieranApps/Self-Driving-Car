import pandas as pd
import numpy as np

class NetworkLayout():

    def __init__(self):
        # These layer sizes can be tweaked to create a better functioning Neural Network
        self.inputSize = 10
        self.hiddenLayerOneSize = 10
        self.hiddenLayerTwoSize = 7
        self.hiddenLayerThreeSize = 5
        self.hiddenLayerFourSize = 3

        # This will be used to keep track of which NN we are currently using
        self.currentGeneration = 1

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
            data.index = ['Weights_1','biasesOne','Weights_2','biasesTwo','Weights_3','biasesThree','Weights_4','biasesFour','Weights_5','FitnessValue']
            # All car networks are stored in the Car directory
            data.to_csv('./Cars/car' + str(i) + '.txt')
    
    def loadNetwork(self):
        print('Loading New Network...')

    def saveNetwork(self):
        print('Saving Networks...')

    def saveBestNetwork(self):
        print('Saving Best Network...')



# Run this file seperately to generate the initial random weights and biases
NL = NetworkLayout()
NL.createRandomValues()