import math


class Speedometer:
    """
    Class responsible for calculation average speed of an object
    """
    def __init__(self):
        """
        :var self.last_point: tuple of coordinates of last localization of the object
        """
        self.last_point = (0, 0, 0)

    def avg_speed(self, point: tuple, time):
        """
        Calculates average speed of an object based on sent point and last point
        :param point: tuple of coordinates of the object
        :param time: time since last coordinates were sent
        :return: float: average speed of an object
        """
        distance = self.__calc_distance(self.last_point, point)
        self.last_point = point
        return distance / time

    def __calc_distance(self, start, end):
        """
        Calculates distance between start and end
        :param start: tuple of coordinates of starting point
        :param end: tuple of coordinates of ending point
        :return: float: distance
        """
        return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2 + (end[2] - start[2])**2)
