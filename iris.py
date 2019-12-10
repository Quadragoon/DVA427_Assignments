import numpy as np
import time
import lab_library as lablib
##########################################################
# INITIALIZATION #########################################
##########################################################
np.random.seed()

start_time = time.time()

all_data = lablib.import_data_from_file("iris.txt", 4)
attributes_min = list()
attributes_max = list()

# initialize attribute min and max lists to allow indexing in them later on
for attribute in all_data[0].attributes:
    attributes_min.append(attribute)
    attributes_max.append(attribute)

for data_point in all_data:
    for attribute_index in range(len(data_point.attributes)):
        minimum = min(attributes_min[attribute_index], data_point.attributes[attribute_index])
        attributes_min[attribute_index] = minimum
        maximum = max(attributes_max[attribute_index], data_point.attributes[attribute_index])
        attributes_max[attribute_index] = maximum

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

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.__str__(), " seconds.")