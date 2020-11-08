from typing import List
from chessboard import Chessboard, queue_to_list


def parse_input(string: str) -> List[List[str]]:
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
    chessboard.find_possible_mating_pieces()
    chessboard.find_moves_for(queue_to_list(chessboard.possible_mating_pieces))
    mate = chessboard.check_for_mates()
    if mate is None:
        print("Biały nie może wygrać w jednym ruchu")
    else:
        print("Biały może wygrać " + mate[0].to_string() + " - " + mate[1].to_string())


if __name__ == "__main__":
    main()
