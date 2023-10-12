import pygame
import numpy as np
import math
import sys

# Define colors
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Set board dimensions
rowCount = 6
columnCount = 7

# Create an empty game board
def create_board():
    board = np.zeros((rowCount, columnCount))
    return board

# Place a piece on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a column is a valid location to place a piece
def is_valid_location(board, col):
    return board[rowCount - 1][col] == 0

# Find the next available row in a column
def get_next_open_row(board, col):
    for r in range(rowCount):
        if board[r][col] == 0:
            return r

# Display the game board
def print_board(board):
    print(np.flip(board, 0))

# Check if a player has won
def winning_move(board, piece):
    # Check horizontal locations for a winning patern
    for c in range(columnCount - 3):
        for r in range(columnCount):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for a wining patern
    for c in range(columnCount):
        for r in range(rowCount - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(columnCount - 3):
        for r in range(rowCount - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(columnCount - 3):
        for r in range(3, rowCount):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

# Initialize pygame
pygame.init()

# Define square size
squareSize = 100

#Define screen dimensions
width = columnCount * squareSize
height = (rowCount + 1) * squareSize
size = (width, height)

#Define screen radius
radius = int(squareSize / 2 - 5)

# Create the game screen
screen = pygame.display.set_mode(size)

# Initialize the game board
board = create_board()

# Set up the game font
myfont = pygame.font.SysFont("arial", 60)

# Game loop
game_over = False
turn = 0

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Draw the current player's piece when hovering over a column
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(squareSize / 2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (posx, int(squareSize / 2)), radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            posx = event.pos[0]
            col = int(math.floor(posx / squareSize))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1 if turn == 0 else 2)

                if winning_move(board, 1 if turn == 0 else 2):
                    winner = "Player 1 wins!!" if turn == 0 else "Player 2 wins!!"
                    label = myfont.render(winner, 1, red if turn == 0 else yellow)
                    screen.blit(label, (30, 10))
                    game_over = True

                print_board(board)
                # Draw the updated board
                for c in range(columnCount):
                    for r in range(rowCount):
                        pygame.draw.rect(screen, blue, (c * squareSize, r * squareSize + squareSize, squareSize, squareSize))
                        if board[r][c] == 1:
                            pygame.draw.circle(screen, red, (int(c * squareSize + squareSize / 2), int(r * squareSize + squareSize + squareSize / 2)), radius)
                        elif board[r][c] == 2:
                            pygame.draw.circle(screen, yellow, (int(c * squareSize + squareSize / 2), int(r * squareSize + squareSize + squareSize / 2)), radius)
                pygame.display.update()

                turn += 1
                turn %= 2

                if game_over:
                    pygame.time.wait(5000)
