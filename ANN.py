import numpy as np
##########################################################
# INITIALIZATION #########################################
##########################################################
np.random.seed()


def createWeightMatrix(first=False, last=False):
    if first:
        return matrix_create_random(numInputParameters, hiddenLayerSize)
    elif last:
        return matrix_create_random(hiddenLayerSize, 1)
    else:
        return matrix_create_random(hiddenLayerSize, hiddenLayerSize)


class Layer:
    def __init__(self, size, first=False, last=False):
        self.inputs = np.zeros((1, size))
        self.errors = np.zeros((1, size))
        self.weights = createWeightMatrix(first, last)


def matrix_create_random(rows, col):
    return np.random.random(size=(rows,col)) * 2 - 1


def matrix_print(matrix):
    print(matrix,"\n")
    return
#    for row in matrix:
#        print("[  ", end="")
#        for elem in row:
#            print(elem, end='  ')
#        print("]")
#    print("")


def printMatrices():
    print('--- printing matrices --------')
    print('hidden layers')
    for layer in layers:
        if ((layer != layers[0]) & (layer != layers[layers.__len__()-1])):
            matrix_print(layer.weights)
    print('input')
    matrix_print(layers[0].inputs)
    print('output')
    matrix_print(layers[-1].outputs)
    # print('error output')
    # matrix_print(errorOutput)
    # print('error hidden layers')
    # for error in hiddenLayerErrors:
    #     matrix_print(error)
    print('------------------')

layers = list()
numInputParameters = 18  # >= 1
numHiddenLayers = 5  # >= 0
hiddenLayerSize = 5  # > 0

def CreateLayers():
    global hiddenLayerSize
    inputLayer = Layer(numInputParameters, first=True)
    layers.append(inputLayer)
    for x in range(numHiddenLayers):
        layers.append(Layer(hiddenLayerSize))
    if numHiddenLayers == 0:
        hiddenLayerSize = numInputParameters
    layers.append(Layer(hiddenLayerSize, last=True))

# error terms for output
errorOutput = np.zeros((numInputParameters, 1))

# error terms for hidden layers (2d list: error term j of hidden layer unit j has size rows(layer weight j))
hiddenLayerErrors = list()
for index in range(numHiddenLayers - 1):
    hiddenLayerErrors.append(np.zeros((numInputParameters, 1)))

# error term for last hidden layer (unnecessary(?))
# errorHidden.append(np.zeros((1,1)))

#############################################################
#############################################################
#############################################################

errorList = list()
errorList.append(errorOutput)
errorList.append(hiddenLayerErrors)


def ANN_run(inputs, weights):
    output = np.zeros((1,1))
    for layer_weights in weights:
        output = inputs.dot(layer_weights)
        print(output, "\n")
    return output


def ANN_run_2():
    for i in range(layers.__len__()):
        #layers[i].outputs = layers[i].inputs.dot(layers[i].weights)
        if i < layers.__len__() - 1:
            #layers[i+1].inputs = layers[i].outputs
            layers[i+1].inputs = layers[i].inputs.dot(layers[i].weights)

    calc_final_output_error(1)
    for layer_index in range(numHiddenLayers - 1):
        calc_errors_in_hidden_layer(layers[- layer_index - 2], layers[ - layer_index - 1])
        print(layers[-layer_index - 2].errors)


def error_for_nodes_in_this_layer(layer_weights, errors_previous_layer, size, layer_outputs):
    node_errors = np.zeros((size, 1))
    for this_node in range(size):
        calculated_error = 0

        for node_downstream in range(size):
            calculated_error += errors_previous_layer[node_downstream]*layer_weights[this_node][node_downstream]

        calculated_error *= (1-layer_outputs[this_node])

        node_errors[this_node] = calculated_error
    return node_errors


def calc_final_output_error(output_target):
    # cycle through all nodes in current layer
    # calculate error in this node
    output_sum = np.sum(layers[-1].inputs.dot(layers[-1].weights))
    print(output_sum)
    final_output_error = ((output_target - output_sum) * output_sum * (1 - output_sum))

    for unit_index in range(hiddenLayerSize):
        weightedError = (final_output_error * layers[-1].weights[unit_index, 0])
        layers[-1].errors[0, unit_index] = (
                    (1 - layers[-1].inputs[0, unit_index]) * layers[-1].inputs[0, unit_index] * weightedError)


def calc_errors_in_hidden_layer(hidden_layer, downstream_layer):
    for unit_index in range(hiddenLayerSize):
        errorSum = 0
        for downstream_unit_index in range(downstream_layer.inputs.__len__()):
            errorSum += (downstream_layer.errors[0, downstream_unit_index] * hidden_layer.weights[unit_index, downstream_unit_index])
        hidden_layer.errors[0, unit_index] = ((1 - hidden_layer.inputs[0, unit_index]) * hidden_layer.inputs[0, unit_index] * errorSum)


# result = ANN_run(X, weightMatrices)
CreateLayers()

layers[0].inputs = matrix_create_random(1, numInputParameters)
ANN_run_2()

# printMatrices()

# errorOutput = error_in_output(result, target)


# For every training example, until overall error becomes sufficiently low, do:
#   1.  Compute output from input (forwards)
#   2.  Compute error terms in output layer
#   3.  Compute error terms in hidden layers (backwards)
#   4.  Update weights using error terms

# input [size INPUTSx1]

# output [size 1x1]

# hidden layer weights [size INPUTSxINPUTS (but the last layer has size 1xINPUTS)]

# error terms (2d list: error term j of hidden layer unit j has size rows(layer weight j))
