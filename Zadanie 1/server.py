import sys
from boat import Boat


def main(n=5, t=1):
    if n < 5:
        raise Exception("N must be greater than 5")

    boat = Boat()
    boat.start_server(n, t)
    boat.manage_requests()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), int(sys.argv[2]))
    else:
        main()
