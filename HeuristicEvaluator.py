from Board import Board
from static import EMPTY, WINNING_LENGTH


class HeuristicEvaluator:
    @staticmethod
    def evaluate_board(board: Board, symbol, opponent_symbol):
        score = 0

        # Evaluate rows and columns
        for line in range(board.size):
            score += HeuristicEvaluator.evaluate_line(board.get_row(line), symbol, opponent_symbol)
            score += HeuristicEvaluator.evaluate_line(board.get_column(line), symbol, opponent_symbol)

        # Evaluate diagonals
        for diagonal in board.get_diagonals():
            score += HeuristicEvaluator.evaluate_line(diagonal, symbol, opponent_symbol)

        return score

    @staticmethod
    def evaluate_line(line: list[int], symbol, opponent_symbol):
        score = 0

        empty_count = line.count(EMPTY)
        line_length = len(line)
        if line_length < 6: return score

        track_start = 0
        track_end = 0
        for i in range(line_length):
            if line[i] == symbol:
                track_start = i
                counter = 1
                for j in range(i + 1, line_length):
                    if line[j] == symbol:
                        counter += 1
                        track_end = j
                    else:
                        break
                if counter == 6:
                    return float('inf')
                elif counter == 5:
                    if ((track_start - 1 >= 0 and line[track_start - 1] == EMPTY)
                        or (track_end + 1 < line_length and line[track_end + 1] == EMPTY)
                        ):
                        score += 3000
                    else:
                        score += 2000
                elif counter == 4:
                    if ((track_start - 2 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == EMPTY)
                        or (track_end + 2 < line_length and line[track_end + 1] == EMPTY and line[track_end + 2] == EMPTY)
                        or (track_end - 2 >= 0 and line[track_end - 1] == EMPTY and line[track_end - 2] == EMPTY)
                        or (track_start + 2 < line_length and line[track_start + 1] == EMPTY and line[track_start + 2] == EMPTY)
                        # or (track_start + 1 < line_length and line[track_start + 1] == EMPTY and track_end - 1 >= 0 and line[track_end - 1] == EMPTY)
                        or (track_end + 1 < line_length and line[track_end + 1] == EMPTY and track_start - 1 >= 0 and line[track_start - 1] == EMPTY)
                        ):
                        score += 2500
                    else:
                        score += 1500
                elif counter == 3 and empty_count >= 3:
                    score += 1000
                elif counter == 2 and empty_count >= 4:
                    score += 450
                else:
                    score += 250

        track_start = 0
        track_end = 0
        for i in range(line_length):
            if line[i] == opponent_symbol:
                track_start = i
                counter = 1
                for j in range(i + 1, line_length):
                    if line[j] == opponent_symbol:
                        counter += 1
                        track_end = j
                    else:
                        break
                if counter == 6:
                    return -2_000_000
                elif counter == 5:
                    if ((track_start - 1 >= 0 and line[track_start - 1] == EMPTY)
                        or (track_end + 1 < line_length and line[track_end + 1] == EMPTY)
                        ):
                        score -= 1_000_005 # loss
                    else:
                        score -= 2000
                elif counter == 4:
                    if ((track_end + 1 < line_length and line[track_end + 1] == EMPTY and track_start - 1 >= 0 and line[track_start - 1] == EMPTY)
                        or (track_start - 2 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] != symbol)
                        or (track_end + 2 < line_length and line[track_end + 1] == EMPTY and line[track_end + 2] != symbol)
                        ):
                        score -= 1_000_004 # loss
                    else:
                        score -= 1000
                elif counter == 3:
                    if ((track_start - 3 >= 0 and line[track_start - 1] == EMPTY
                            and line[track_start - 2] == opponent_symbol and line[track_start - 3] != symbol)
                        or (track_end + 3 < line_length and line[track_end + 1] == EMPTY
                            and line[track_end + 2] == opponent_symbol and line[track_end + 3] != symbol)
                        or (track_start - 2 >= 0 and line[track_start - 1] == EMPTY
                            and line[track_start - 2] == opponent_symbol and track_end + 1 < line_length and line[track_end + 1] != symbol)
                        or (track_end + 2 < line_length and line[track_end + 1] == EMPTY
                            and line[track_end + 2] == opponent_symbol and track_start - 1 >= 0 and line[track_start - 1] != symbol)
                        or (track_start - 3 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == EMPTY and line[track_start - 3] == opponent_symbol)
                        or (track_end + 3 < line_length and line[track_end + 1] == EMPTY and line[track_end + 2] == EMPTY and line[track_end + 3] == opponent_symbol)
                        ):
                        score -= 1_000_003 # loss
                    else:
                        score -= 750
                elif counter == 2:
                    if ((track_start - 4 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == opponent_symbol
                            and ((line[track_start - 3] == opponent_symbol and line[track_start - 4] != symbol) or (line[track_start - 3] != symbol and line[track_start - 4] == opponent_symbol)))
                        or (track_end + 4 < line_length and line[track_end + 1] == EMPTY and line[track_start + 2] == opponent_symbol
                            and ((line[track_start + 3] == opponent_symbol and line[track_end + 4] != symbol) or (line[track_start + 3] != symbol  and line[track_end + 4] == opponent_symbol)))
                        or (track_start - 3 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == opponent_symbol
                            and line[track_start - 3] == opponent_symbol and track_end + 1 > line_length and line[track_end + 1] != symbol)
                        or (track_end + 3 < line_length and line[track_end + 1] == EMPTY and line[track_start + 2] == opponent_symbol
                            and line[track_start + 3] == opponent_symbol and track_start - 1 >= 0 and line[track_start - 1] != symbol)
                        or (track_start - 4 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == EMPTY
                            and line[track_start - 3] == opponent_symbol and line[track_start - 4] == opponent_symbol)
                        or (track_end + 4 < line_length and line[track_end + 1] == EMPTY and line[track_end + 2] == EMPTY
                            and line[track_end + 3] == opponent_symbol and line[track_end + 4] == opponent_symbol)
                        or (track_start - 2 >= 0 and line[track_start - 1] == EMPTY and line[track_start - 2] == opponent_symbol
                            and track_end + 2 < line_length and line[track_end + 1] == EMPTY and line[track_end + 2] == opponent_symbol)
                        ):
                        score -= 1_000_002 # loss
                    else:
                        score -= 400
                else:
                    score -= 200
        return score
    
    @staticmethod
    def evaluate_board2(board: Board, player, opponent):
        """
        A heuristic evaluation function for the board.
        Considers winning moves, blocking opponent, and positional advantage.
        """
        
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        def count_consecutive(row, col, dr, dc, target):
            """Counts consecutive pieces and returns the count."""
            count = 0
            open_ends = 0

            # Count in the forward direction
            for step in range(6):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    if board.board[r][c] == target:
                        count += 1
                    elif board.board[r][c] == EMPTY:
                        open_ends += 1
                        break
                    else:
                        break
                    
            return count, open_ends

        # Assign positional weight (favoring center positions)
        def positional_weight(row, col):
            """Returns weight based on proximity to the center."""
            center = board.size // 2
            return (center - abs(center - row)) + (center - abs(center - col))

        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] != EMPTY:
                    current_player = board.board[row][col]
                    for dr, dc in directions:
                        count, open_ends = count_consecutive(row, col, dr, dc, current_player)

                        # Assign scores based on patterns
                        if count >= 6:
                            if current_player == player:
                                return float('inf')  # Immediate win
                            else:
                                return -100_000  # Immediate loss
                        elif count == 5:
                            if current_player == player:
                                score += 10_000 * open_ends
                            else:
                                score -= 100_000 * open_ends
                        elif count == 4:
                            if current_player == player:
                                score += 5000 * open_ends
                            else:
                                score -= 10_000 * open_ends
                        elif count == 3:
                            if current_player == player:
                                score += 100 * open_ends
                            else:
                                score -= 100 * open_ends
                        elif count == 2:
                            if current_player == player:
                                score += 10 * open_ends
                            else:
                                score -= 10 * open_ends

                # Add positional weight for the current cell
                if board.board[row][col] == player:
                    score += positional_weight(row, col)
                elif board.board[row][col] == opponent:
                    score -= positional_weight(row, col)

        return score

    