from math import *
import random
import lab_library as lablib
import operator
import numpy as np


infinity = 999999
num_nodes = 10


class Node:
    def __init__(self, id):
        self.id = id
        self.distances = list()

        for i in range(num_nodes):
            if i == self.id:
                self.distances.append(0)
            else:
                self.distances.append(infinity)


# Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set
unvisited_nodes = list()
# Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other
# nodes. Set the initial node as current
nodes = list()
for i in range(num_nodes):
    nodes.append(Node(id=i))
    unvisited_nodes.append(i)


current_node = 0

while True:
    # For the current node, consider all of its unvisited neighbours and calculate their tentative distances through the
    # current node.Compare the newly calculated tentative distance to the current assigned value and assign the smaller
    # one. For example, if the current node A is marked with a distance of 6, and the edge connecting it with a
    # neighbour B has length 2, then the distance to B through A will be 6 + 2 = 8. If B was previously marked with a
    # distance greater than 8 then change it to 8. Otherwise, the current value will be kept

    # neighbors = [x for x in node.distances if x < infinity]
    neighbors = [x for x in nodes if x.distances < infinity]

    for neighbor in neighbors:
        nodeDistance = nodes[current_node].distances[current_node] + neighbor.distances[current_node]
        if nodeDistance < neighbor.distances[current_node]
            neighbor.distances = nodeDistance
    # When we are done considering all of the unvisited neighbours of the current node, mark the current node as visited and
    # remove it from the unvisited set. A visited node will never be checked again.
    unvisited_nodes.pop(current_node)

    # If the smallest tentative distance among the nodes in the unvisited set is infinity (when planning a complete
    # traversal; occurs when there is no connection between the initial node and remaining unvisited nodes), then stop.
    # The algorithm has finished.

    # Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new "current
    # node", and go back to step 3.


