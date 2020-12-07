


class Board:
    def __init__(self, p1 = 'p1', p2 = 'p2'):
        self.board = [[Placeholder() for x in range(8)] for _ in range(8)]
        self.player_1 = p1
        self.player_2 = p2
        self.players = (self.player_1, self.player_2)
        
        self.white_starting_pos = (
            (0,2), (2,2), (4,2), (6,2),
            (1,1), (3,1), (5,1), (7,1),
            (0,0), (2,0), (4,0), (6,0)
        )
        
        self.black_starting_pos = (
            (1,7), (3,7), (5,7), (7,7),
            (0,6), (2,6), (4,6), (6,6),
            (1,5), (3,5), (5,5), (7,5)
        )
        for white, black in zip(self.white_starting_pos, self.black_starting_pos):
            self.board[white[0]][white[1]] = Stone()
            self.board[black[0]][black[1]] = Stone('black')
        
    def draw_board(self):
        columns_row = ('  ',' |', ' A',' |', ' B',' |', ' C',' |', ' D',' |', ' E' ,' |', ' F',' |', ' G',' |', ' H', '\n')
        spacer = ('-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n')
        board = [*columns_row, *spacer]
        def print_row(number):
            row = []
            for x in range(8):
                row.append(' |')
                row.append(self.board[x][number])
            row.append('\n')
            return (f'{number+1}', *row)
        for row in reversed(range(8)):
            board.extend(print_row(row))
            board.extend(spacer)
        print(*board)
    
    def make_move(self, old_pos, new_pos):
        if isinstance(self.board[old_pos[0]][old_pos[1]], Stone):
            if isinstance(self.board[new_pos[0]][new_pos[1]]):
                self.board[new_pos[0]][new_pos[1]], self.board[old_pos[0]][old_pos[1]] = \
                self.board[old_pos[0]][old_pos[1]], Placeholder()
                return True
            else:
                raise Exception("It's ain't no free place")
        else:
            raise Exception("It's ain't no stone!")
    
    def check_for_promote(self, pos):
        white_promote = ((x,7) for x in range(8))
        black_promote = ((x,0) for x in range(8))
        return True if pos in white_promote or pos in black_promote else False
    
    def check_winner(self):
        pass
        





class Stone:
    def __init__(self, color = None, stone_type = None):
        self.name = "Stone"
        self.color = color.capitalize() if color else 'White'
        self.type = stone_type.capitalize() if stone_type else 'Stone'
    
    def __repr__(self):
        return f'{self.color[0]}{self.type[0]}'

 
class Placeholder:
    def __repr__(self):
        return ' x'


# class Game:...
b = Board()


# s = Stone('b', 'q')
# print(s)
