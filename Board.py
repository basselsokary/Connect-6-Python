import itertools
from static import EMPTY, WHITE, BLACK

class Board:
    def __init__(self, size: int = 19):
        self.size = size
        self.occupied_cells = set()
        # self.all_empty_cells = list(itertools.product(range(size), range(size)))
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]

    def check_draw(self) -> bool:
        for row in self.board:
            for elem in row:
                if elem == EMPTY:
                    return False
        return True

    def check_win(self, row, col, symbol) -> bool:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # All directions

        for dr, dc in directions:
            count = 1  # Start with the current stone

            # Positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                r += dr
                c += dc

            # Negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                r -= dr
                c -= dc

            if count >= 6:
                return True

        return False

    def check_win_whole_board(self, symbol) -> bool:
        def _check_line(line: list[int], player_symbol: str) -> bool:
            """
            Check if a given line contains 6 consecutive player_symbol.

            :param line: A list representing a row or column.
            :param player_symbol: The symbol of the player ('B' or 'W').
            :return: True if 6 consecutive symbols are found, False otherwise.
            """
            count = 0
            for cell in line:
                if cell == player_symbol:
                    count += 1
                    if count == 6:
                        return True
                else:
                    count = 0
            return False

        for line in range(self.size):
            if _check_line(self.get_row(line), symbol) or _check_line(self.get_column(line), symbol):
                return True
            
        for diagonal in self.get_diagonals():
            if _check_line(diagonal, symbol):
                return True
            
        return False

    def valid_move(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == EMPTY

    def display_board(self):
        for row in self.board:
            for elem in row:
                print(f'{elem}|', end='')
            print()

    def move(self, row, col, symbol) -> bool:
        if self.valid_move(row, col):
            self.board[row][col] = symbol
            self.occupied_cells.add((row, col)) # Add move(x, y) to occupied cells
            # self.all_empty_cells.remove((row, col))
            # self.update_occupied_cells(row, col)
            return True
        return False

    def undo_move(self, row: int, col: int) -> bool:
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] != EMPTY:
            self.board[row][col] = EMPTY
            # self.all_empty_cells.append((row, col))
            self.occupied_cells.remove((row, col)) # Remove move(x, y) from occupied cells
            return True
        return False

    def get_row(self, row: int) -> list[int]:
        return self.board[row]

    def get_column(self, col: int) -> list[int]:
        return [self.board[row][col] for row in range(self.size)]

    def get_diagonals(self):
        n = self.size
        diagonals = []

        # Top-left to bottom-right diagonals
        for dig in range(n + n - 1):
            temp = []
            for row in range(max(0, dig - n + 1), min(n, dig + 1)):
                col = dig - row
                if 0 <= col < n:
                    temp.append(self.board[row][col])
            diagonals.append(temp)

        # Top-right to bottom-left diagonals
        for dig in range(-n + 1, n):
            temp = []
            for row in range(max(0, dig), min(n, n + dig)):
                col = row - dig
                if 0 <= col < n:
                    temp.append(self.board[row][col])
            diagonals.append(temp)

        return diagonals

    def get_adjacent_cells(self):
        """Finds all empty cells adjacent to any occupied cell."""
        adjacent_moves = set()  # Using a set to avoid duplicates
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        # directions = [
        #     (dx, dy)
        #     for dx in range(-2, 3)  # Include -2, -1, 0, 1, 2
        #     for dy in range(-2, 3)
        #     if not (dx == 0 and dy == 0)  # Exclude the center cell itself
        # ]

        for x, y in self.occupied_cells:
            if self.board[x][y] != EMPTY:  # Check if the cell is occupied
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if self.valid_move(nx, ny):
                        adjacent_moves.add((nx, ny))

        # return list(adjacent_moves)
        return adjacent_moves

    def reset_board(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.occupied_cells = set()
        
    def game_over(self):
        return self.check_draw() or self.check_win_whole_board(WHITE) or self.check_win_whole_board(BLACK)
    
    def update_occupied_cells(self, row, col):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for dx, dy in directions:
            r, c = dx + row, dy + col
            if self.valid_move(r, c):
                self.occupied_cells.add((r, c))