import numpy as np
import math
import sys
import pygame

class ConnectFour(object):
    
    def __init__(self):
        self.game_over = False
        self.square_size = 100
        self.radius = self.square_size/2-5
        self.row_count = 6
        self.col_count = 7
        self.width = self.square_size * self.col_count
        self.height = self.square_size * (self.row_count + 1)
        self.turn = 0
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)
        self.board = np.zeros((self.row_count, self.col_count))
        self.posx = 0 # the position of the dropping piece (moving along mouse)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.myfont = pygame.font.SysFont('monospace', 75)


    def Draw(self):
        for c in range(self.col_count):
            for r in range(self.row_count):
                pygame.draw.rect(self.screen, self.blue, (c*self.square_size, r*self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, self.black, (c*self.square_size + self.square_size/2, r*self.square_size + self.square_size + self.square_size/2), self.radius)
    
        for c in range(self.col_count):
            for r in range(self.row_count):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.red, (c*self.square_size + self.square_size/2, self.height-(r*self.square_size + self.square_size/2)), self.radius)
                if self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.yellow, (c*self.square_size + self.square_size/2, self.height-(r*self.square_size + self.square_size/2)), self.radius)
        pygame.display.update()
    
    def Input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.square_size))
                self.posx = event.pos[0]
                if self.turn == 0:
                    pygame.draw.circle(self.screen, self.red, (self.posx, self.square_size/2), self.radius)
                else:
                    pygame.draw.circle(self.screen, self.yellow, (self.posx, self.square_size/2), self.radius)
            pygame.display.update()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, self.black, (0, 0, self.width, self.square_size))
                self.posx = event.pos[0]
                col = math.floor(self.posx/self.square_size)
                if self.is_valid_col(col):
                    row = self.get_next_open_row(col)
                    if self.turn == 0:
                        self.drop_piece(row, col, 1)
                        if self.is_winning(1):
                            label = self.myfont.render("Player 1 Wins", 1, self.red)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                    else:
                        self.drop_piece(row, col, 2)
                        if self.is_winning(2):
                            label = self.myfont.render("Player 2 Wins", 1, self.yellow)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                    self.Draw()
                    self.turn = (self.turn + 1) % 2
            
            if self.game_over:
                pygame.time.wait(20)
                
    def is_valid_col(self, col):
            return self.board[self.row_count-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.row_count):
            if self.board[r][col] == 0: return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        
    def is_winning(self, piece):
        for r in range(self.row_count - 3):
            for c in range(self.col_count):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
        for r in range(self.row_count):
            for c in range(self.col_count - 3):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
        for r in range (self.row_count - 3):
            for c in range(self.col_count - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
        for r in range(3, self.row_count):
            for c in range(self.col_count - 3):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
    

    def Start(self):
        while not self.game_over:
            self.Draw()
            self.Input()
#             Logic()
        
    
  