import json
import random
import socket
from time import sleep


class Boat:
    """
    Class responsible for sending location of imaginary boat to the client through http protocole
    """
    def __init__(self):
        """
        :var self.server: socket for managing connection
        """
        self.server = None
        self.n = None
        self.t = None

    def start_server(self, n: int, t: int):
        """
        Creates socket connection to localhost on port 8000
        :param n: number of localizations to send
        :param t: delay between localizations
        :return: None
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 8000))
        self.n = n
        self.t = t

    def manage_requests(self):
        """
        Manages get requests send to the server
        :return: None
        """
        self.server.listen(5)
        client, address = self.server.accept()
        for _ in range(self.n):
            self.__send_response(client, json.dumps(
                {"localization": (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)),
                 "time": self.t}))
            sleep(self.t)

        self.__send_response(client, json.dumps({"localization": "stop", "time": self.t}))
        client.close()

    def __send_response(self, client: socket.socket, body: json):
        """
        Sends response to the client
        :param client: socket of a client
        :param body: message to send
        :return: None
        """
        client.send(bytes("HTTP/1.1 200 OK\n"
                          + "Content-Type: application/json\n"
                          + "Content-Length: " + str(len(body)) + "\n"
                          + "Connection: close" + "\n"
                          + "\n"
                          + body + '\n', "utf-8"))
