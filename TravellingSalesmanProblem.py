from math import *
import random


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


def distance(p1, p2):
    return sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Individual:
    def __init__(self, num_cities, initialize=False):
        self.route = []
        if initialize is True:
            for i in range(num_cities):
                self.route.append(i)
            random.shuffle(self.route)

    def print_route(self):
        print("Route:", self.route)
        return

    def calculate_distance(self, cities):
        print("Calculate distance:")
        for city in self.route:
            print("[", city, cities[city].x, cities[city].y, "]")
        sum = 0
        for i in range(52):
            delta = distance(cities[self.route[i-1]], cities[self.route[i]])
            sum += delta
            print("d:[", i, "] [", delta, "]")
        print("SUM: [", sum, "]")
        return sum

    def mutate(self):
        length = float(len(self.route))
        pos1 = random.random()*length
        pos2 = pos1
        while pos2 == pos1:
            pos2 = random.random()*length

        # switch elements
        self.route[pos1], self.route[pos2] = self.route[pos2], self.route[pos1]



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

    return route_c

a = Point(0, 0)
b = Point(1, 0)

print(distance(a, b))

cities = list()
import_data("berlin52_modified", cities)
print("-----")
individuals = Individual(52, initialize=True)
individuals.print_route()
individuals.calculate_distance(cities)
print("......")

individual_a = Individual(52, initialize=True)
individual_b = Individual(52, initialize=True)
child = crossover(individual_a, individual_b)
print(".....", child)


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

