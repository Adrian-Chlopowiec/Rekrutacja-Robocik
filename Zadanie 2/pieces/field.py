class Field:
    def __init__(self, x: int, y: int):
        self.location = (x, y)

    def to_string(self):
        return {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
