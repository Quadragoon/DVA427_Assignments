#################################################################################
# DEFINITIONS AND DECLARATIONS ##################################################
#################################################################################

infinity = 999999


class DijkstraNode:
    def __init__(self):
        self.distance_to_target = infinity
        self.neighbour_distances = dict()
        self.best_neighbour = "bonsly"

    def add_neighbour(self, neighbour_id, distance):
        self.neighbour_distances[neighbour_id] = distance


# because we're not only importing numbers, we have to use a custom import function
def import_node_data_from_file(filename):
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

    for data_point in all_data:
        first_node = data_point[0]
        second_node = data_point[1]
        distance = int(data_point[2])

        # Each line in the data represents two neighbour relations: a path from first_node to second_node and
        # a path from second_node to first_node.
        # If these nodes don't already exist, we create them. After that check we add their new neighbours.
        if first_node not in nodes.keys():
            nodes[first_node] = DijkstraNode()  # create new node and add it to the dictionary of nodes
        nodes[first_node].add_neighbour(second_node, distance)  # add the other node as a neighbour

        if second_node not in nodes.keys():
            nodes[second_node] = DijkstraNode()  # create new node and add it to the dictionary of nodes
        nodes[second_node].add_neighbour(first_node, distance)  # add the other node as a neighbour


#################################################################################
# CODE EXECUTION ################################################################
#################################################################################

nodes = dict()
import_node_data_from_file("city 1.txt")

target_id = "F"  # set the target/source node to the one we want to find distances to
current_node_id = target_id  # remember the current node identifier for later
current_node = nodes[current_node_id]  # remember the current node object for later
current_node.distance_to_target = 0  # our target will always have a distance of 0
unvisited_nodes = nodes.copy()  # create a set of unvisited nodes (containing every node)

while len(unvisited_nodes) > 0:
    # For the current node, consider all of its unvisited neighbours and calculate their tentative distances through the
    # current node. Compare the newly calculated tentative distance to the current assigned value and assign the smaller
    # one.
    # Each node will remember which neighbour allowed the shortest distance. This will allow finding the shortest path.

    for neighbour_id in current_node.neighbour_distances:
        if neighbour_id in unvisited_nodes.keys():
            node_distance = current_node.distance_to_target + current_node.neighbour_distances[neighbour_id]
            if node_distance < nodes[neighbour_id].distance_to_target:
                nodes[neighbour_id].distance_to_target = node_distance
                nodes[neighbour_id].best_neighbour = current_node_id

    # When we are done considering all of the unvisited neighbours of the current node, remove the current node
    # from the unvisited set. A visited node will never be checked again.
    unvisited_nodes.pop(current_node_id)

    # Find the unvisited node with the shortest tentative distance and mark it as the current node.
    # this code isn't elegant (by python standards) but it works
    lowest_tentative_distance = infinity
    for possible_next_node in unvisited_nodes:
        if unvisited_nodes[possible_next_node].distance_to_target < lowest_tentative_distance:
            lowest_tentative_distance = unvisited_nodes[possible_next_node].distance_to_target
            current_node_id = possible_next_node
            current_node = nodes[current_node_id]

# print out each node's shortest path to the target by printing the best neighbour until we're there
for node_id in nodes:
    if nodes[node_id].distance_to_target == 0:  # trying to find a path from the target to the target will get weird...
        continue  # ... so we won't try doing that
    print(node_id, "->", nodes[node_id].best_neighbour, end="")
    location = nodes[nodes[node_id].best_neighbour]
    while location != nodes[target_id]:
        print(" ->", location.best_neighbour, end="")
        location = nodes[location.best_neighbour]
    print("")
