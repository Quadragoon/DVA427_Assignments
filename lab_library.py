def import_data_from_file(filename, num_attributes, has_classification=True):
    data_file = open("assignment1.txt", mode="r")

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
        data_point = Data()
        data_point.attributes = list(map(float, line.split(",")))
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