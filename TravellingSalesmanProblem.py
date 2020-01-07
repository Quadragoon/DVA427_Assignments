from math import *
import random
import lab_library as lablib

cities = list()


def import_data_2(filename):
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
    def __init__(self, initialize=False):
        self.route = []
        if initialize is True:
            for i in range(1, cities.__len__()):
                self.route.append(i)
            random.shuffle(self.route)
        self.distance = -1

    def print_route(self):
        print("Route:", self.route)
        return

    def calculate_distance(self):
        # print("Calculate distance:")
        # for city in self.route:
        #    print("[", city, cities[city].x, cities[city].y, "]")

        distance_sum = 0

        # calculate distance from the start point to the first step on the route
        delta = distance(cities[0], cities[self.route[0]])
        # add that distance to total distance traveled
        distance_sum += delta
        # print("d:[ S ] [", delta, "]")

        for i in range(self.route.__len__() - 1):
            # calculate distance from each destination to the next
            delta = distance(cities[self.route[i]], cities[self.route[i+1]])
            # add up the distances
            distance_sum += delta
            # print("d:[", i, "to", i+1, "] [", delta, "]")

        # calculate distance from the last step on the route to the end point
        delta = distance(cities[self.route[-1]], cities[0])
        # add that distance to total distance traveled
        distance_sum += delta
        # print("d:[ E ] [", delta, "]")

        print("DISTANCE SUM: [", distance_sum, "]")
        self.distance = distance_sum
        return distance_sum

    def mutate(self):
        length = (len(self.route))
        pos1 = round(random.random() * length)
        pos2 = pos1
        while pos2 == pos1:
            pos2 = round(random.random() * length)

        self.route[pos1] = self.route[pos2]


def crossover(parent_a, parent_b):
    print("crossover:")
    # route_a = parent_a.route.copy()
    # route_b = parent_b.route.copy()

    route_a = [7, 3, 1, 8, 2, 4, 6, 5]
    route_b = [7, 5, 2, 8, 4, 3, 1, 6]
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

import_data_2("berlin52_formatted.tsp")
print("-----")
population = Individual(initialize=True)
population.print_route()
population.calculate_distance()
print("......")

individual_a = Individual(initialize=True)
individual_b = Individual(initialize=True)
child = crossover(individual_a, individual_b)


num_individuals = 100
prob_crossover = 0.8

population_size = 100
prob_mutation = 0.1

# initialize
population = list()
while population.__len__() < population_size:
    population.append(Individual(initialize=True))

while True:
    # Selection
    best_distance = population[0].calculate_distance()
    next_best_distance = population[1].calculate_distance()
    best_individuals = list()
    best_individuals.append(population[0])
    best_individuals.append(population[1])

    if next_best_distance < best_distance:
        best_distance, next_best_distance = next_best_distance, best_distance
        best_individuals[0], best_individuals[1] = best_individuals[1], best_individuals[0]

    for individual in population:
        this_distance = individual.calculate_distance()

        if this_distance < next_best_distance:
            if this_distance < best_distance:
                # Replace best individual
                best_individuals[0], best_individuals[1] = individual, best_individuals[0]
                best_distance, next_best_distance = this_distance, best_distance
            else:
                # Replace next best individual
                best_individuals[1] = individual
                next_best_distance = this_distance

        # Crossover

        # Mutation
    for individual in population:
        if random.random() >= prob_mutation:
            individual.mutate()

    # population.sort(key=lambda x: x.calculate_distance())

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
