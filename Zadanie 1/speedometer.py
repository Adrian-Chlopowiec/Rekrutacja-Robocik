import math


class Speedometer:
    def __init__(self):
        self.last_point = (0, 0, 0)

    def avg_speed(self, point, time):
        distance = self.__calc_distance(self.last_point, point)
        self.last_point = point
        return distance / time

    def __calc_distance(self, start, end):
        return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2 + (end[2] - start[2])**2)
