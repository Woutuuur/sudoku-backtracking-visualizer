import math
import pygame
import time
import sys
import config


def is_safe(board, y, x, val):
    for i in range(9):
        if (board[i][x] == val or board[y][i] == val):
            return False
    x = x - x % 3
    y = y - y % 3
    for i in range(3):
        for j in range (3):
            if (board[y + i][x + j] == val):
                return False
    return True

def empty_spot_exists(board, spot):
    for i in range(9):
        for j in range (9):
            if(board[i][j] == 0):
                spot[0] = i
                spot[1] = j
                return True
    return False

def solve(board):
    global backtrack_count

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
    if (config.visualize == True):
        draw_board(board, [-1,-1]);

    spot = [0,0]
    if (not empty_spot_exists(board, spot)):
        return True
    
    y = spot[0]
    x = spot[1]

    if (config.visualize == True):
        win.fill(white)
        draw_board(board, spot)
        pygame.time.delay(config.delay)
        pygame.display.update()
    for val in range(1, 10):
        if (is_safe(board, y, x, val)):
    
            board[y][x] = val

            if (solve(board)):
                return True

            board[y][x] = 0

    backtrack_count += 1
    return False

def readBoard(str):
    rows = [[0 for i in range(9)] for j in range(9)] 
    for i in range (len(str)):
        y = int(math.floor(i / 9))
        x = i % 9
        rows[y][x] = int(str[i].replace('.', '0').replace(' ', '0'))
    return rows

inp = input("Input a board: ")
board = readBoard(inp)
pygame.init()
w = config.width
h = config.height
white = (255,255,255)
red = (255, 0, 0)
black = (0,0,0)
light_gray = (220,220,220)
gray = (100,100,100)
win = pygame.display.set_mode((w,h + int(h / 9)))
pygame.display.set_caption("Sudoku solver")
font = pygame.font.SysFont('freesansbold.ttf', int(1.0/3.0 * min(w, h) / 9 * config.font_multiplier)); 
#font = pygame.font.Font(pygame.font.get_default_font(), int(1.0/3.0 * min(w, h) / 9 * config.font_multiplier))

backtrack_count = 0

def draw_info():
    info = font.render("Number of backtracks: " + str(backtrack_count), True, black, white)
    infoRect = info.get_rect()
    infoRect.center = (int(w / 2), int(h + h / 9 / 2))
    win.blit(info, infoRect)

def draw_board(board, spot):
    for i in range(9):
        for j in range (9):
            value = str(board[i][j]).replace('0', ' ')
            text = font.render(value, True, black, white)
            textRect = text.get_rect()
            textRect.center = (int(w / 9 * j + w / 9 / 2), int(h / 9 * i + h / 9 / 2))
            if ((i == spot[0] or j == spot[1]) and spot[0] != -1 and config.enable_hightlight):
                text = font.render(value, True, black, light_gray)
                pygame.draw.rect(win, light_gray, [int(w / 9 * j), int(h / 9 * i), int(w / 9), int(h / 9)])
            if (i == spot[0] and j == spot[1] and spot[0] != -1):
                    pygame.draw.rect(win, red, [int(w / 9 * j), int(h / 9 * i), int(w / 9), int(h / 9)], config.hightlight_border_size)
            else:
                 pygame.draw.rect(win, black, [int(w / 9 * j), int(h / 9 * i), int(w / 9), int(h / 9)], 1)
            win.blit(text, textRect)
    for i in range (1, 3):
        pygame.draw.line(win, black, [0, int(h / 3 * i)], [w, int(h / 3 * i)], 4)
        pygame.draw.line(win, black, [int(w / 3 * i), 0], [int(w / 3 * i), h], 4)
    draw_info()

while True:
    win.fill(white)
    draw_board(board, [-1,-1])
    pygame.display.update()
    solve(board)
    pygame.display.update() 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)