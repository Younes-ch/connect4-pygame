import numpy as np
import pygame
import sys
import math



class Connect4:
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)

    ROW_COUNT = 6
    COLUMN_COUNT = 7

    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE/2 - 5)
    screen = pygame.display.set_mode(size)

    def __init__(self):
        self.board = Board()
        self.player1 = Player(1, self.RED)
        self.player2 = Player(2, self.YELLOW)
        self.game_over = False
        self.turn = 0
        pygame.init()
        self.board.draw()
        pygame.display.update()
        self.myfont = pygame.font.SysFont("monospace", 75)

    def play(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(Connect4.screen, Connect4.BLACK, (0,0, Connect4.width, Connect4.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(Connect4.screen, Connect4.RED, (posx, int(Connect4.SQUARESIZE/2)), Connect4.RADIUS)
                    else: 
                        pygame.draw.circle(Connect4.screen, Connect4.YELLOW, (posx, int(Connect4.SQUARESIZE/2)), Connect4.RADIUS)
                pygame.display.update()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(Connect4.screen, Connect4.BLACK, (0,0, Connect4.width, Connect4.SQUARESIZE))

                    # Ask for Player 1 Input
                    if self.turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/Connect4.SQUARESIZE))

                        if self.board.is_valid_location(col):
                            row = self.board.get_next_open_row(col)
                            self.board.drop_piece(row, col, 1)

                            if self.board.winning_move(1):
                                label = self.myfont.render("Player 1 wins!!", 1, Connect4.RED)
                                Connect4.screen.blit(label, (40,10))
                                self.game_over = True
                    
                    # Ask for Player 2 Input
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/Connect4.SQUARESIZE))

                        if self.board.is_valid_location(col):
                            row = self.board.get_next_open_row(col)
                            self.board.drop_piece(row, col, 2)

                            if self.board.winning_move(2):
                                label = self.myfont.render("Player 2 wins!!", 1, Connect4.YELLOW)
                                Connect4.screen.blit(label, (40,10))
                                self.game_over = True
                    
                    self.board.print_board()
                    self.board.draw()
                    self.turn += 1
                    self.turn = self.turn % 2

                    if self.game_over:
                        pygame.time.wait(3000)

class Board:
    def __init__(self):
        self.board = np.zeros((Connect4.ROW_COUNT, Connect4.COLUMN_COUNT))

    def create_board(self):
        return np.zeros((Connect4.ROW_COUNT, Connect4.COLUMN_COUNT))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[Connect4.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(Connect4.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(Connect4.COLUMN_COUNT-3):
            for r in range(Connect4.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(Connect4.COLUMN_COUNT):
            for r in range(Connect4.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
        # Check positively sloped diaganols
        for c in range(Connect4.COLUMN_COUNT-3):
            for r in range(Connect4.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(Connect4.COLUMN_COUNT-3):
            for r in range(3, Connect4.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
    
    def draw(self):
        for c in range(Connect4.COLUMN_COUNT):
            for r in range(Connect4.ROW_COUNT):
                pygame.draw.rect(Connect4.screen, Connect4.BLUE, (c*Connect4.SQUARESIZE, r*Connect4.SQUARESIZE+Connect4.SQUARESIZE, Connect4.SQUARESIZE, Connect4.SQUARESIZE))
                pygame.draw.circle(Connect4.screen, Connect4.BLACK, (int(c*Connect4.SQUARESIZE+Connect4.SQUARESIZE/2), int(r*Connect4.SQUARESIZE+Connect4.SQUARESIZE+Connect4.SQUARESIZE/2)), Connect4.RADIUS)

        for c in range(Connect4.COLUMN_COUNT):
            for r in range(Connect4.ROW_COUNT):    
                if self.board[r][c] == 1:
                    pygame.draw.circle(Connect4.screen, Connect4.RED, (int(c*Connect4.SQUARESIZE+Connect4.SQUARESIZE/2), Connect4.height-int(r*Connect4.SQUARESIZE+Connect4.SQUARESIZE/2)), Connect4.RADIUS)
                elif self.board[r][c] == 2: 
                    pygame.draw.circle(Connect4.screen, Connect4.YELLOW, (int(c*Connect4.SQUARESIZE+Connect4.SQUARESIZE/2), Connect4.height-int(r*Connect4.SQUARESIZE+Connect4.SQUARESIZE/2)), Connect4.RADIUS)
        pygame.display.update()

class Player:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color

    def get_move(self):
        # Get player's move (replace with appropriate code)
        move = int(input(f'Player {self.piece}, enter a column: '))
        while not self.is_valid_move(move):
            move = int(input('Invalid move, enter a valid column: '))
        return move

    def is_valid_move(self, move):
        return move >= 0 and move < Connect4.COLUMN_COUNT and game.board.is_valid_location(move)

# Create game instance and start game
game = Connect4()
game.play()
