import numpy as np
#############################################################
#### INITIALIZATION #########################################
#############################################################
np.random.seed()

def matrix_create_random(rows, col):
    return np.random.random(size=(rows,col))

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
    print('input')
    matrix_print(X)
    print('output')
    matrix_print(Y)
    print('hidden layers')
    for layer in hiddenLayers:
        matrix_print(layer)
    print('error output')
    matrix_print(errorOutput)
    print('error hidden layers')
    for error in errorHidden:
        matrix_print(error)
    print('------------------')
inputsize = 3 # >= 1
hiddensize = 3 # >= 0

#input [size INPUTSx1]
X = np.zeros((inputsize,1))
#output [size 1x1]
Y = np.zeros((1,1))

#hidden layer weights [size INPUTSxINPUTS (but the last layer has size 1xINPUTS)]
hiddenLayers = list()
for x in range(hiddensize-1):
    hiddenLayers.append(matrix_create_random(inputsize,inputsize))
#the last hidden layer: reduces inputsize units to one single unit (which is the output)
#hiddenLayers.append(np.zeros((1,inputsize)))
hiddenLayers.append(matrix_create_random(1,inputsize))

#error terms for output
errorOutput = np.zeros((inputsize,1))
#errorOutput = matrix_create_random(inputsize,1)

#error terms for hidden layers (2d list: error term j of hidden layer unit j has size rows(layer weight j))
errorHidden = list()
for index in range(hiddensize-1):
    errorHidden.append(np.zeros((inputsize,1)))

#error term for last hidden layer (unneccessary(?))
#errorHidden.append(np.zeros((1,1)))

printMatrices()
#############################################################
#############################################################
#############################################################

errorlist = errorOutput
errorlist.append(errorHidden)

def ANN_run(inputs, weights):
    output = np.zeros((1,1))
    for layer_weights in weights:
        output = layer_weights.dot(inputs)
        print(output, "\n")
    return output


def error_for_nodes_in_this_layer(layer_weights, errors_previous_layer, size, layer_outputs):
    node_errors = np.zeros((size,1))
    for this_node in range(size):
        calculated_error = 0

        for node_downstream in range(size):
            calculated_error += errors_previous_layer[node_downstream]*layer_weights[this_node][node_downstream]

        calculated_error*= (1-layer_outputs[this_node])

        node_errors[this_node] = calculated_error
    return node_errors



def error_in_output(output_ANN, output_target, weights):
    #cycle through all nodes in current layer
        #calculate error in this node

    return (output_target - output_ANN)*output_ANN*(1-output_ANN)

def error_in_hidden_layers(output_error, hidden_layers,):
    sum = 0
    #for unit in
    return



result = ANN_run(X, hiddenLayers)
#errorOutput = error_in_output(result, target)


#For every training example, until overall error becomes sufficiently low, do:
#   1.  Compute output from input (forwards)
#   2.  Compute error terms in output layer
#   3.  Compute error terms in hidden layers (backwards)
#   4.  Update weights using error terms

#input [size INPUTSx1]

#output [size 1x1]

#hidden layer weights [size INPUTSxINPUTS (but the last layer has size 1xINPUTS)]

#error terms (2d list: error term j of hidden layer unit j has size rows(layer weight j))

