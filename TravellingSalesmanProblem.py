from math import *


def distance(p1, p2):
    return sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


a = Point(0, 0)
b = Point(1, 0)

print(distance(a, b))



