from speedometer import Speedometer
from clientmanager import Client


def main():
    speedometer = Speedometer()
    client = Client()
    client.manage_client()
    client.send_requests(speedometer)


if __name__ == "__main__":
    main()
