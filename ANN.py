import numpy as np
##########################################################
# INITIALIZATION #########################################
##########################################################
np.random.seed()
numInputParameters = 18  # >= 1
numHiddenLayers = 1  # >= 0
hiddenLayerSize = 5  # > 0


def createWeightMatrix(first=False, last=False):
    if first & last:
        return matrix_create_random(numInputParameters, 1)
    elif first:
        return matrix_create_random(numInputParameters, hiddenLayerSize)
    elif last:
        return matrix_create_random(hiddenLayerSize, 1)
    else:
        return matrix_create_random(hiddenLayerSize, hiddenLayerSize)


def sigmoid(value):
    return 1 / (1 + np.exp(-value))


class Layer:
    def __init__(self, size, first=False, last=False):
        self.weights = createWeightMatrix(first, last)
        self.inputs = np.zeros((1, size))
        self.errors = np.zeros((1, size))
        self.outputs = np.zeros((1, size))


def matrix_create_random(rows, col):
    return np.random.random(size=(rows,col)) * 2 - 1


def matrix_print(matrix):
    print(matrix,"\n")
    return


def printMatrices():
    print('--- printing matrices --------')
    print('hidden layers')
    for layer in layers:
        if ((layer != layers[0]) & (layer != layers[-1])):
            matrix_print(layer.weights)
    print('input')
    matrix_print(layers[0].inputs)
    # print('output')
    # matrix_print(layers[-1].outputs)
    # print('error output')
    # matrix_print(errorOutput)
    # print('error hidden layers')
    # for error in hiddenLayerErrors:
    #     matrix_print(error)
    print('------------------')


layers = list()


def CreateLayers():
    if numHiddenLayers == 0:
        layers.append(Layer(numInputParameters, first=True, last=True))
    else:
        layers.append(Layer(numInputParameters, first=True))

    global hiddenLayerSize
    for x in range(numHiddenLayers):
        if x < numHiddenLayers - 1:
            layers.append(Layer(hiddenLayerSize))
        else:
            layers.append(Layer(hiddenLayerSize, last=True))

#############################################################
#############################################################
#############################################################


# given the targeted output, calculate the error of the output
def calc_output_error(output_target):
    final_layer = layers[-1]
    output_sum = np.sum(final_layer.outputs.dot(final_layer.weights))
    output_sigmoid = sigmoid(output_sum)
    final_output_error = ((output_target - output_sigmoid) * output_sigmoid * (1 - output_sigmoid))

    for unit_index in range(hiddenLayerSize):
        weightedError = (final_output_error * final_layer.weights[unit_index, 0])
        final_layer.errors[0, unit_index] = (
                    (1 - final_layer.outputs[0, unit_index]) * final_layer.outputs[0, unit_index] * weightedError)

    print(final_layer.errors)


def calc_errors_in_hidden_layer(hidden_layer, downstream_layer):
    for unit_index in range(hiddenLayerSize):
        errorSum = 0

        # calculate error terms according to this formula:
        # delta_j = (1 - O_j) * O_j * Sigma(delta_k * W_kj)
        for downstream_unit_index in range(downstream_layer.outputs.__len__()):
            errorSum += (downstream_layer.errors[0, downstream_unit_index] * hidden_layer.weights[unit_index, downstream_unit_index])
        hidden_layer.errors[0, unit_index] = ((1 - hidden_layer.outputs[0, unit_index]) * hidden_layer.outputs[0, unit_index] * errorSum)


def ANN_run():
    layers[0].outputs = layers[0].inputs
    for i in range(numHiddenLayers):
        layers[i+1].inputs = layers[i].outputs.dot(layers[i].weights)
        layers[i+1].outputs = sigmoid(layers[i+1].inputs)

    print("Calculating error in final layer, index " + str(layers.__len__() - 1))
    calc_output_error(1)

    # iterate error calculation over hidden layers, starting at the end and moving backwards to the start
    for layer_index in range(numHiddenLayers, 0, -1):
        print("Calculating error in layer " + str(layer_index - 1) + " from layer " + str(layer_index))
        calc_errors_in_hidden_layer(layers[layer_index - 1], layers[layer_index])


CreateLayers()

layers[0].inputs = matrix_create_random(1, numInputParameters)
ANN_run()

# printMatrices()


# For every training example, until overall error becomes sufficiently low, do:
#   1.  Compute output from input (forwards)
#   2.  Compute error terms in output layer
#   3.  Compute error terms in hidden layers (backwards)
#   4.  Update weights using error terms

# input [size INPUTSx1]

# output [size 1x1]

# hidden layer weights [size INPUTSxINPUTS (but the last layer has size 1xINPUTS)]

# error terms (2d list: error term j of hidden layer unit j has size rows(layer weight j))
