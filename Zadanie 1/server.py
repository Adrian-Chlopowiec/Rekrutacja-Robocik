import sys
from boat import Boat


def main(n=5, t=1):
    if n < 5:
        raise Exception("N must be greater than 5")
    if t <= 0:
        raise Exception("T must be grater than 0")

    boat = Boat()
    boat.start_server(n, t)
    boat.manage_requests()


if __name__ == "__main__":
    """
    :param sys.argv[1]: N - number of coordinates to be sent by boat
    :param sys.argv[2]: T - delay between sending coordinates in seconds    
    """
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), int(sys.argv[2]))
    else:
        main()
