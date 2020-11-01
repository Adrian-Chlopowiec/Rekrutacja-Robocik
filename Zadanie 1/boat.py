import json
import socket
import random
import sys
from time import sleep


def send_response(client, body):
    client.send(bytes("HTTP/1.1 200 OK\n"
                      + "Content-Type: application/json\n"
                      + "Content-Length: " + str(len(body)) + "\n"
                      + "Connection: close" + "\n"
                      + "\n"
                      + body + '\n', "utf-8"))


def main():
    n = int(sys.argv[1])
    if n < 5:
        raise Exception("N must be greater than 5")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 8000))
    server.listen(5)

    client, address = server.accept()
    for _ in range(n):
        send_response(client, json.dumps(
            {"localization": (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)),
             "time": sys.argv[2]}))
        sleep(int(sys.argv[2]))

    send_response(client, json.dumps({"localization": "stop", "time": sys.argv[2]}))
    client.close()


if __name__ == "__main__":
    main()
