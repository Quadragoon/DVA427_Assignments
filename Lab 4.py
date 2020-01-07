from math import *
import random
import lab_library as lablib
import operator
import numpy as np


infinity = 999999
num_nodes = 10


class Dijkstra_node:
    def __init__(self):
        self.distance_to_target = infinity
        self.neighbour_distances = dict()
        self.best_neighbour = "bonsly"

    def add_neighbour(self, neighbour_id, distance):
        self.neighbour_distances[neighbour_id] = distance


# because we're not only importing numbers, we have to use a custom import function
def import_data_from_file(filename):
    data_file = open(filename, mode="r")

    line = data_file.readline()
    while line != "@data\n":
        line = data_file.readline()

    print("Found data start, processing...")

    all_data = []

    for line in data_file:
        if not any(character.isdigit() for character in line):
            continue
        all_data.append(list(line.split(" ")))

    data_count = len(all_data)
    print("Total number of data points: " + data_count.__str__())
    return all_data


data_points = import_data_from_file("city 1.txt")
nodes = dict()
for data_point in data_points:
    first_node = data_point[0]
    second_node = data_point[1]
    distance = int(data_point[2])

    if first_node not in nodes.keys():
        nodes[first_node] = Dijkstra_node()  # create new node and add it to the dictionary of nodes
    nodes[first_node].add_neighbour(second_node, distance)

    if second_node not in nodes.keys():
        nodes[second_node] = Dijkstra_node()  # create new node and add it to the dictionary of nodes
    nodes[second_node].add_neighbour(first_node, distance)

# Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set
# Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other
# nodes. Set the initial node as current

current_node_id = "F"
current_node = nodes[current_node_id]
current_node.distance_to_target = 0
unvisited_nodes = nodes.copy()

while True:
    # For the current node, consider all of its unvisited neighbours and calculate their tentative distances through the
    # current node.Compare the newly calculated tentative distance to the current assigned value and assign the smaller
    # one. For example, if the current node A is marked with a distance of 6, and the edge connecting it with a
    # neighbour B has length 2, then the distance to B through A will be 6 + 2 = 8. If B was previously marked with a
    # distance greater than 8 then change it to 8. Otherwise, the current value will be kept

    for neighbour_id in current_node.neighbour_distances:
        if neighbour_id in unvisited_nodes.keys():
            node_distance = current_node.distance_to_target + current_node.neighbour_distances[neighbour_id]
            if node_distance < nodes[neighbour_id].distance_to_target:
                nodes[neighbour_id].distance_to_target = node_distance
                nodes[neighbour_id].best_neighbour = current_node_id
    # When we are done considering all of the unvisited neighbours of the current node, mark the current node as visited and
    # remove it from the unvisited set. A visited node will never be checked again.
    unvisited_nodes.pop(current_node_id)
    if len(unvisited_nodes) == 0:
        break

    # this isn't elegant (by python standards) but it works
    lowest_tentative_distance = infinity
    for possible_next_node in unvisited_nodes:
        if unvisited_nodes[possible_next_node].distance_to_target < lowest_tentative_distance:
            lowest_tentative_distance = unvisited_nodes[possible_next_node].distance_to_target
            current_node_id = possible_next_node
            current_node = nodes[current_node_id]

    # If the smallest tentative distance among the nodes in the unvisited set is infinity (when planning a complete
    # traversal; occurs when there is no connection between the initial node and remaining unvisited nodes), then stop.
    # The algorithm has finished.

    # Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new "current
    # node", and go back to step 3.

for node_id in nodes:
    if nodes[node_id].distance_to_target == 0: # trying to find a path from the target to the target will get weird...
        continue  # ... so we won't try doing that
    location = node_id
    print(location, "->", nodes[location].best_neighbour, end="")
    location = nodes[location].best_neighbour
    while location != "F":
        print(" ->", nodes[location].best_neighbour, end="")
        location = nodes[location].best_neighbour
    print("")
