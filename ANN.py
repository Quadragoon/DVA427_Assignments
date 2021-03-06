import numpy as np
import math
import time
import random
import lab_library as lablib
import os

# For every training example, until overall error becomes sufficiently low, do:
#   1.  Compute output from input (forwards)
#   2.  Compute error terms in output layer
#   3.  Compute error terms in hidden layers (backwards)
#   4.  Update weights using error terms

# input [size INPUTSx1]

# output [size 1x1]

# hidden layer weights [size HIDDENxHIDDEN (but the last layer has size HIDDENx1) and the first layer INPUTSxHIDDEN]

# error terms (2d list: error term j of hidden layer unit j has size rows(layer weight j))

##########################################################
# INITIALIZATION #########################################
##########################################################
numInputParameters = 19  # >= 1
numHiddenLayers = 1  # >= 0
hiddenLayerSize = 15  # > 0
eta = 0.3  # > 0
noOfRuns = 300

output_ANN = 0.0

start_time = time.time()
folder_name = '_'.join(["execution", start_time.__str__()])
path = os.path.join('', folder_name)
os.makedirs(path)


def create_weight_matrix(first=False, last=False):
    if first & last:
        return matrix_create_random(numInputParameters, 1)
    elif first:
        return matrix_create_random(numInputParameters, hiddenLayerSize)
    elif last:
        return matrix_create_random(hiddenLayerSize, 1)
    else:
        return matrix_create_random(hiddenLayerSize, hiddenLayerSize)


def matrix_sigmoid(value):
    return 1 / (1 + np.exp(-value))


def scalar_sigmoid(value):
    return 1 / (1 + math.exp(-value))


class Layer:
    def __init__(self, size, first=False, last=False):
        self.size = size
        self.weights = create_weight_matrix(first, last)
        self.inputs = np.zeros((1, size))
        self.errors = np.zeros((1, size))
        self.outputs = np.zeros((1, size))

        # create matrix of some size derived from the createWeightMatrix function (which takes into account whether
        # this is the first layer, last layer, or somewhere in between)
        self.weight_deltas = create_weight_matrix(first, last)
        # set all matrix elements to zero by multiplying them (by zero)
        self.weight_deltas *= 0


def matrix_create_random(rows, col):
    return np.random.random(size=(rows, col)) * 2 - 1


def matrix_print(matrix):
    print(matrix, "\n")
    return


def print_matrices():
    print('--- printing matrices --------')
    print('hidden layers')
    for layer in layers:
        if (layer != layers[0]) & (layer != layers[-1]):
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


def create_layers():
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
    layers[0].inputs = matrix_create_random(1, numInputParameters)


def create_testing_layers():
    global numHiddenLayers
    numHiddenLayers = 1
    global numInputParameters
    numInputParameters = 2
    global hiddenLayerSize
    hiddenLayerSize = 2

    layers.append(Layer(numInputParameters, first=True))

    layers[0].inputs[0, 0] = 2
    layers[0].inputs[0, 1] = 1
    layers[0].weights[0, 0] = 1
    layers[0].weights[0, 1] = 2
    layers[0].weights[1, 0] = 3
    layers[0].weights[1, 1] = 4

    for x in range(numHiddenLayers):
        if x < numHiddenLayers - 1:
            layers.append(Layer(hiddenLayerSize))
        else:
            layers.append(Layer(hiddenLayerSize, last=True))

    layers[-1].weights[0, 0] = 1
    layers[-1].weights[1, 0] = 2


#############################################################
#############################################################
#############################################################


# calculate ANN output for the current inputs and weights
def calc_output():
    layers[0].outputs = layers[0].inputs
    for layer_index in range(numHiddenLayers):
        layers[layer_index + 1].inputs = layers[layer_index].outputs.dot(layers[layer_index].weights)
        layers[layer_index + 1].outputs = matrix_sigmoid(layers[layer_index + 1].inputs)

    final_layer = layers[-1]
    # the np.dot operation will return a 1x1 matrix, so use the [0, 0] index operator to get the number contained inside
    output_sum = (final_layer.outputs.dot(final_layer.weights))[0, 0]
    output_sigmoid = scalar_sigmoid(output_sum)
    return output_sigmoid


# given the targeted output, calculate the error of the output
def calc_output_error(output, target):
    output_error = (-(target - output) * output * (1 - output))
    return output_error


def calc_errors_in_final_layer(output_error):
    final_layer = layers[-1]
    weighted_error_matrix = output_error * final_layer.weights
    for unit_index in range(final_layer.size):
        unit_output = final_layer.outputs[0, unit_index]
        final_layer.errors[0, unit_index] = ((1 - unit_output) * unit_output * weighted_error_matrix[unit_index, 0])


def calc_errors_in_final_layer_mat_mult(output_error):
    final_layer = layers[-1]
    weighted_error_matrix = np.diag(output_error * np.transpose(final_layer.weights)[0])
    inverted_outputs = np.diag((-final_layer.outputs + 1)[0])
    final_layer.errors = final_layer.outputs.dot(inverted_outputs)
    final_layer.errors = final_layer.errors.dot(weighted_error_matrix)


def calc_errors_in_hidden_layer(hidden_layer, downstream_layer):
    for unit_index in range(hidden_layer.size):
        unit_output = hidden_layer.outputs[0, unit_index]
        # calculate error terms according to this formula:
        # delta_j = (1 - O_j) * O_j * Sigma(delta_k * W_kj)
        downstream_error_sum = downstream_layer.errors.dot(hidden_layer.weights[unit_index].transpose())[0]
        hidden_layer.errors[0, unit_index] = ((1 - unit_output) * unit_output * downstream_error_sum)


def calc_errors_in_hidden_layer_mat_mult(hidden_layer, downstream_layer):
    downstream_error_sums = downstream_layer.errors.dot(hidden_layer.weights.transpose())
    inverted_outputs = np.diag((-hidden_layer.outputs + 1)[0])
    hidden_layer.errors = hidden_layer.outputs.dot(inverted_outputs).dot(np.diag(downstream_error_sums[0]))


def calc_output_weight_deltas(output_error):
    final_layer = layers[-1]
    # weight_delta = eta * delta_j * xji
    final_layer.weight_deltas = np.transpose(final_layer.outputs) * output_error
    final_layer.weight_deltas *= eta


def calc_output_weight_deltas_old(output_error):
    final_layer = layers[-1]
    for unit_index in range(hiddenLayerSize):
        # weight_delta = eta * delta_j * xji
        xji = final_layer.outputs[0, unit_index]  # * final_layer.weights[unit_index, 0]
        weight_delta = eta * output_error * xji
        final_layer.weight_deltas[unit_index, 0] = weight_delta


def update_layer_weights(hidden_layer, downstream_layer):
    hidden_layer.weight_deltas = np.transpose(hidden_layer.outputs).dot(downstream_layer.errors)
    hidden_layer.weight_deltas *= eta

    downstream_layer.weights -= downstream_layer.weight_deltas


def update_layer_weights_old(hidden_layer, downstream_layer):
    for unit_index in range(hidden_layer.size):
        xji = hidden_layer.outputs[0, unit_index]  # * hidden_layer.weights[unit_index, downstream_unit_index]
        for downstream_unit_index in range(downstream_layer.size):
            # weight_delta = eta * delta_j * xji
            weight_delta = eta * downstream_layer.errors[0, downstream_unit_index] * xji
            hidden_layer.weight_deltas[unit_index, downstream_unit_index] = weight_delta

    downstream_layer.weights -= downstream_layer.weight_deltas


def run_ann_on_current_input(target, update_weights=False, print_comparison=False):
    global output_ANN
    output = calc_output()

    output_ANN = output

    output_error = calc_output_error(output, target)

    if update_weights:
        calc_errors_in_final_layer_mat_mult(output_error)
        calc_output_weight_deltas(output_error)

        # iterate error calculation over hidden layers, starting at the end and moving backwards to the start
        for layer_index in range(numHiddenLayers, 0, -1):
            hidden_layer = layers[layer_index - 1]
            downstream_layer = layers[layer_index]
            calc_errors_in_hidden_layer_mat_mult(hidden_layer, downstream_layer)
            update_layer_weights(hidden_layer, downstream_layer)
        layers[0].weights -= layers[0].weight_deltas
    if print_comparison:
        print("Target: " + target.__str__() + "       Rounded output: " + int(round(output)).__str__())

    return output_error


class TestData:
    def __init__(self):
        self.total = 0
        self.correct_total = 0
        self.target_positive = 0
        self.correct_positive = 0
        self.target_negative = 0
        self.correct_negative = 0


def run_ann_on_set(target_set, update_weights=False, file=None, first_run_on_set=False):
    test_data = TestData()
    for data_point in target_set:
        # set inputs for ANN
        layers[0].inputs[0] = np.array(data_point.attributes)
        run_ann_on_current_input(data_point.classification, update_weights=update_weights)
        if data_point.classification == 1:
            test_data.total += 1
            test_data.target_positive += 1
            if output_ANN >= 0.5:
                test_data.correct_positive += 1
                test_data.correct_total += 1
        elif data_point.classification == 0:
            test_data.total += 1
            test_data.target_negative += 1
            if output_ANN < 0.5:
                test_data.correct_negative += 1
                test_data.correct_total += 1
    if file is not None:
        if first_run_on_set:
            line = ' '.join(["Total:", test_data.total.__str__(),
                             " Positive:", test_data.target_positive.__str__(),
                             " Negative:", test_data.target_negative.__str__(), '\n'])
            file.write(line)
            file.write("@data\n")
        line = ' '.join([test_data.correct_total.__str__(),
                         test_data.correct_positive.__str__(),
                         test_data.correct_negative.__str__(), '\n'])
        file.write(line)
    return test_data


#############################################################
#############################################################
#############################################################

layers = list()
create_layers()

all_data = lablib.import_data_from_file("assignment1.txt", 19)
attributes_max = list()
attributes_min = list()
data_count = len(all_data)

# initialize max and min attribute lists to permit indexing later on
lablib.initialize_max_and_min_attribute_lists(attributes_min, attributes_max, all_data[0])

training_set_size = math.ceil(data_count * 0.75)
training_set = random.sample(all_data, training_set_size)
all_data = [x for x in all_data if x not in training_set]

validation_set_size = math.floor(data_count * 0.15)
validation_set = random.sample(all_data, validation_set_size)
all_data = [x for x in all_data if x not in validation_set]

testing_set_size = math.floor(data_count * 0.1)
testing_set = random.sample(all_data, testing_set_size)
all_data = [x for x in all_data if x not in testing_set]

lablib.find_max_and_min_attributes_in_set(training_set, attributes_min, attributes_max)

lablib.normalize_data_set(training_set, attributes_min, attributes_max)
lablib.normalize_data_set(validation_set, attributes_min, attributes_max)
lablib.normalize_data_set(testing_set, attributes_min, attributes_max)

print("trainingSetSize: " + training_set_size.__str__())
print("validationSetSize: " + validation_set_size.__str__())
print("testingSetSize: " + testing_set_size.__str__())

bestAccuracy = 0

info_file = open(os.path.join(path, "info.txt"), mode="w+")
training_results_file = open(os.path.join(path, "training_results.txt"), mode="w+")
validation_results_file = open(os.path.join(path, "validation_results.txt"), mode="w+")
testing_results_file = open(os.path.join(path, "testing_results.txt"), mode="w+")

if info_file is not None:
    line = ' '.join(["Eta:", eta.__str__(), '\n',
                     "  #_of_runs:", noOfRuns.__str__(), '\n',
                     "  hidden_layer_size:", hiddenLayerSize.__str__(), '\n',
                     "  num_hidden_layers:", numHiddenLayers.__str__(), '\n'])
    info_file.write(line)
    info_file.close()

for i in range(noOfRuns):
    if i == 0:
        run_ann_on_set(training_set, update_weights=True, file=training_results_file, first_run_on_set=True)
    else:
        run_ann_on_set(training_set, update_weights=True, file=training_results_file)

    if i == 0:
        validation_set_data = run_ann_on_set(validation_set, file=validation_results_file, first_run_on_set=True)
    else:
        validation_set_data = run_ann_on_set(validation_set, file=validation_results_file)
    correct_guesses = validation_set_data.correct_total
    correct_positives = validation_set_data.correct_positive
    correct_negatives = validation_set_data.correct_negative

    accuracy = 100*correct_guesses/validation_set_size
    if accuracy > bestAccuracy:
        bestAccuracy = accuracy

    print("i:  ", i, " ", sep="", end="")
    # print(error_sum)
    print("Accuracy: ", round(accuracy, 2), " [", correct_guesses, "/", validation_set_size, "] ", sep="", end="")
    print("Correct positives: ", correct_positives, "   Correct negatives: ", correct_negatives, sep="", end="")
    print("")

print("\n Best accuracy: ", bestAccuracy, sep="")
print("Now testing once on testing set...")

testing_set_data = run_ann_on_set(testing_set, file=testing_results_file, first_run_on_set=True)
correct_guesses = testing_set_data.correct_total
target_positives = testing_set_data.target_positive
correct_positives = testing_set_data.correct_positive
target_negatives = testing_set_data.target_negative
correct_negatives = testing_set_data.correct_negative

accuracy = 100*correct_guesses/testing_set_size
positive_accuracy = 100 * correct_positives / target_positives
negative_accuracy = 100 * correct_negatives / target_negatives

# print(error_sum)
print("Accuracy: ", round(accuracy, 2), " [", correct_guesses, "/", testing_set_size, "] ", sep="")
print("Positives accuracy: ", round(positive_accuracy, 2), " [", correct_positives, "/", target_positives, "] ", sep="")
print("Negatives accuracy: ", round(negative_accuracy, 2), " [", correct_negatives, "/", target_negatives, "] ", sep="")

print("")

training_results_file.close()
validation_results_file.close()
testing_results_file.close()

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.__str__(), " seconds.")
