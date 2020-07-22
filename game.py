import pandas as pd
import numpy as np
import pprint

class Board:
    players = []


    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.ready = False
        self.last = None

        self.board = [[BlankSpace() for x in range(8)] for _ in range(rows)]

        self.board[0][1] = Stone(0,1,'black','normal')
        self.board[0][3] = Stone(0,3,'black','normal')
        self.board[0][5] = Stone(0,5,'black','normal')
        self.board[0][7] = Stone(0,7,'black','normal')
        self.board[1][0] = Stone(1,0,'black','normal')
        self.board[1][2] = Stone(1,2,'black','normal')
        self.board[1][4] = Stone(1,4,'black','normal')
        self.board[1][6] = Stone(1,6,'black','normal')
        self.board[2][1] = Stone(2,1,'black','normal')
        self.board[2][3] = Stone(2,3,'black','normal')
        self.board[2][5] = Stone(2,5,'black','normal')
        self.board[2][7] = Stone(2,7,'black','normal')

        self.board[7][0] = Stone(7,0,'white','normal')
        self.board[7][2] = Stone(7,2,'white','normal')
        self.board[7][4] = Stone(7,4,'white','normal')
        self.board[7][6] = Stone(7,6,'white','normal')
        self.board[6][1] = Stone(6,1,'white','normal')
        self.board[6][3] = Stone(6,3,'white','normal')
        self.board[6][5] = Stone(6,5,'white','normal')
        self.board[6][7] = Stone(6,7,'white','normal')
        self.board[5][0] = Stone(5,0,'white','normal')
        self.board[5][2] = Stone(5,2,'white','normal')
        self.board[5][4] = Stone(5,4,'white','normal')
        self.board[5][6] = Stone(5,6,'white','normal')

        self.player1 = 'p1'
        self.player2 = 'p2'
        
        self.turn = 'white'

        self.winner = None

        horizontal = ['a','b','c','d','e','f','g','h'] 
        wertical = [1,2,3,4,5,6,7,8]

        self.move_dict = {}
        for x,n_x in zip(horizontal, range(8)):
            for y,n_y in zip(reversed(wertical), range(8)):
                self.move_dict[(x,y)] = (n_x, n_y)

    def decode_move(self, old_pos, new_pos):
        old_tup = self.move_dict[(old_pos[0], int(old_pos[1]))]
        new_tup = self.move_dict[(new_pos[0], int(new_pos[1]))]
        return old_tup, new_tup

    def draw_board(self):
        print(
            '  ', ' A', ' B', ' C', ' D', ' E' , ' F', ' G', ' H', '\n',
            '8', self.board[0][0], self.board[0][1], self.board[0][2], self.board[0][3], self.board[0][4], self.board[0][5], self.board[0][6], self.board[0][7], '\n',
            '7', self.board[1][0], self.board[1][1], self.board[1][2], self.board[1][3], self.board[1][4], self.board[1][5], self.board[1][6], self.board[1][7], '\n',
            '6', self.board[2][0], self.board[2][1], self.board[2][2], self.board[2][3], self.board[2][4], self.board[2][5], self.board[2][6], self.board[2][7], '\n',
            '5', self.board[3][0], self.board[3][1], self.board[3][2], self.board[3][3], self.board[3][4], self.board[3][5], self.board[3][6], self.board[3][7], '\n',
            '4', self.board[4][0], self.board[4][1], self.board[4][2], self.board[4][3], self.board[4][4], self.board[4][5], self.board[4][6], self.board[4][7], '\n',
            '3', self.board[5][0], self.board[5][1], self.board[5][2], self.board[5][3], self.board[5][4], self.board[5][5], self.board[5][6], self.board[5][7], '\n',
            '2', self.board[6][0], self.board[6][1], self.board[6][2], self.board[6][3], self.board[6][4], self.board[6][5], self.board[6][6], self.board[6][7], '\n',
            '1', self.board[7][0], self.board[7][1], self.board[7][2], self.board[7][3], self.board[7][4], self.board[7][5], self.board[7][6], self.board[7][7], '\n',
        )


class BlankSpace:
    def __init__(self):
        self.name = 'BlankSpace'

    def __repr__(self):
        return ' *'


class Stone:
    def __init__(self, row, col, color, mode):
        self.color = color
        self.mode = mode
        self.row = row
        self.col = col
        self.pos = (col, row) # (y,x) cords


        if self.color == 'black' and self.mode == 'normal':
            self.name = 'BS'
        if self.color == 'black' and self.mode == 'queen':
            self.name = 'BQ'
        if self.color == 'white' and self.mode == 'normal':
            self.name = 'WS'
        if self.color == 'white' and self.mode == 'queen':
            self.name = 'WQ'

    def make_move(self, new_pos, game, turn):
        if game.board[self.row][self.col].name==self.name and game.turn == self.color:
            if self.validate_move(self.pos, new_pos, self.mode, game.board, self.color):
                print('color: ', self.color)
                print('ok validated')

            
                game.board[self.row][self.col] = BlankSpace()
                game.board[new_pos[1]][new_pos[0]] = self
                self.update_pos(new_pos)
                self.pos = (new_pos[0],new_pos[1])
                
                if game.turn == 'white':
                    game.turn = 'black'
                else:
                    game.turn = 'white'
            else:
                print('not validated')
        return game

    def update_pos(self, new_pos):
        self.row = new_pos[1]
        self.col = new_pos[0]
        self.pos = (self.col, self.row)  # (y,x) cords

    def validate_move(self, old_pos, new_pos, stone_type, board, color):
        print('old pos:', old_pos)
        print('new pos:', new_pos)
        
        if stone_type=='normal':

            if color == 'white':
                # LEFT / RIGHR + UP
                if old_pos[0]-new_pos[0] == 1 or old_pos[0]-new_pos[0] == -1:
                    if old_pos[1]-new_pos[1] == 1:
                        print('ok')
                    else:
                        return False
                else:
                    print('not ok')
                    return False
            else:
                # LEFT / RIGHR + DOWN
                if old_pos[0]-new_pos[0] == 1 or old_pos[0]-new_pos[0] == -1:
                    if old_pos[1]-new_pos[1] == -1:
                        print('ok')
                    else:
                        return False
                else:
                    print('not ok')
                    return False
        else:
            pass

        if True:
            return True
        else:
            return False

    def __repr__(self):
        return self.name

b = Board(8,8)

b.draw_board()





while True:
    print('Turn: ', b.turn)
    old_pos = input('Pick stone: ')
    new_pos = input("What's ur move? ")
    old_pos, new_pos = b.decode_move(old_pos, new_pos)
    selected = b.board[old_pos[1]][old_pos[0]]

    if isinstance(selected, Stone):
        b = b.board[old_pos[1]][old_pos[0]].make_move(new_pos, b, 'w')
    else:
        print('U picked blak space')

    b.draw_board()



'''
# def translate(old_pos, new_pos, move_dict):
    
#     # old_tup = ()
#     # new_tup = (new_pos[0], new_pos[1])
#     print(old_pos)
#     print(new_pos)
#     old_tup = move_dict[(old_pos[0], int(old_pos[1]))]
#     new_tup = move_dict[(new_pos[0], int(new_pos[1]))]
#     print(old_tup)
#     print(new_tup)

# horizontal = ['a','b','c','d','e','f','g','h']
# wertical = [1,2,3,4,5,6,7,8]

# move_dict = {}
# for x,n_x in zip(horizontal, range(8)):
#     for y,n_y in zip(reversed(wertical), reversed(range(8))):
#         move_dict[(x,y)] = (n_x, n_y)


# # old_x, old_y, new_x, new_y = 
# translate('a1', 'b2', move_dict)
# print('old: ', old_x, ' ', old_y)
# print('new: ', new_x, ' ', new_y)
# pprint.pprint(move_dict)
#'''