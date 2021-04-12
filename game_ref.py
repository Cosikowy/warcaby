from pprint import pprint


class Board:
    def __init__(self, p1='p1', p2='p2'):
        self.board = [[Placeholder() for x in range(8)] for _ in range(8)]
        self.player_1 = p1
        self.player_2 = p2
        self.players = (self.player_1, self.player_2)

        self.white_starting_pos = (
            (0, 2), (2, 2), (4, 2), (6, 2),
            (1, 1), (3, 1), (5, 1), (7, 1),
            (0, 0), (2, 0), (4, 0), (6, 0)
        )

        self.black_starting_pos = (
            (1, 7), (3, 7), (5, 7), (7, 7),
            (0, 6), (2, 6), (4, 6), (6, 6),
            (1, 5), (3, 5), (5, 5), (7, 5)
        )
        # for white, black in zip(self.white_starting_pos, self.black_starting_pos):
        #     self.board[white[0]][white[1]] = Stone()
        #     self.board[black[0]][black[1]] = Stone('black')

    def draw_board(self):
        def print_row(number):
            row = []
            for x in range(8):
                row.append(' |')
                row.append(self.board[x][number])
            row.append('\n')
            return (f'{number}', *row)
        # columns_row = ('  ',' |', ' A',' |', ' B',' |', ' C',' |', ' D',' |', ' E' ,' |', ' F',' |', ' G',' |', ' H', '\n')
        columns_row = ('  ', ' |', ' 0', ' |', ' 1', ' |', ' 2', ' |',
                       ' 3', ' |', ' 4', ' |', ' 5', ' |', ' 6', ' |', ' 7', '\n')

        spacer = ('-', ' +', ' -', ' +', ' -', ' +', ' -', ' +', ' -',
                  ' +', ' -', ' +', ' -', ' +', ' -', ' +', ' -', '\n')
        board = [*columns_row, *spacer]
        for row in reversed(range(8)):
            board.extend(print_row(row))
            board.extend(spacer)
        print(*board)

    def move_list(self, pos):
        def moves_on_line(x_range, y_range, moves):
            action = 'move'
            try:
                for i, (new_x, new_y) in enumerate(zip(x_range, y_range)):
                    if isinstance(self.board[new_x][new_y], Placeholder):
                        moves[(new_x, new_y)] = action
                    elif self.board[new_x][new_y].color == stone.color:
                        break
                    elif isinstance(self.board[x_range[i+1]][y_range[i+1]], Placeholder):
                        action = f'attack;{new_x},{new_y}'
                        moves[(new_x, new_y)] = action
            except IndexError:
                pass
       
        move_list = {}
        x, y = pos[0], pos[1]
        self.board[x][y] = Stone()    # for testing pourpose
        stone = self.board[x][y]


        moves_on_line(range(x+1, 8), range(y+1, 8), move_list)  # up right
        moves_on_line(range(x+1, 8), range(y-1, -1, -1),
                      move_list)  # down right
        moves_on_line(range(x-1, -1, -1), range(y+1, 8), move_list)  # up left
        moves_on_line(range(x-1, -1, -1), range(y-1, -1, -1),
                      move_list)  # down left
        return move_list

    def move(self, old_pos, new_pos):
        x, y, new_x, new_y = old_pos[0], old_pos[1], new_pos[0], new_pos[1]
        self.board[x][y], self.board[new_x][new_y] =\
            Placeholder(), self.board[x][y]

    def validate_move(self, old_pos, new_pos):
        move_list = self.move_list(old_pos)
        x, y, new_x, new_y = old_pos[0], old_pos[1], new_pos[0], new_pos[1]

        stone = self.board[x][y]

        if not new_pos in move_list.keys():
            return False

        if abs(x - new_x) > 2:
            return False

        if stone.type == 'stone'.capitalize():
            if stone.color == 'white'.capitalize():
                return y - new_y < -2
            else:
                return y - new_y > 2

        return True

    def check_for_promote(self, pos):
        stone = self.board[pos[0]][pos[1]]

        white_promote = ((x, 7) for x in range(8))
        black_promote = ((x, 0) for x in range(8))

        if stone.color == 'white'.capitalize():
            return True if pos in white_promote else False
        else:
            return True if pos in black_promote else False

    def check_winner(self):
        stones = {'White':0, 'Black':0 }
        for x, line in enumerate(self.board):
            for y, stone in enumerate(line):
                if isinstance(stone, Stone):
                    stones[stone.color] += 1
        
        if stones['White'] == 0:
            return True, 'Black'
        elif stones['Black'] == 0:
            return True, 'White'
        else:
            return False, None
    
    
class Stone:
    def __init__(self, color=None, stone_type=None):
        self.name = "Stone"
        self.color = color.capitalize() if color else 'White'
        self.type = stone_type.capitalize() if stone_type else 'Stone'

    def __repr__(self):
        return f'{self.color[0]}{self.type[0]}'


class Placeholder:
    def __init__(self, name='x'):
        self.name = name

    def __repr__(self):
        return f' {self.name}'


# class Game:...
b = Board()
b.board[2][4] = Stone('black')
# b.board[4][4] = Stone('white')

moves = b.move_list((3, 3))
for (x, y) in moves.keys():
    b.board[x][y] = Placeholder(f'{moves[(x,y)][0]}')
# b.board[2][4] = Stone('black')


b.draw_board()
print(b.check_winner())
# pprint(moves)


# b.move((4,4),(6,6))
# b.draw_board()

# s = Stone('b', 'q')
# print(s)
