import numpy as np
import random
import pygame
import sys
import math
# Board dimensions
rows = 7  # Customize the number of rows
columns = 7  # Customize the number of columns

# Colors
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Constants for player and AI
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

# Connect-4 specifics
WINDOW_LENGTH = 4
EMPTY = 0

# Function to print the game board
def print_board(board):
    print(np.flip(board, 0))

# Function to create an empty game board
def create_board():
    board = np.zeros((rows, columns))
    return board

# Function to drop a piece into a column
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column is a valid location for a piece
def is_valid_location(board, col):
    return board[rows - 1][col] == 0

# Function to find the next open row in a column
def get_next_open_row(board, col):
    for r in range(rows + 1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(columns - 3):
        for r in range(rows):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(columns):
        for r in range(rows - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(columns - 3):
        for r in range(rows - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(columns - 3):
        for r in range(3, rows):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE

    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    # AI's pieces
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 1:
        score += 3

    # Player's pieces
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score


def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )


def score_position(board, piece):
    score = 0
    # center pieces
    center_array = [int(i) for i in list(board[:, columns // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # hori scores

    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(columns - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # verti scores
    for c in range(columns):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # pos slope scores
    for r in range(rows - 3):
        for c in range(columns - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]

            score += evaluate_window(window, piece)

    # neg slope scores
    for r in range(rows - 3):
        for c in range(columns - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]

            score += evaluate_window(window, piece)

    return score


# 34;34
# Minimax algorithm for determining the optimal move for the AI player
def minimax(board, depth, maximizingPlayer):
    # Get the valid locations where the AI can make a move
    valid_locations = get_valid_locations(board)
    # Check if the current state is a terminal node (end of the game or depth reached)
    is_terminal = is_terminal_node(board)

    # Base case: If depth is 0 or the game is over, return the score for the current position
    if depth == 0 or is_terminal:
        if is_terminal:
            # If the AI wins, return a high positive score
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000000000)
            # If the player wins, return a high negative score
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000000000000)
            # If it's a tie, return a neutral score
            else:
                return (None, 0)
        else:  # Depth 0
            # Evaluate the score for the current position and return it
            return (None, score_position(board, AI_PIECE))

    # If the current move is for the AI player (maximizing player)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)

        # Iterate through each valid move
        for col in valid_locations:
            # Find the next open row in the column
            row = get_next_open_row(board, col)
            # Create a copy of the board to simulate the move
            b_copy = board.copy()
            # Drop the AI piece in the selected column
            drop_piece(b_copy, row, col, AI_PIECE)

            # Recursively call minimax for the opponent's turn (minimizing player)
            new_score = minimax(b_copy, depth - 1, False)[1]

            # Update the best move and its value if the new score is greater
            if new_score > value:
                column = col
            return column, value
        
    else:  # If the current move is for the player (minimizing player)
        value = math.inf
        column = random.choice(valid_locations)

        # Iterate through each valid move
        for col in valid_locations:
            # Find the next open row in the column
            row = get_next_open_row(board, col)
            # Create a copy of the board to simulate the move
            b_copy = board.copy()
            # Drop the player's piece in the selected column
            drop_piece(b_copy, row, col, PLAYER_PIECE)

            # Recursively call minimax for the AI's turn (maximizing player)
            new_score = minimax(b_copy, depth - 1, True)[1]

            # Update the best move and its value if the new score is smaller
            if new_score < value:
                value = new_score
                column = col
            return column, value


# Function to get valid locations for the next move
def get_valid_locations(board):
    valid_location = []
    # Iterate through each column
    for col in range(columns):
        # Check if the location in the column is a valid move
        if is_valid_location(board, col):
            # Add the valid column to the list of valid locations
            valid_location.append(col)
    return valid_location


# Function to pick the best score and corresponding column for the AI player
def pick_best_score(board, piece):
    # Get the valid locations for the AI's next move
    valid_location = get_valid_locations(board)
    # Initialize the best score to a very low value
    best_score = -10000
    # Choose a random column from the valid locations initially
    best_col = random.choice(valid_location)

    # Iterate through each valid column
    for col in valid_location:
        # Find the next open row in the column
        row = get_next_open_row(board, col)
        # Create a copy of the board to simulate the move
        temp_board = board.copy()
        # Drop the AI piece in the selected column
        drop_piece(temp_board, row, col, piece)

        # Calculate the score for the current position
        score = score_position(temp_board, piece)
        # Update the best score and corresponding column if the current score is higher
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

# Function to draw the game board on the Pygame window
def draw_board(board):
    # Iterate through each column
    for c in range(columns):
        # Iterate through each row
        for r in range(rows):
            # Draw a blue rectangle for each grid cell
            pygame.draw.rect(
                screen,
                blue,
                (c * squaresize, r * squaresize + squaresize, squaresize, squaresize),
            )
            # Draw a black circle at the center of each grid cell
            pygame.draw.circle(
                screen,
                black,
                (
                    int(c * squaresize + squaresize / 2),
                    int(r * squaresize + squaresize + squaresize / 2),
                ),
                radius,
            )

    # Iterate through each column
    for c in range(columns):
        # Iterate through each row
        for r in range(rows):
            # If the current cell has a player's piece, draw a red circle
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    red,
                    (
                        int(c * squaresize + squaresize / 2),
                        height - int(r * squaresize + squaresize / 2),
                    ),
                    radius,
                )
            # If the current cell has an AI's piece, draw a yellow circle
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    yellow,
                    (
                        int(c * squaresize + squaresize / 2),
                        height - int(r * squaresize + squaresize / 2),
                    ),
                    radius,
                )
            # Update the Pygame display to show the changes
            pygame.display.update()

# calls the function and creates the board connecting it to the varialbe board
# Initialize the game board and display settings
board = create_board()
print_board(board)

game_over = False
turn = 0

# Initialize Pygame
pygame.init()
squaresize = 100
width = columns * squaresize
height = rows * squaresize

size = (width, height)

radius = int(squaresize / 2 - 5)

# Set up the Pygame window
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

# Randomly choose the starting player (either PLAYER or AI)
turn = random.randint(PLAYER, AI)

# Main game loop
while not game_over:
    # Event handling loop
    for event in pygame.event.get():
        # Quit the game if the window is closed
        if event.type == pygame.QUIT:
            sys.exit()

        # Update the display when the mouse moves
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            # Draw a red circle at the mouse position if it's the player's turn
            if turn == PLAYER:
                pygame.draw.circle(screen, red, (posx, int(squaresize / 2)), radius)
        
        pygame.display.update()

        # Drop a piece when the mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))

                # Check if the selected column is a valid move
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    # Drop the player's piece in the selected column
                    drop_piece(board, row, col, PLAYER_PIECE)

                    # Check if the player has won
                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!", 1, red)
                        screen.blit(label, (40, 10))
                        game_over = True

                    # Switch turns
                    turn += 1
                    turn = turn % 2

                    # Update the display
                    draw_board(board)

    # AI's turn
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 10, True)

        if is_valid_location(board, col):
            # Pause for a short duration to visualize the AI's move
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            # Drop the AI's piece in the selected column
            drop_piece(board, row, col, AI_PIECE)

            # Check if the AI has won
            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!", 1, yellow)
                screen.blit(label, (40, 10))
                game_over = True
            
            print_board(board)
            draw_board(board)
            # Switch turns
            turn += 1
            turn = turn % 2

    # Display the game outcome for a brief moment before exiting
    if game_over:
        pygame.time.wait(3000)
        # print(turn)
