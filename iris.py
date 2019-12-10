import numpy as np
import time
import lab_library as lablib
##########################################################
# INITIALIZATION #########################################
##########################################################
np.random.seed()

start_time = time.time()

all_data = lablib.import_data_from_file("iris.txt", 4)

training_set_size = math.ceil(data_count * 0.75)
# training_set = all_data[0:training_set_size]
training_set = random.sample(all_data, training_set_size)
all_data = [x for x in all_data if x not in training_set]

validation_set_size = math.floor(data_count * 0.15)
# validation_set = all_data[training_set_size:training_set_size + validation_set_size]
validation_set = random.sample(all_data, validation_set_size)
all_data = [x for x in all_data if x not in validation_set]

testing_set_size = math.floor(data_count * 0.1)
# testing_set = all_data[training_set_size + validation_set_size:training_set_size + validation_set_size + testing_set_size]
testing_set = random.sample(all_data, testing_set_size)
all_data = [x for x in all_data if x not in testing_set]

for data_point in training_set:
    for attribute_index in range(len(data_point.attributes)):
        minimum = min(attributes_min[attribute_index], data_point.attributes[attribute_index])
        attributes_min[attribute_index] = minimum
        maximum = max(attributes_max[attribute_index], data_point.attributes[attribute_index])
        attributes_max[attribute_index] = maximum

for data_point in training_set:
    for attribute_index in range(len(data_point.attributes)):
        attribute_max = attributes_max[attribute_index]
        attribute_min = attributes_min[attribute_index]
        if attribute_max == attribute_min:
            continue
        data_point.attributes[attribute_index] = (data_point.attributes[attribute_index] - attribute_min) / (attribute_max - attribute_min)

for data_point in validation_set:
    for attribute_index in range(len(data_point.attributes)):
        attribute_max = attributes_max[attribute_index]
        attribute_min = attributes_min[attribute_index]
        if attribute_max == attribute_min:
            continue
        data_point.attributes[attribute_index] = (data_point.attributes[attribute_index] - attribute_min) / (attribute_max - attribute_min)

for data_point in testing_set:
    for attribute_index in range(len(data_point.attributes)):
        attribute_max = attributes_max[attribute_index]
        attribute_min = attributes_min[attribute_index]
        if attribute_max == attribute_min:
            continue
        data_point.attributes[attribute_index] = (data_point.attributes[attribute_index] - attribute_min) / (attribute_max - attribute_min)

print("trainingSetSize: " + training_set_size.__str__())
print("validationSetSize: " + validation_set_size.__str__())
print("testingSetSize: " + testing_set_size.__str__())

noOfRuns = 100
bestAccuracy = 0

for i in range(noOfRuns):
    correct_guesses = 0
    correct_positives = 0
    correct_negatives = 0
    error_sum = 0

    for data_point in training_set:
        layers[0].inputs[0] = np.array(data_point.attributes)
        ANN_run(data_point.classification, update_weights=True)
    for data_point in validation_set:
        layers[0].inputs[0] = np.array(data_point.attributes)
        error_sum += abs(ANN_run(data_point.classification, print_comparison=False))
        if (output_ANN >= 0.5) & (data_point.classification == 1):
            correct_guesses += 1
            correct_positives += 1
        elif (output_ANN < 0.5) & (data_point.classification == 0):
            correct_guesses += 1
            correct_negatives += 1

    accuracy = 100*correct_guesses/validation_set_size
    if accuracy > bestAccuracy:
        bestAccuracy = accuracy

    print("i:  ", i, " ", sep="", end="")
    # print(error_sum)
    print("Accuracy: ", accuracy, " [", correct_guesses, "/", validation_set_size, "] ", sep="", end="")
    print("Correct positives: ", correct_positives, "   Correct negatives: ", correct_negatives, sep="", end="")
    print("")

print("\n Best accuracy: ", bestAccuracy, sep="")
print("Now testing once on testing set...")

correct_guesses = 0
correct_positives = 0
correct_negatives = 0
error_sum = 0

for data_point in testing_set:
    layers[0].inputs[0] = np.array(data_point.attributes)
    ANN_run(data_point.classification)
    if (output_ANN >= 0.5) & (data_point.classification == 1):
        correct_guesses += 1
        correct_positives += 1
    elif (output_ANN < 0.5) & (data_point.classification == 0):
        correct_guesses += 1
        correct_negatives += 1

accuracy = 100*correct_guesses/testing_set_size
if accuracy > bestAccuracy:
    bestAccuracy = accuracy

# print(error_sum)
print("Accuracy: ", accuracy, " [", correct_guesses, "/", testing_set_size, "] ", sep="", end="")
print("Correct positives: ", correct_positives, "   Correct negatives: ", correct_negatives, sep="", end="")
print("")

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.__str__(), " seconds.")
