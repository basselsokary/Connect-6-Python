import random
import time

from Board import Board
from HeuristicEvaluator import HeuristicEvaluator
from static import EMPTY, WHITE, BLACK, DIRECTIONS

class AIPlayer:
    def __init__(self, symbol, heu = 1, alpha_beta = True, depth = 3):
        self.name = 'Computer'
        self.depth = depth
        self.symbol = symbol
        self.opponent = WHITE if self.symbol == BLACK else BLACK # 1 for BLACK, 2 for WHITE, and 0 for blanks
        self.sorted_cells = []
        self.heuristic = heu # 1 for first heuristic function, x for the other one
        self.alpha_beta = alpha_beta

    def move(self, board: Board):
        if self.alpha_beta:
            _, row1, col1, row2, col2 = self.minimax_alpha_beta(board, self.depth, True, float('-inf'), float('inf'))
        else:
            _, row1, col1, row2, col2 = self.minimax(board, self.depth, True)
        print(f'alpha-beta => {self.alpha_beta}')
        if not board.move(row1, col1, self.symbol) or not board.move(row2, col2, self.symbol):
            if not self.move_center(board):
                return self.move_randomly(board)
        return row1, col1, row2, col2
    
    def minimax_alpha_beta(self, board: Board, depth: int, is_maximizing: bool, alpha, beta):
        game_over = board.game_over()
        if depth == 0 or game_over:
            if game_over:
                if board.check_win_whole_board(self.symbol):
                    return (float('inf'), -1, -1, -1, -1)
                elif board.check_win_whole_board(self.opponent):
                    return (-2_000_000, -1, -1, -1, -1)
                else:
                    return (0, -1, -1, -1, -1)
            if self.heuristic == 1:
                return HeuristicEvaluator.evaluate_board(board, self.symbol, self.opponent), -1, -1, -1, -1
            return HeuristicEvaluator.evaluate_board2(board, self.symbol, self.opponent), -1, -1, -1, -1
        
        def get_nighboors_of_cell(row, col):
            nighboor = set()
            for dx, dy in DIRECTIONS:
                if board.valid_move(row + dx, col + dy):
                    nighboor.add((row + dx, col + dy))
            return nighboor
                    
        best_moves = (-1, -1, -1, -1)  # Best pair of moves: (row1, col1, row2, col2)
        
        # adjacent_cells = set(self.order_moves(board, board.get_adjacent_cells(), is_maximizing))
        adjacent_cells = board.get_adjacent_cells()

        if is_maximizing:
            max_eval = float('-inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.symbol)  # First move
                adjacent_cells = adjacent_cells.union(get_nighboors_of_cell(x1, y1))
                for x2, y2 in adjacent_cells:
                    if (x2, y2) == (x1, y1):
                        continue
                    board.move(x2, y2, self.symbol)  # Second move
                    score = self.minimax_alpha_beta(board, depth - 1, False, alpha, beta)[0]
                    board.undo_move(x2, y2)  # Undo second move
                    if score > max_eval:
                        max_eval = score
                        best_moves = (x1, y1, x2, y2)
                    alpha = max(alpha, score)
                    if self.alpha_beta_pruning(alpha, beta):
                        board.undo_move(x1, y1)  # Undo first move
                        break
                if self.alpha_beta_pruning(alpha, beta):
                    break
                else:
                    board.undo_move(x1, y1)  # Undo first move
            return max_eval, best_moves[0], best_moves[1], best_moves[2], best_moves[3]
        else:
            min_eval = float('inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.opponent)  # First move
                adjacent_cells = adjacent_cells.union(get_nighboors_of_cell(x1, y1))
                for x2, y2 in adjacent_cells:
                    if (x2, y2) == (x1, y1):
                        continue
                    board.move(x2, y2, self.opponent)  # Second move
                    score = self.minimax_alpha_beta(board, depth - 1, True, alpha, beta)[0]
                    print(f'Opp score: {score}')
                    board.undo_move(x2, y2)  # Undo second move
                    if score < min_eval:
                        min_eval = score
                        best_moves = (x1, y1, x2, y2)
                    beta = min(beta, score)
                    if self.alpha_beta_pruning(alpha, beta):
                        board.undo_move(x1, y1)  # Undo first move
                        break
                if self.alpha_beta_pruning(alpha, beta):
                    break
                else:
                    board.undo_move(x1, y1)  # Undo first move
            return min_eval, best_moves[0], best_moves[1], best_moves[2], best_moves[3]

    def minimax(self, board: Board, depth: int, is_maximizing: bool):
        game_over = board.game_over()
        if depth == 0 or game_over:
            if game_over:
                if board.check_win_whole_board(self.symbol):
                    return (float('inf'), -1, -1, -1, -1)
                elif board.check_win_whole_board(self.opponent):
                    return (-2_000_000, -1, -1, -1, -1)
                else:
                    return (0, -1, -1, -1, -1)
            if self.heuristic == 1:
                return HeuristicEvaluator.evaluate_board(board, self.symbol, self.opponent), -1, -1, -1, -1
            return HeuristicEvaluator.evaluate_board2(board, self.symbol, self.opponent), -1, -1, -1, -1
        
        def get_nighboors_of_cell(row, col):
            nighboor = set()
            for dx, dy in DIRECTIONS:
                if board.valid_move(row + dx, col + dy):
                    nighboor.add((row + dx, col + dy))
            return nighboor
                    
        best_moves = (-1, -1, -1, -1)  # Best pair of moves: (row1, col1, row2, col2)
        
        # adjacent_cells = set(self.order_moves(board, board.get_adjacent_cells(), is_maximizing))
        adjacent_cells = board.get_adjacent_cells()

        if is_maximizing:
            max_eval = float('-inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.symbol)  # First move
                adjacent_cells = adjacent_cells.union(get_nighboors_of_cell(x1, y1))
                for x2, y2 in adjacent_cells:
                    if (x2, y2) == (x1, y1):
                        continue
                    board.move(x2, y2, self.symbol)  # Second move
                    score = self.minimax(board, depth - 1, False)[0]
                    board.undo_move(x2, y2)  # Undo second move
                    if score > max_eval:
                        max_eval = score
                        best_moves = (x1, y1, x2, y2)
                board.undo_move(x1, y1)  # Undo first move
            return max_eval, best_moves[0], best_moves[1], best_moves[2], best_moves[3]
        else:
            min_eval = float('inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.opponent)  # First move
                adjacent_cells = adjacent_cells.union(get_nighboors_of_cell(x1, y1))
                for x2, y2 in adjacent_cells:
                    if (x2, y2) == (x1, y1):
                        continue
                    board.move(x2, y2, self.opponent)  # Second move
                    score = self.minimax(board, depth - 1, True)[0]
                    board.undo_move(x2, y2)  # Undo second move
                    if score < min_eval:
                        min_eval = score
                        best_moves = (x1, y1, x2, y2)
                board.undo_move(x1, y1)  # Undo first move
            return min_eval, best_moves[0], best_moves[1], best_moves[2], best_moves[3]

    def order_moves(self, board: Board, moves, is_maximizing: bool):
        """
        Orders moves based on a heuristic evaluation of the resulting board state.
        """
        move_scores = []
        for x, y in moves:
            board.move(x, y, self.symbol if is_maximizing else self.opponent)
            # Evaluate the board after making this move
            score = HeuristicEvaluator.evaluate_board(board, self.symbol, self.opponent)
            move_scores.append((score, (x, y)))
            board.undo_move(x, y)  # Undo the move
        
        # Sort moves by score: descending for maximizing, ascending for minimizing
        move_scores.sort(reverse=is_maximizing, key=lambda item: item[0])
        
        # Extract the sorted moves
        return [move for _, move in move_scores]

    # minimax for one move
    def move_one(self, board: Board):
        self.adj_cells = list(board.get_adjacent_cells())
        _, row1, col1 = self.minimax_one_move(board, self.depth, True, float('-inf'), float('inf'))
        board.move(row1, col1, self.symbol)
        self.adj_cells = list(board.get_adjacent_cells())
        _, row2, col2 = self.minimax_one_move(board, self.depth, True, float('-inf'), float('inf'))
        board.move(row2, col2, self.symbol)
        
        return row1, col1, row2, col2
    
    def minimax_one_move(self, board: Board, depth: int, is_maximizing: bool, alpha, beta):
        game_over = board.game_over()
        if depth == 0 or game_over:
            if game_over:
                if board.check_win_whole_board(self.symbol):
                    return (float('inf'), -1, -1)
                elif board.check_win_whole_board(self.opponent):
                    return (-2_000_000, -1, -1)
                else:
                    return (0, -1, -1)
            return HeuristicEvaluator.evaluate_board(board, self.symbol, self.opponent), -1, -1
        
        best_moves = (-1, -1)  # Best pair of moves: (row1, col1)
        adjacent_cells = board.get_adjacent_cells()
        
        if is_maximizing:
            max_eval = float('-inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.symbol)  # First move
                score = self.minimax(board, depth - 1, False, alpha, beta)[0]
                print(score)
                board.undo_move(x1, y1)  # Undo first move
                if score > max_eval:
                    max_eval = score
                    best_moves = (x1, y1)
                alpha = max(alpha, score)
                if self.alpha_beta_pruning(alpha, beta):
                    break
            return max_eval, best_moves[0], best_moves[1]
        else:
            min_eval = float('inf')
            for x1, y1 in adjacent_cells:
                board.move(x1, y1, self.opponent)  # First move
                score = self.minimax(board, depth - 1, True, alpha, beta)[0]
                board.undo_move(x1, y1)  # Undo first move
                if score < min_eval:
                    min_eval = score
                    best_moves = (x1, y1)
                beta = min(beta, score)
                if self.alpha_beta_pruning(alpha, beta):
                    break
            return min_eval, best_moves[0], best_moves[1]
        
    def alpha_beta_pruning(self, alpha, beta):
        # return False
        if beta <= alpha:
            return True
        return False

    # Two moves (NOT Minimax)
    def make_best_move(self, board: Board):
        best_move = (-1, -1, -1, -1)
        max_eval = float('-inf')
        for x, y in board.get_adjacent_cells():
            board.move(x, y, self.symbol) # First move
            for x2, y2 in board.get_adjacent_cells():
                if (x, y) == (x2, y2):
                    continue

                board.move(x2, y2, self.symbol) # Second move
                score = HeuristicEvaluator.evaluate_board(board, self.symbol, self.opponent)
                board.undo_move(x2, y2) # Undo second move
                if score > max_eval:
                    max_eval = score
                    best_move = (x, y, x2, y2)
            board.undo_move(x, y) # Undo first move
            
        if not board.move(best_move[0], best_move[1], self.symbol) or not board.move(best_move[2], best_move[3], self.symbol):
            if not self.move_center(board):
                return self.move_randomly(board)

        return best_move[0], best_move[1], best_move[2], best_move[3]

    def move_center(self, board: Board):
        x, y = int(board.size / 2), int(board.size / 2)
        possible_cells = [[x, y], [x + 1, y], [x - 1, y],
                          [x, y + 1], [x, y - 1], [x + 1, y + 1],
                          [x - 1, y - 1], [x + 1, y - 1], [x - 1, y + 1]]
        cnt = 0
        for a, b in possible_cells:
            if board.move(a, b, self.symbol):
                cnt += 1
            if cnt == 2:
                return True
        return False

    def move_randomly(self, board: Board):
            x, y = int(board.size / 2), int(board.size / 2)
            cnt = 0
            while not board.move(x, y, self.symbol) and cnt < board.size ** 2:
                x, y = random.randint(1, board.size), random.randint(1, board.size)
                cnt += 1
            r1, c2 = x, y
            x, y = int(board.size / 2), int(board.size / 2)
            while not board.move(x, y, self.symbol) and cnt < board.size ** 2:
                x, y = random.randint(1, board.size), random.randint(1, board.size)
                cnt += 1
            return r1, c2, x, y
            
    
        
        