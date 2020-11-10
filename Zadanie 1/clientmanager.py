import socket

from speedometer import Speedometer


def parse_response(response: str):
    """
    Parses response to retrieve point and time from its body.\n
    :param response: str
    :return: dict: contains point and time
    """
    lines = response.splitlines()
    loc_and_time = lines[-1].split(sep=', "')
    point = loc_and_time[0].split(sep=": ")[1]
    time = loc_and_time[1].split(sep=": ")[1][:-1]
    return {"point": point, "time": int(time)}


def convert_to_list(string: str):
    """
    Converts string of coordinates to list.\n
    :param string: str: string of coordinates
    :return: list
    """
    values = string.split(sep=", ")
    values[0] = values[0][1:]
    values[-1] = values[-1][:-1]
    return [int(x) for x in values]


class Client:
    """
    Class responsible for retrieving object localization through http protocol\n
    :param client: socket for managing connection
    """
    def __init__(self):
        self.client = None

    def manage_client(self):
        """
        Creates connection between Client and server\n
        :return: None
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), 8000))

    def send_requests(self, speedometer: Speedometer):
        """
        Sends requests for localization to the object until receiving stop message\n
        :param speedometer: Speedometer
        :return: None
        """
        stop_signal_sent = False
        while not stop_signal_sent:
            request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % socket.gethostname()
            self.client.send(request.encode())
            response = self.client.recv(4096)
            stop_signal_sent = self.__parse_and_print_response(response, speedometer)

    def __parse_and_print_response(self, response: bytes, speedometer: Speedometer):
        """
        Parses response to retrieve point and time from its body, then prints them.\n
        :param response: bytes: containing information about localization of the object
        :param speedometer: Speedometer
        :return: Boolean: signals whether stop message was sent
        """
        dict_of_strings = parse_response(response.decode())
        if dict_of_strings["point"] == '"stop"':
            return True
        else:
            point, time = convert_to_list(dict_of_strings["point"]), dict_of_strings["time"]
            print(str("Average speed: " + str(speedometer.avg_speed(tuple(point), time))) +
                  " | Localization: " + str(point) + " | Time since last signal: " + str(time))
        return False
