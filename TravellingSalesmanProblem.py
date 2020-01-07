from math import *
import random
import lab_library as lablib


def import_data(filename, cities):
    data_file = open(filename, mode="r")
    i = 0
    for line in data_file:
        data = list(map(float, line.split(" ")))
        id = int(data[0])
        x = data[1]
        y = data[2]
        city_to_import = City(x, y)
        #print(city_to_import.id, city_to_import.x, city_to_import.y)
        cities.append(city_to_import)


def import_data_2(filename, cities):
    imported_data = lablib.import_data_from_file(filename, 3, has_classification=False, sep=" ")
    for data_point in imported_data:
        x = data_point.attributes[1]
        y = data_point.attributes[2]
        cities.append(City(x, y))


def distance(p1, p2):
    return sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Individual:
    def __init__(self, num_cities, initialize=False):
        self.route = []
        if initialize is True:
            for i in range(1, num_cities):
                self.route.append(i)
            random.shuffle(self.route)

    def print_route(self):
        print("Route:", self.route)
        return

    def calculate_distance(self, cities):
        print("Calculate distance:")
        for city in self.route:
            print("[", city, cities[city].x, cities[city].y, "]")
        distance_sum = 0

        # calculate distance from the start point to the first step on the route
        delta = distance(cities[0], cities[self.route[0]])
        # add that distance to total distance traveled
        distance_sum += delta
        print("d:[ S ] [", delta, "]")

        for i in range(self.route.__len__() - 1):
            # calculate distance from each destination to the next
            delta = distance(cities[self.route[i]], cities[self.route[i+1]])
            # add up the distances
            distance_sum += delta
            print("d:[", i, "to", i+1, "] [", delta, "]")

        # calculate distance from the last step on the route to the end point
        delta = distance(cities[self.route[-1]], cities[0])
        # add that distance to total distance traveled
        distance_sum += delta
        print("d:[ E ] [", delta, "]")

        print("SUM: [", distance_sum, "]")
        return distance_sum


def crossover(parent_a, parent_b):
    print("crossover:")
    #route_a = parent_a.route.copy()
    #route_b = parent_b.route.copy()

    route_a = [7,3,1,8,2,4,6,5]
    route_b = [7,5,2,8,4,3,1,6]
    print(route_a)
    print(route_b)

    crossover_length = 3
    crossover_start = 2

    crossover_set = []
    for i in range(crossover_length):
        crossover_set.append(route_a[crossover_start+i])

    difference_set = route_b.copy()
    for element in crossover_set:
        difference_set.remove(element)

    route_c = []
    for i in range(crossover_start):
        route_c.append(difference_set[i])
    for element in crossover_set:
        route_c.append(element)
    for i in range(crossover_start, len(difference_set)):
        route_c.append(difference_set[i])

    print("a: ", route_a)
    print("c: ", route_c)
    print("b: ", route_b)

    return 1


a = City(0, 0)
b = City(1, 0)

print(distance(a, b))

cities = list()
import_data_2("berlin52_formatted.tsp", cities)
print("-----")
individuals = Individual(52, initialize=True)
individuals.print_route()
individuals.calculate_distance(cities)
print("......")

individual_a = Individual(52, initialize=True)
individual_b = Individual(52, initialize=True)
child = crossover(individual_a, individual_b)


num_individuals = 100
prob_mutate = 0.1

# initialize
individuals = list()
for i in range(num_individuals):
    individuals.append(Individual(len(cities), initialize=True))

while True:
    # Selection
    best_distance = individuals[0].calculate_distance()
    next_best_distance = individuals[1].calculate_distance()
    best_individuals = list()
    best_individuals.append(individuals[0])
    best_individuals.append(individuals[1])

    if next_best_distance < best_distance:
        best_distance, next_best_distance = next_best_distance, best_distance
        best_individuals[0], best_individuals[1] = best_individuals[1], best_individuals[0]

    for individual in individuals:
        this_distance = individual.calculate_distance(cities)

        if this_distance < next_best_distance:
            if this_distance < best_distance:
                # Replace best individual
                best_individuals[0] = individual
                best_distance = this_distance
            else:
                # Replace next best individual
                best_individuals[1] = individual
                next_best_distance = this_distance

    for i in range(num_individuals-2):
        # Crossover
        # Mutation
    # Replacement




# for individual in individuals:
#    for i in range(cities.count()):
#        individual.route[i]
#    print(individual.route)



# Create initial random population
# While termination criteria is not satisfied:
#   Evaluate fitness of each individual
#   IF Termination criteria satisfied:
#       Stop and return the best one in the population
#   ELSE:
#   Select parents according to fitness
#   Recombine parents to generate a set of offspring
#   Mutate offspring
#   Replace population by the set of new offspring

