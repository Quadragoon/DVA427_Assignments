def import_data_from_file(filename, num_attributes, has_classification=True, sep=","):
    data_file = open(filename, mode="r")

    line = data_file.readline()
    while line != "@data\n":
        line = data_file.readline()

    print("Found data start, processing...")

    class Data:
        attributes = []
        classification = 0

        def __str__(self):
            return "CLASS: " + self.classification.__str__() + "   " + "".join(self.attributes.__str__())

    all_data = []

    for line in data_file:
        if not any(character.isdigit() for character in line):
            continue
        data_point = Data()
        data_point.attributes = list(map(float, line.split(sep)))
        if has_classification:
            data_point.classification = int(data_point.attributes[-1])
            del data_point.attributes[-1]

        if len(data_point.attributes) == num_attributes:
            all_data.append(data_point)
        else:
            continue

    data_count = len(all_data)
    print("Total number of data points: " + data_count.__str__())
    return all_data


def normalize_data_set(data_set, attributes_min, attributes_max):
    for data_point in data_set:
        for attribute_index in range(len(data_point.attributes)):
            attribute_max = attributes_max[attribute_index]
            attribute_min = attributes_min[attribute_index]
            if attribute_max == attribute_min:
                continue
            data_point.attributes[attribute_index] = (data_point.attributes[attribute_index] - attribute_min) / (
                        attribute_max - attribute_min)


def initialize_max_and_min_attribute_lists(attributes_min, attributes_max, data_point):
    for attribute in data_point.attributes:
        attributes_max.append(attribute)
        attributes_min.append(attribute)


def find_max_and_min_attributes_in_set(data_set, attributes_min, attributes_max):
    for data_point in data_set:
        for attribute_index in range(len(data_point.attributes)):
            minimum = min(attributes_min[attribute_index], data_point.attributes[attribute_index])
            attributes_min[attribute_index] = minimum
            maximum = max(attributes_max[attribute_index], data_point.attributes[attribute_index])
            attributes_max[attribute_index] = maximum
