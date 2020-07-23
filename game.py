import pandas as pd
import numpy as np
import pprint
import os

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

        # self.winner = None

        horizontal = ['a','b','c','d','e','f','g','h'] 
        wertical = [1,2,3,4,5,6,7,8]
        self.move_dict = {}
        for x,n_x in zip(horizontal, range(8)):
            for y,n_y in zip(reversed(wertical), range(8)):
                self.move_dict[(x,y)] = (n_x, n_y)

    def winner(self):
        black_count = 0
        white_count = 0
        for x, _ in enumerate(self.board):
            for y, _ in enumerate(self.board[0]):
                if isinstance(self.board[x][y], Stone):
                    if self.board[x][y].color == 'white':
                        white_count+=1
                    else:
                        black_count+=1
        if white_count == 0:
            return True, 'white'
        if black_count == 0:
            return True, 'black'
        
        return False, 'noone'

    def decode_move(self, old_pos, new_pos):
        old_tup = self.move_dict[(old_pos[0], int(old_pos[1]))]
        new_tup = self.move_dict[(new_pos[0], int(new_pos[1]))]
        return old_tup, new_tup

    def stones(self):
        for x, _ in enumerate(self.board):
            for y, _ in enumerate(self.board[0]):
                if isinstance(self.board[x][y], Stone):
                    yield self.board[x][y]

    def draw_board(self):
        print(
            '  ', ' A', ' B', ' C', ' D', ' E' , ' F', 'G ', ' H', '\n',
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
        self.pos = (col, row)
        if self.color == 'black' and self.mode == 'normal':
            self.name = 'BS'
        if self.color == 'black' and self.mode == 'queen':
            self.name = 'BQ'
        if self.color == 'white' and self.mode == 'normal':
            self.name = 'WS'
        if self.color == 'white' and self.mode == 'queen':
            self.name = 'WQ'


    def upgrade(self):
        self.mode = 'queen'
        if self.color == 'white':
            self.name = 'WQ'
        else:
            self.name = 'BQ'


    def make_move(self, new_pos, game):
        attacked = False
        if game.turn == self.color:
            validation, event_place, new_pos, event = self.validate_move(self.pos, new_pos, self.mode, game, self.color)
            if validation:
                if event:
                    if event=='delete':
                        game.board[event_place[1]][event_place[0]] = BlankSpace()
                        attacked = True
                game.board[self.row][self.col] = BlankSpace()
                game.board[new_pos[1]][new_pos[0]] = self
                self.update_pos(new_pos)
                self.pos = (new_pos[0],new_pos[1])
                if game.turn == 'white':
                    game.turn = 'black'
                else:
                    game.turn = 'white'
            else:
                event = 'Wrong move'
        else:
            event = 'Wrong color'
        return game, attacked, new_pos, event


    def check_for_upgrade(self, pos):
        white_upgrade = [(1,0),(3,0),(5,0),(7,0)]
        black_upgrade = [(0,7),(2,7),(4,7),(5,7)]
        if self.color == 'white':
            if pos in white_upgrade:
                return True
        else:
            if pos in black_upgrade:
                return True
        return False


    def update_pos(self, new_pos):
        self.row = new_pos[1]
        self.col = new_pos[0]
        self.pos = (new_pos[1], new_pos[0])


    def stone_enviroment(self, old_pos, game, color):
        enviroment = {}
        try:
            if isinstance(game.board[old_pos[1]-1][old_pos[0]+1],BlankSpace): # up/right
                enviroment[(old_pos[0]+1,old_pos[1]-1)] = ((old_pos[0]+1,old_pos[1]-1), None)
            else:
                if game.board[old_pos[1]-1][old_pos[0]+1].color!=color and isinstance(game.board[old_pos[1]-2][old_pos[0]+2], BlankSpace):
                    enviroment[(old_pos[0]+1,old_pos[1]-1)] = ((old_pos[0]+2,old_pos[1]-2), 'delete')
        except IndexError:
            pass
        try:
            if isinstance(game.board[old_pos[1]-1][old_pos[0]-1],BlankSpace): # up/left
                enviroment[(old_pos[0]-1,old_pos[1]-1)] = ((old_pos[0]-1,old_pos[1]-1), None)
            else:
                if game.board[old_pos[1]-1][old_pos[0]-1].color!=color and isinstance(game.board[old_pos[1]-2][old_pos[0]-2], BlankSpace):
                    enviroment[(old_pos[0]-1,old_pos[1]-1)] = ((old_pos[0]-2,old_pos[1]-2), 'delete')
        except IndexError:
            pass
        try:
            if isinstance(game.board[old_pos[1]+1][old_pos[0]+1],BlankSpace): # down/right
                enviroment[(old_pos[0]+1,old_pos[1]+1)] = ((old_pos[0]+1,old_pos[1]+1), None)
            else:
                if game.board[old_pos[1]+1][old_pos[0]+1].color!=color and isinstance(game.board[old_pos[1]+2][old_pos[0]+2], BlankSpace):
                    enviroment[(old_pos[0]+1,old_pos[1]+1)] = ((old_pos[0]+2,old_pos[1]+2), 'delete')
        except IndexError:
            pass
        try:
            if isinstance(game.board[old_pos[1]+1][old_pos[0]-1],BlankSpace): # down/left
                enviroment[(old_pos[0]-1,old_pos[1]+1)] = ((old_pos[0]-1,old_pos[1]+1), None)
            else:
                if game.board[old_pos[1]+1][old_pos[0]-1].color!=color and isinstance(game.board[old_pos[1]+2][old_pos[0]-2], BlankSpace):
                    enviroment[(old_pos[0]-1,old_pos[1]+1)] = ((old_pos[0]-2,old_pos[1]+2), 'delete')
        except IndexError:
            pass
        return enviroment


    def queen_enviroment(self, old_pos, game, color):
        enviroment = {}
        attack = None
        attacked_at = None
        for x in range(1,8):
            if old_pos[0]+x>8:
                break
            if old_pos[1]-x<1:
                break
            try:
                if isinstance(game.board[old_pos[1]-x][old_pos[0]+x],BlankSpace): # up/right
                    enviroment[(old_pos[0]+x,old_pos[1]-x)] = ((old_pos[0]+x,old_pos[1]-x), attack)
                else:
                    if game.board[old_pos[1]-x][old_pos[0]+x].color!=color and isinstance(game.board[old_pos[1]-(x+1)][old_pos[0]+(x+1)], BlankSpace):
                        enviroment[(old_pos[0]+x,old_pos[1]-x)] = ((old_pos[0]+(x+1),old_pos[1]-(x+1)), 'delete')
                        attack = 'delete'
                        attacked_at = (old_pos[0]+x,old_pos[1]-x)
                    else:
                        break
            except IndexError:
                pass
        attack = None
        for x in range(1,8):
            if old_pos[0]-x<0:
                break
            if old_pos[1]-x<0:
                break
            try:
                if isinstance(game.board[old_pos[1]-x][old_pos[0]-x],BlankSpace): # up/left
                    enviroment[(old_pos[0]-x,old_pos[1]-x)] = ((old_pos[0]-x,old_pos[1]-x), attack)
                else:
                    if game.board[old_pos[1]-x][old_pos[0]-x].color!=color and isinstance(game.board[old_pos[1]-(x+1)][old_pos[0]-(x+1)], BlankSpace):
                        enviroment[(old_pos[0]-x,old_pos[1]-x)] = ((old_pos[0]-(x+1),old_pos[1]-(x+1)), 'delete')
                        attacked_at = (old_pos[0]-x,old_pos[1]-x)
                        attack = 'delete'
                    else:
                        break
            except IndexError:
                pass
        attack = None
        for x in range(1,8):
            if old_pos[0]+x>8:
                break
            if old_pos[1]+x>8:
                break
            try:
                if isinstance(game.board[old_pos[1]+x][old_pos[0]+x],BlankSpace): # down/right
                    enviroment[(old_pos[0]+x,old_pos[1]+x)] = ((old_pos[0]+x,old_pos[1]+x), attack)
                else:
                    if game.board[old_pos[1]+x][old_pos[0]+x].color!=color and isinstance(game.board[old_pos[1]+(x+1)][old_pos[0]+(x+1)], BlankSpace):
                        enviroment[(old_pos[0]+x,old_pos[1]+x)] = ((old_pos[0]+(x+1),old_pos[1]+(x+1)), 'delete')
                        attacked_at = (old_pos[0]+x,old_pos[1]+x)
                        attack = 'delete'
                    else:
                        break
            except IndexError:
                pass
        attack = None
        for x in range(1,8):
            if old_pos[0]+x>8:
                break
            if old_pos[1]-x<1:
                break
            try:
                if isinstance(game.board[old_pos[1]+x][old_pos[0]-x],BlankSpace): # down/left
                    enviroment[(old_pos[0]-x,old_pos[1]+x)] = ((old_pos[0]-x,old_pos[1]+x), attack)
                else:
                    if game.board[old_pos[1]+x][old_pos[0]-x].color!=color and isinstance(game.board[old_pos[1]+(x+1)][old_pos[0]-(x+1)], BlankSpace):
                        enviroment[(old_pos[0]-x,old_pos[1]+x)] = ((old_pos[0]-(x+1),old_pos[1]+(x+1)), 'delete')
                        attacked_at = (old_pos[0]-x,old_pos[1]+x)
                        attack = 'delete'
                    else:
                        break
            except IndexError:
                pass
        return enviroment, attacked_at


    def validate_move(self, old_pos, new_pos, stone_type, game, color):
        possible_moves = []
        effect = []
        all_possible_moves = []
        for stone in game.stones():
            if stone.mode == 'normal' and stone.color == color:
                all_possible_moves.append(stone.stone_enviroment(stone.pos, game, color))
            elif stone.mode == 'normal' and stone.color == color:
                all_possible_moves.append(stone.queen_enviroment(stone.pos, game, color))
        
        priority_moves = {}
        for moves in all_possible_moves:
            if moves.keys():
                for key, value in moves.items():
                    if moves[key][1] == 'delete':
                        priority_moves[key] = value


        if stone_type=='normal':
            possible_moves = self.stone_enviroment(old_pos,game, color)
            if priority_moves.keys():
                if new_pos in priority_moves.keys():
                    return True, new_pos, possible_moves[new_pos][0], possible_moves[new_pos][1]
                else:
                    return False, None, None, 'attack is required'
            if new_pos in possible_moves.keys():
                if possible_moves[new_pos][1] is None:
                    if color == 'white':
                        if old_pos[1]-new_pos[1] == -1:
                            return False, None, None, None
                    else:
                        if old_pos[1]-new_pos[1] == 1:
                            return False, None, None, None
                return True, new_pos, possible_moves[new_pos][0], possible_moves[new_pos][1]
            else:
                return False, None, None, None
        else:
            possible_moves, attacked_at = selected.queen_enviroment(old_pos, game, game.turn)
            priority_moves = {}
            for key, value in possible_moves.items():
                if possible_moves[key][1] == 'delete':
                    priority_moves[key] = value
            if priority_moves.keys():
                if new_pos in priority_moves.keys():
                    return True, attacked_at, possible_moves[new_pos][0], possible_moves[new_pos][1]
                else:
                    return False, None, None, 'attack is required'
            if new_pos in possible_moves.keys():
                return True, attacked_at, possible_moves[new_pos][0], possible_moves[new_pos][1]

    def __repr__(self):
        return self.name


class Game:
    
    def __init__(self):
        self.ID = ''
    
    def validate_input(self, _input):
        try:
            old = _input.split(',')[0]
            new = _input.split(',')[1]
            horizontal = ['a','b','c','d','e','f','g','h'] 
            wertical = [1,2,3,4,5,6,7,8]
            
            if old[0] not in horizontal:
                return False
            if int(old[1]) not in wertical:
                return False
            if new[0] not in horizontal:
                return False
            if int(new[1]) not in wertical:
                return False
            return True
        
        except:
            return False

    def run_game(self):
        b = Board(8,8)
        event = None
        while True:
            os.system('cls')
            b.draw_board()
            if event:
                print(event)
            print('Turn: ', b.turn)
            move = input("What's ur move? ")
            if self.validate_input(move):

                old_pos = move.split(',')[0]
                new_pos = move.split(',')[1]
                picked_stone = move.split(',')[0]
                destination = move.split(',')[1]
                old_pos, new_pos = b.decode_move(old_pos, new_pos)
                selected = b.board[old_pos[1]][old_pos[0]]
                if isinstance(selected, Stone):
                    b, attacked, new_pos, move_event = b.board[old_pos[1]][old_pos[0]].make_move(new_pos, b)
                    if attacked:
                        if move_event == 'deleted':
                            event = f'Attacked at {destination}'
                        possible_attack = False
                        if selected.mode =='normal':
                            enviroment = selected.stone_enviroment(selected.pos, b, b.turn)
                        else:
                            enviroment, _ = selected.queen_enviroment(selected.pos, b, b.turn)
                        for key, value in enviroment.items():
                            if value[1] == 'delete':
                                possible_attack = True
                                break
                        if possible_attack:
                            possible_attack = False
                            if b.turn == 'white':
                                b.turn = 'black'
                            else:
                                b.turn = 'white'
                    else:
                        event = f'Moved to {destination}'
                    if selected.check_for_upgrade(new_pos):
                        selected.mode = 'queen'
                        if selected.color == 'white':
                            selected.name = 'WQ'
                        else:
                            selected.name = 'BQ'
                else:
                    event = 'You picked blank space'
            else:
                event = 'Wrong move'


                winner_check, winner = b.winner()

                if winner_check:
                    return winner




game1 = Game()

game1.run_game()

