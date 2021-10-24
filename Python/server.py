import json
import socket

HOST = 'localhost'
PORT = 9001
# Denotes the end of the data
DELIMITER = '|'
# Start and end of the JSON object. A data set must have BOTH so we know that it is COMPLETE
START_SYMBOL = '{'
END_SYMBOL = '}'

# If the NN is in use, set this to true to prevent another process running. Unity will also be 'Frozen' While this process is running as to not miss frames
neuralNetworkInUse = False

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hasConnection = False
while not hasConnection:
    try:
        socket.connect((HOST, PORT))
        hasConnection = True
    except:
        print('Could not connect to Unity. Trying again...')

def processInputs(data):

    print('Got: ', data)
    if(data != "{Hello}"):
        raise Exception('AAAAAAAAAAAA')

data = ''
allData = False
while hasConnection:
    rawData = socket.recv(1024).decode('utf-8')
    data += rawData
    if(data.__contains__(DELIMITER)):
        tempData = data.split(DELIMITER)
        for i in range(0, len(tempData) - 1):
            # Check that at least on of the split objects contains a start and end of the object
            # A limitation of this is that we can only have a one deep level object 
            if(tempData[i].__contains__(START_SYMBOL) and tempData[i].__contains__(END_SYMBOL)):
                data = tempData[i]
                allData = True
                break
    
    if(allData and not neuralNetworkInUse):
        processInputs(data)
        data = ''
        allData = False


socket.close()