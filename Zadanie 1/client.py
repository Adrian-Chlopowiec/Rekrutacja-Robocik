import socket
from speedometer import Speedometer


def parse_response(response: str):
    lines = response.splitlines()
    loc_and_time = lines[-1].split(sep=', "')
    point = loc_and_time[0].split(sep=": ")[1]
    time = loc_and_time[1].split(sep=": ")[1][1:-2]
    return {"point": point, "time": int(time)}


def convert_to_list(string: str):
    values = string.split(sep=", ")
    values[0] = values[0][1:]
    values[-1] = values[-1][:-1]
    return [int(x) for x in values]


def connect(speedometer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 8000))

    end_flag = True
    while end_flag:
        request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % socket.gethostname()
        client.send(request.encode())
        response = client.recv(4096)
        dict_of_strings = parse_response(response.decode())
        if dict_of_strings["point"] == '"stop"':
            end_flag = False
        else:
            point, time = convert_to_list(dict_of_strings["point"]), dict_of_strings["time"]
            print(str(speedometer.avg_speed(point, time)) + " " + str(point) + " " + str(time))


def main():
    speedometer = Speedometer()
    connect(speedometer)


if __name__ == "__main__":
    main()
