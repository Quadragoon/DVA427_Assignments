import time
import lab_library as lablib

##########################################################
# INITIALIZATION #########################################
##########################################################
start_time = time.time()

all_data = lablib.import_data_from_file("iris.txt", 4, sep=" ")
attributes_min = list()
attributes_max = list()
irises = list()


# initialize attribute min and max lists to allow indexing in them later on
lablib.initialize_max_and_min_attribute_lists(attributes_min, attributes_max, all_data[0])

# read all data, finding the maximum and minimum values for each attribute
lablib.find_max_and_min_attributes_in_set(all_data, attributes_min, attributes_max)

# normalize data to land between 0 and 1 using the min and max values (min being 0 and max being 1)
lablib.normalize_data_set(all_data, attributes_min, attributes_max)


def fuzzy_short(x):
    if x > 0.6:
        return 0
    k = -1/0.6
    m = 1
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


def defuzz_short(x):

    0.3

    return


class FuzzyClassifiedAttribute:
    def __init__(self, short, medium, long):
        self.short = short
        self.medium = medium
        self.long = long


class Iris:
    def __init__(self, classified_attributes):
        self.classified_attributes = classified_attributes
        self.classification = 0


for data_point in all_data:
    fuzzy_classified_attributes = list()
    for attribute in data_point.attributes:
        short_value = fuzzy_short(attribute)
        medium_value = fuzzy_medium(attribute)
        long_value = fuzzy_long(attribute)
        fuzzy_classified_attributes.append(FuzzyClassifiedAttribute(short_value, medium_value, long_value))
    new_iris = Iris(fuzzy_classified_attributes)
    new_iris.classification = data_point.classification
    irises.append(new_iris)


##########################################################
# CLASSIFICATION #########################################
##########################################################
zadeh_operators = True


def AND(a, b):
    if zadeh_operators:
        return min(a, b)
    else:
        return a*b


def OR(a, b):
    if zadeh_operators:
        return max(a, b)
    else:
        return 1 - ((1-a)*(1-b))


def fuzzy_r1(iris):
    x1 = iris.classified_attributes[0]
    x2 = iris.classified_attributes[1]
    x3 = iris.classified_attributes[2]
    x4 = iris.classified_attributes[3]

    ax1 = OR(x1.short, x1.long)
    ax2 = OR(x2.medium, x2.long)
    ax3 = OR(x3.medium, x3.long)
    ax4 = x4.medium

    return AND(AND(ax1, ax2), AND(ax3, ax4))


def fuzzy_r2(iris):
    x3 = iris.classified_attributes[2]
    x4 = iris.classified_attributes[3]

    ax3 = OR(x3.short, x3.medium)
    ax4 = x4.short

    return AND(ax3, ax4)


def fuzzy_r3(iris):
    x2 = iris.classified_attributes[1]
    x3 = iris.classified_attributes[2]
    x4 = iris.classified_attributes[3]

    ax2 = OR(x2.short, x2.medium)
    ax3 = x3.long
    ax4 = x4.long

    return AND(AND(ax2, ax3), ax4)


def fuzzy_r4(iris):
    x1 = iris.classified_attributes[0]
    x2 = iris.classified_attributes[1]
    x3 = iris.classified_attributes[2]
    x4 = iris.classified_attributes[3]

    ax1 = x1.medium
    ax2 = OR(x2.short, x2.medium)
    ax3 = x3.short
    ax4 = x4.long

    return AND(AND(ax1, ax2), AND(ax3, ax4))


def naive_classification():
    accurate_classifications = 0
    for i in range(len(irises)):
        iris = irises[i]
        r1 = fuzzy_r1(iris)
        r2 = fuzzy_r2(iris)
        r3 = fuzzy_r3(iris)
        r4 = fuzzy_r4(iris)

        classed_as = 0
        max_rule = max(r1, r2, r3, r4)
        if max_rule == r1:
            classed_as = 2
        elif max_rule == r2:
            classed_as = 1
        elif max_rule == r3:
            classed_as = 3
        elif max_rule == r4:
            classed_as = 2
        else:
            for loop_count in range(3):
                print("ERROR DURING CLASSIFICATION, ABORT EXPERIMENT, THE IRISES ARE ESCAPING")

        if classed_as == iris.classification:
            accurate_classifications += 1
        else:
            print("Iris #", i, "incorrectly classed as", classed_as, "but is", iris.classification)

    classification_percentage = accurate_classifications / len(all_data) * 100
    print("Naïve classification complete.")
    print("Accurate classifications: ", accurate_classifications, "/", len(all_data), ". That's ", round(classification_percentage, 3), "%!", sep="")


##########################################################
# FINALIZATION ###########################################
##########################################################

naive_classification()

end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.__str__(), " seconds.")
