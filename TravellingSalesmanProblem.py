from math import *
import random
import lab_library as lablib
import operator
import numpy as np

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

        # print("DISTANCE SUM: [", distance_sum, "]")
        self.distance = distance_sum
        return distance_sum

    def mutate(self):
        length = (len(self.route))
        pos1 = random.randrange(0, length)
        pos2 = pos1
        while pos2 == pos1:
            pos2 = random.randrange(0, length)

        self.route[pos1] = self.route[pos2]


def crossover(parent_a, parent_b):
    route_a = parent_a.route
    route_b = parent_b.route

    crossover_length = random.randrange(5, 10)
    crossover_start_index = random.randrange(0, route_a.__len__() - crossover_length)
    crossover_end_index = crossover_start_index + crossover_length

    crossover_set = route_a[crossover_start_index:crossover_end_index]

    difference_set = [x for x in route_b if x not in crossover_set]

    route_c = []
    for i in range(crossover_start_index):
        route_c.append(difference_set[i])
    for element in crossover_set:
        route_c.append(element)
    for i in range(crossover_start_index, len(difference_set)):
        route_c.append(difference_set[i])

    return route_c


import_data_2("berlin52_formatted.tsp")

population_size = 100
prob_crossover = 1.0
prob_mutation = 0.2

# initialize
population = list()
while population.__len__() < population_size:
    population.append(Individual(initialize=True))

while True:
    # Selection
    # Sort based on distance
    for individual in population:
        individual.calculate_distance()
    key_function = operator.attrgetter("distance")
    population.sort(key=key_function, reverse=False)

    fitness_ratings = list()
    total_fitness = 0
    for individual in population:
        fitness_ratings.append((individual.distance - population[-1].distance) ** 5)
        total_fitness += fitness_ratings[-1]

    probability_distribution = list()
    for fitness in fitness_ratings:
        weighted_probability = fitness / total_fitness
        probability_distribution.append(weighted_probability)

    # Create children
    children = list()
    for i in range(population_size):
        parents = np.random.choice(population, 2, p=probability_distribution, replace=False)
        # Crossover
        child = Individual()
        child.route = crossover(parents[0], parents[1])
        # Mutation
        if random.random() <= prob_mutation:
            child.mutate()

    # population.sort(key=lambda x: x.calculate_distance())

    # Replacement


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
