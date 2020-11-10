from typing import List
from chessboard import Chessboard


def parse_input(string: str) -> List[List[str]]:
    """
    Parses input string to matrix of strings containing representations of chess pieces and fields.
    :param string: input
    :return: matrix of strings
    """
    array = string.splitlines()
    matrix = list()
    for line in array:
        line = line[1:-1]
        encoded_pieces = line.split(sep=", ")
        for i in range(len(encoded_pieces)):
            encoded_pieces[i] = encoded_pieces[i][1:-1]
        matrix.append(encoded_pieces)
    return matrix


def main():
    string = ""
    for _ in range(8):
        string += input() + '\n'
    matrix = parse_input(string)
    chessboard = Chessboard(matrix)
    chessboard.find_mate()


if __name__ == "__main__":
    main()
