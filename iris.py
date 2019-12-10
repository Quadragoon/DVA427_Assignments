import numpy as np
import time
import lab_library as lablib

##########################################################
# INITIALIZATION #########################################
##########################################################
np.random.seed()

start_time = time.time()

all_data = lablib.import_data_from_file("iris.txt", 4, sep=" ")
attributes_min = list()
attributes_max = list()

# initialize attribute min and max lists to allow indexing in them later on
for attribute in all_data[0].attributes:
    attributes_min.append(attribute)
    attributes_max.append(attribute)

# read all data, finding the maximum and minimum values for each attribute
for data_point in all_data:
    for attribute_index in range(len(data_point.attributes)):
        minimum = min(attributes_min[attribute_index], data_point.attributes[attribute_index])
        attributes_min[attribute_index] = minimum
        maximum = max(attributes_max[attribute_index], data_point.attributes[attribute_index])
        attributes_max[attribute_index] = maximum

# normalize data to land between 0 and 1 using the min and max values (min being 0 and max being 1)
for data_point in all_data:
    for attribute_index in range(len(data_point.attributes)):
        attribute_max = attributes_max[attribute_index]
        attribute_min = attributes_min[attribute_index]
        if attribute_max == attribute_min:
            continue
        data_point.attributes[attribute_index] = (data_point.attributes[attribute_index] - attribute_min) / (attribute_max - attribute_min)


##########################################################
# CLASSIFICATION #########################################
##########################################################
zadeh_operators = True


def fuzzy_AND(a, b):
    if zadeh_operators:
        return min(a, b)
    else:
        return a*b


def fuzzy_OR(a, b):
    if zadeh_operators:
        return max(a, b)
    else:
        return 1 - ((1-a)*(1-b))


def fuzzy_short(x):
    if x > 0.6:
        return 0
    k = -1/0.6
    m = 0
    return k*x+m


def fuzzy_medium(x):
    if x <= 0.6:
        k = 1/0.6
        m = 0
    else:
        k = -2.5
        m = 2.5
    return k*x+m


def fuzzy_long(x):
    if x < 0.6:
        return 0
    else:
        k = 2.5
        m = -1.5
    return k*x+m


class FuzzyCategory:
    def __init__(self, short, medium, long):
        self.short = short
        self.medium = medium
        self.long = long


class Iris:
    def __init__(self, fuzzy_categories):
        self.fuzzy_categories = fuzzy_categories
        self.classification = 0


irises = list()

for data_point in all_data:
    fuzzy_categories = list()
    for attribute in data_point.attributes:
        fuzzy_categories.append(FuzzyCategory(fuzzy_short(attribute), fuzzy_medium(attribute), fuzzy_long(attribute)))
    new_iris = Iris(fuzzy_categories)
    new_iris.classification = data_point.classification
    irises.append(new_iris)

##########################################################
# FINALIZATION ###########################################
##########################################################

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.__str__(), " seconds.")


