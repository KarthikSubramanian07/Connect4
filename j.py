import numpy as np
import pygame
import sys
import math

rows = 6  # to customize your own game,
colums = 7  # ''
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)


def create_baord():  # funcion to create the board
    board = np.zeros((rows, colums))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows-1][col] == 0


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def winning_moce(board, piece):
    # check hori
    for c in range(colums-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check verti
    for c in range(colums):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # positive slopes
    for c in range(colums-3):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c+1] and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # negatibe slopes
    for c in range(colums-3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r-1][c+1] and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(colums):
        for r in range(rows):
            pygame.draw.rect(screen, blue, (c*sqauresize, r *
                             sqauresize+sqauresize, sqauresize, sqauresize))
            pygame.draw.circle(screen, black, (int(c*sqauresize+sqauresize/2),
                                               int(r*sqauresize+sqauresize+sqauresize/2)), radius)
    for c in range(colums):
        for r in range(rows):
            if board[r][c] == 1:
                pygame.draw.circle(screen, red, (int(c*sqauresize+sqauresize/2),
                                                 height - int(r*sqauresize+sqauresize/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, yellow, (int(c*sqauresize+sqauresize/2),
                                                    height - int(r*sqauresize+sqauresize/2)), radius)
            pygame.display.update()


# calls the function and creates the board connecting it to the varialbe board
board = create_baord()

game_over = False
turn = 0

pygame.init()
sqauresize = 100
width = colums * sqauresize
height = rows * sqauresize

size = (width, height)

radius = int(sqauresize/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, sqauresize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(
                    sqauresize/2)), radius)
            if turn == 1:
                pygame.draw.circle(screen, yellow, (posx, int(
                    sqauresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, sqauresize))
            # print(event.pos)
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/sqauresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_moce(board, 1):
                        label = myfont.render("Player 1 wins!", 1, red)
                        screen.blit(label, (40, 10))
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/sqauresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_moce(board, 2):
                        label = myfont.render("Player 2 wins!", 1, yellow)
                        screen.blit(label, (40, 10))
                        game_over = True

            draw_board(board)
            turn += 1
            turn = turn % 2
            if game_over:
                pygame.time.wait(3000)
        # print(turn)
