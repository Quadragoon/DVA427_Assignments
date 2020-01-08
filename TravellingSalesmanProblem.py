from math import *
import random
import lab_library as lablib
import operator
import numpy as np


cities = list()


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
        distance_sum = 0

        # calculate distance from the start point to the first step on the route
        delta = distance(cities[0], cities[self.route[0]])
        # add that distance to total distance traveled
        distance_sum += delta

        for i in range(self.route.__len__() - 1):
            # calculate distance from each destination to the next
            delta = distance(cities[self.route[i]], cities[self.route[i+1]])
            # add up the distances
            distance_sum += delta

        # calculate distance from the last step on the route to the end point
        delta = distance(cities[self.route[-1]], cities[0])
        # add that distance to total distance traveled
        distance_sum += delta

        self.distance = distance_sum
        return distance_sum

    def mutate(self):
        length = len(self.route)
        pos1 = random.randrange(0, length)
        pos2 = pos1
        while pos2 == pos1:
            pos2 = random.randrange(0, length)

        self.route[pos1], self.route[pos2] = self.route[pos2], self.route[pos1]

    def mutate_reversal(self):
        length = (len(self.route))
        mutation_length = random.randrange(1, length)
        mutation_start = random.randrange(0, length - mutation_length)
        mutation_end = mutation_start + mutation_length

        mutated_section = self.route[mutation_start:mutation_end]
        mutated_section.reverse()
        self.route[mutation_start:mutation_end] = mutated_section


def create_crossover_route(parent_a, parent_b):
    route_a = parent_a.route
    route_b = parent_b.route

    # decide which parts of the genetic material to copy over from parent A
    crossover_length = random.randrange(2, 15)
    crossover_start_index = random.randrange(0, len(route_a) - crossover_length)
    crossover_end_index = crossover_start_index + crossover_length

    # create the set of route information to be crossed over from A
    crossover_set = route_a[crossover_start_index:crossover_end_index]

    # create the set that contains every route stop that isn't in the crossover set, and take this from parent B
    difference_set = [x for x in route_b if x not in crossover_set]

    route_c = []
    # copy from difference set until we reach the start index of crossover
    for i in range(crossover_start_index):
        route_c.append(difference_set[i])
    # then copy the entire crossover set
    for element in crossover_set:
        route_c.append(element)
    # then resume copying from the difference set
    for i in range(crossover_start_index, len(difference_set)):
        route_c.append(difference_set[i])

    return route_c


imported_data = lablib.import_data_from_file("berlin52_formatted.tsp", 3, has_classification=False, sep=" ")
for data_point in imported_data:
    x = data_point.attributes[1]
    y = data_point.attributes[2]
    cities.append(City(x, y))

population_size = 20
prob_crossover = 1.0
prob_mutation = 0.5
prob_mutation_reversal = 0.5

# initialize
population = list()
while population.__len__() < population_size:
    population.append(Individual(initialize=True))

best_dist = 99999
stagnation = 0
infinity = 10000000000

while stagnation <= infinity:
    # Selection
    # Sort based on distance
    for individual in population:
        individual.calculate_distance()
    key_function = operator.attrgetter("distance")
    population.sort(key=key_function, reverse=False)

    # Find individual with shortest route
    if population[0].distance < best_dist:
        best_dist = population[0].distance
        print(best_dist)
        stagnation = 0
    else:
        stagnation += 1
        if stagnation % 1000 == 0:
            print(stagnation, "generations without improvement...")

    fitness_ratings = list()
    total_fitness = 0
    for individual in population:
        # fitness ratings are based on distance compared to the worst distance in the population, scaled by a power of 5
        fitness_ratings.append((individual.distance - population[-1].distance) ** 5)
        total_fitness += fitness_ratings[-1]

    probability_distribution = list()  # Create custom probability function
    for fitness in fitness_ratings:
        weighted_probability = fitness / total_fitness
        probability_distribution.append(weighted_probability)

    # Create children
    children = list()
    children.append(population[0])  # elitism

    # one quarter of the population will be entirely new, random individuals
    random_portion = floor(population_size/4)
    for i in range(1, random_portion):
        children.append(Individual(initialize=True))

    # fill in the remaining three-quarters of the population with children of parents selected by fitness
    for i in range(random_portion, population_size):
        parents = np.random.choice(population, 2, p=probability_distribution, replace=False)
        # Crossover
        child = Individual()
        child.route = create_crossover_route(parents[0], parents[1])
        # Mutation
        if random.random() <= prob_mutation:
            child.mutate()
        if random.random() <= prob_mutation_reversal:
            child.mutate_reversal()
        children.append(child)

    # Replacement
    population = children


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
