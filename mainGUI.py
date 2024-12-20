"""Connect 6"""
#region Import
import itertools
import sys
import time
import pygame
from pygame.locals import *
import pygame.gfxdraw
from collections import namedtuple

from AIPlayer import AIPlayer
from Board import Board
from Player import Player
from static import EMPTY, WHITE, BLACK
#endregion

#region Init Variables
Point = namedtuple('Point', 'X Y')


B_COLOR = (45, 45, 45)
W_COLOR = (219, 219, 219)

double_clicked = 0

SIZE = 30
Line_Points = 19  # Board size
Outer_Width = 50
Border_Width = 4
Inside_Width = 4
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # Grid line starting point (upper left corner) coordinates
Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
SCREEN_WIDTH = SCREEN_HEIGHT + 200

Stone_Radius = SIZE // 2 - 3
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xE3, 0x92, 0x65)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)
DARK_GRAY = (64, 64, 64)

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10
#endregion

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
    #region Screen Setup
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    global Line_Points
    Line_Points, player_symbol, chosen_heuristic = get_user_preferences(screen)
    alpha_beta = True if (chosen_heuristic.upper() == 'A'  or chosen_heuristic.upper() == 'B') else False
    chosen_heuristic = 1 if (chosen_heuristic.upper() == 'A' or chosen_heuristic.upper() == 'C') else 2
    # Line_Points, player_symbol = 29, WHITE

    global SIZE, Border_Length, SCREEN_HEIGHT, SCREEN_WIDTH, RIGHT_INFO_POS_X, Start_X, Start_Y, Stone_Radius, Stone_Radius2
    
    # Get display info for responsiveness
    display_info = pygame.display.Info()
    max_width, max_height = display_info.current_w, display_info.current_h

    # Dynamically adjust SIZE if the board exceeds the screen size
    max_board_size = min(max_width, max_height) - 200  # Leave some margin for UI
    board_size_pixels = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
    if board_size_pixels > max_board_size:
        SIZE = max_board_size // Line_Points + 6  # Scale down the size
    
    Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
    SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2 + 100
    SCREEN_WIDTH = SCREEN_HEIGHT + 200 + 100
    RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10
    Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # Grid line starting point (upper left corner) coordinates
    Stone_Radius = SIZE // 2 - 3
    Stone_Radius2 = SIZE // 2 + 3
    if Line_Points >= 25:
        Stone_Radius += 4
    
    # Game screen
    screen = pygame.display.set_mode((min(SCREEN_WIDTH, max_width), min(SCREEN_HEIGHT, max_height)), flags=pygame.RESIZABLE)
    pygame.display.set_caption('Connect-6')    
    
    font1 = pygame.font.SysFont('Arial', 32)
    font2 = pygame.font.SysFont('Arial', 72)
    fwidth, fheight = font2.size('32')
    #endregion

    winner = None
    checkerboard = Board(Line_Points)
    player = Player('Human', player_symbol)
    computer = AIPlayer(WHITE if player_symbol == BLACK else BLACK, heu=chosen_heuristic, alpha_beta=alpha_beta, depth=1)
    print(f"Hueristic: {chosen_heuristic}")
    print(f"Alpha-Beta: {alpha_beta}")
    black_win_count = 0
    white_win_count = 0
    user_moves = set()  # To store the two moves of the user (NO DUPLICATES)

    player_first_move(screen, checkerboard, player if player_symbol == BLACK else computer)
    cur_runner = WHITE
    is_draw = False

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        checkerboard.reset_board()
                        player_first_move(screen, checkerboard, player if player_symbol == BLACK else computer)
                        cur_runner = WHITE
            elif cur_runner == computer.symbol: # AI
                s = time.time()
                r, c , r2, c2 = computer.move(checkerboard)
                e = time.time()
                print(e - s)
                print(f'Computer played ({r}, {c})')
                print(f'Computer played ({r2}, {c2})')
                if checkerboard.check_win(r, c, cur_runner) or checkerboard.check_win(r2, c2, cur_runner):
                    winner = computer
                    if computer.symbol == BLACK:
                        black_win_count += 1
                    else:
                        white_win_count += 1
                    break
                else:
                    is_draw = checkerboard.check_draw()
                if winner is None:
                    cur_runner = switch_turn(cur_runner)
            elif cur_runner == player.symbol: # Human
                if event.type == MOUSEBUTTONDOWN:
                    if winner is None:
                        pressed_array = pygame.mouse.get_pressed()
                        if pressed_array[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            click_point = _get_clickpoint(mouse_pos)
                            if click_point is not None:
                                if checkerboard.valid_move(click_point.X, click_point.Y):
                                    # Record the user's move
                                    user_moves.add(click_point)
                                    if len(user_moves) == 2:  # Wait for two moves
                                        for move in user_moves:
                                            checkerboard.move(move.X, move.Y, cur_runner)
                                            print(f'{player.name} played ({move.X}, {move.Y})')
                                            if checkerboard.check_win(move.X, move.Y, cur_runner):
                                                winner = player
                                                if player.symbol == BLACK:
                                                    black_win_count += 1
                                                else:
                                                    white_win_count += 1
                                                break
                                            else:
                                                is_draw = checkerboard.check_draw()
                                        user_moves.clear()
                                        
                                        if winner is None:
                                            cur_runner = switch_turn(cur_runner)
                            else:
                                print('Click a cell!')


        # Update screen board
        _draw_checkerboard(screen)
        for i, row in enumerate(checkerboard.board):
            for j, cell in enumerate(row):
                if cell == BLACK:
                    _draw_chessman(screen, Point(j, i), B_COLOR)
                elif cell == WHITE:
                    _draw_chessman(screen, Point(j, i), W_COLOR)

        _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count)

        # Check win or draw
        if is_draw:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, 'Draw', RED_COLOR)
            cur_runner = EMPTY
            winner = EMPTY
            is_draw = False
        elif winner:
            if winner == EMPTY:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, 'Draw', RED_COLOR)
            else:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, f'{winner.name} Wins', RED_COLOR)
            cur_runner = EMPTY

        pygame.display.flip()


# Get user preferences about the game (Size & Stone Colour)
def get_user_preferences(screen):
    font = pygame.font.SysFont('Arial', 36)
    input_box = pygame.Rect(300, 200, 140, 50)
    color_inactive = pygame.Color('gray')
    color_active = pygame.Color('black')
    color = color_inactive
    active = False
    text = ''
    board_size = None
    player_color = None
    chosen_heuristic = None
    

    # Get Board Size
    while board_size is None:
        screen.fill(Checkerboard_Color)  # Background color

        # Display instructions
        text_surface = font.render("Enter board size (ODD Number -> 9 : 59):", True, (0, 0, 0))
        screen.blit(text_surface, (150, 150))
        pygame.draw.rect(screen, color, input_box, 2)

        # Render the current text
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user clicked on the input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            board_size = int(text)
                            if board_size < 9 or board_size > 59 or board_size % 2 == 0:
                                raise ValueError("Board size must be ODD number between 9 AND 59.")
                            break  # Exit the size input loop
                        except ValueError:
                            text = ''  # Reset input for invalid values
                            board_size = None
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
    
    clock = pygame.time.Clock()
    button_black = Button(300, 200, 150, 50, "Black", BLACK_COLOR, (0, 128, 255), WHITE_COLOR)
    button_white = Button(300, 300, 150, 50, "White", WHITE_COLOR, (0, 128, 255), BLACK_COLOR)
    
    # Get Player's Color
    while player_color not in [BLACK, WHITE]:
        screen.fill(Checkerboard_Color)
        
        button_black.draw(screen)
        button_white.draw(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button_white.is_clicked(event):
                player_color = WHITE
            elif button_black.is_clicked(event):
                player_color = BLACK

    # Buttons
    button_a = Button(300, 200, 400, 50, "Heuristic 1 WITH Alpha-Beta (A)", (0, 128, 255), (255, 255, 255))
    button_b = Button(300, 300, 400, 50, "Heuristic 2 WITH Alpha-Beta (B)", (0, 128, 255), (255, 255, 255))
    button_c = Button(300, 400, 500, 50, "Heuristic 1 WITHOUT Alpha-Beta (C)", (0, 128, 255), (255, 255, 255))
    button_d = Button(300, 500, 500, 50, "Heuristic 2 WITHOUT Alpha-Beta (D)", (0, 128, 255), (255, 255, 255))

    # Get Player's Heuristic
    while chosen_heuristic not in ["A", "B", "C", "D"]:
        screen.fill(Checkerboard_Color)

        button_a.draw(screen)
        button_b.draw(screen)
        button_c.draw(screen)
        button_d.draw(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
            # Check button clicks
            if button_a.is_clicked(event):
                chosen_heuristic = "A"
            elif button_b.is_clicked(event):
                chosen_heuristic = "B"
            elif button_c.is_clicked(event):
                chosen_heuristic = "C"
            elif button_d.is_clicked(event):
                chosen_heuristic = "D"

        clock.tick(60)
                
    return board_size, player_color, chosen_heuristic


# Get the first move (Place one stone at first of the game)
def player_first_move(screen, checkerboard: Board, player):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif isinstance(player, AIPlayer):
                # player.move(checkerboard)
                checkerboard.move(int(checkerboard.size/2), int(checkerboard.size/2), player.symbol)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    click_point = _get_clickpoint(mouse_pos)
                    if click_point is not None:
                        if checkerboard.valid_move(click_point.X, click_point.Y):
                            checkerboard.move(click_point.X, click_point.Y, player.symbol)
                            return
                    else:
                        print('Click a cell!')

        # Draw the board and existing stones
        _draw_checkerboard(screen)
        for i, row in enumerate(checkerboard.board):
            for j, cell in enumerate(row):
                if cell == BLACK:
                    _draw_chessman(screen, Point(j, i), B_COLOR)
                elif cell == WHITE:
                    _draw_chessman(screen, Point(j, i), W_COLOR)
                    
        pygame.display.flip()


# Switching turns
def switch_turn(current_player):
    return WHITE if current_player == BLACK else BLACK


# Display board
def _draw_checkerboard(screen):
    screen.fill(Checkerboard_Color)

    # Draw a border outside the chessboard grid lines
    pygame.draw.rect(screen, DARK_GRAY, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)

    # Draw grid lines
    for i in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_Y, Start_Y + SIZE * i),
                         (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                         1)
    for j in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_X + SIZE * j, Start_X),
                         (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                         1)

    # Dynamically calculate star and celestial element positions
    # Place stars at approximately 1/6 and 5/6 positions of the board
    star_positions = [Line_Points // 6, Line_Points // 2, (5 * Line_Points) // 6]
    for i in star_positions:
        for j in star_positions:
            # Set a larger radius for the center star
            radius = 5 if i == Line_Points // 2 and j == Line_Points // 2 else 3

            # Draw anti-aliased filled circles for stars
            pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, DARK_GRAY)
            pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, DARK_GRAY)


# Draw chess pieces
def _draw_chessman(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
    pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)


# Information display on the left side of the picture
def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2), B_COLOR)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4), W_COLOR)

    print_text(screen, font, RIGHT_INFO_POS_X, Start_X + 3, 'Player', BLUE_COLOR)
    print_text(screen, font, RIGHT_INFO_POS_X, Start_X + Stone_Radius2 * 3 + 3, 'Computer', BLUE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT, SCREEN_HEIGHT - Stone_Radius2 * 8, 'State: ', BLUE_COLOR)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)), B_COLOR)
    _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2), W_COLOR)
    print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(Stone_Radius2 * 5.5) + 3, f'{black_win_count} wins', BLUE_COLOR)
    print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - Stone_Radius2 * 3 + 3, f'{white_win_count} wins', BLUE_COLOR)


def _draw_chessman_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)


# Return the coordinates of the game area based on the mouse click position
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    if pos_x < -Inside_Width or pos_y < -Inside_Width:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > Stone_Radius:
        x += 1
    if pos_y % SIZE > Stone_Radius:
        y += 1
    if x >= Line_Points or y >= Line_Points:
        return None

    return Point(y, x)


class Button:
    def __init__(self, x, y, width, height, text, color=DARK_GRAY, hover_color=DARK_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Render and center text
        text_surface = pygame.font.SysFont('Arial', 32).render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            return self.rect.collidepoint(event.pos)
        return False


if __name__ == '__main__':
    main()
