from Board import Board


class Player:
    def __init__(self, name, symbol: str):
        self.name = name
        self.symbol = symbol

    def move(self, board: Board, row, col):
        if board.move(row, col, self.symbol):
            return True
        return False

