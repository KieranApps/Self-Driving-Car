import json
import socket
import sys
import NeuralNetwork as NN

HOST = 'localhost'
PORT = 9001
# Denotes the end of the data
DELIMITER = '|'
# Start and end of the JSON object. A data set must have BOTH so we know that it is complete
START_SYMBOL = '{'
END_SYMBOL = '}'

# If the NN is in use, set this to true to prevent another process running. Unity will also be 'Frozen' While this process is running as to not miss frames
neuralNetworkInUse = False
neuralNetwork = NN.NeuralNetwork()
# Process the inputs from the Unity Project to select the option
def processInputs(data):
    jsonData = json.loads(data)

    if('getInputs' in jsonData and jsonData['getInputs'] == True):
        carInputs = neuralNetwork.processInputs(jsonData, DELIMITER)
        sock.sendall(carInputs.encode())

    elif ('reset' in jsonData and jsonData['reset']  == True):
        status = neuralNetwork.reset(jsonData['time'], jsonData['distance'], DELIMITER)
        sock.sendall(status.encode())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hasConnection = False

while not hasConnection:
    try:
        sock.connect((HOST, PORT))
        hasConnection = True
    except:
        print('Could not connect to Unity. Trying again...')

# Initialise the data
data = ''
allData = False
# Start the Unity Simulation first (since its a large project it causes issues the other way around)
# If the connection is lost, the Unity project stopped. So, stop the server
while hasConnection:
    # Recieve a maximum amount of bytes
    rawData = sock.recv(1024).decode('utf-8')
    if(rawData == ''):
        print('Closing')
        sock.close()
        hasConnection = False
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
