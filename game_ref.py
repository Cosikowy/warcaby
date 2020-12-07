



class Board:
    players = []
    
    def __init__(self, rows, cols, p1 = 'p1', p2 = 'p2'):
        self.board = [[Placeholder() for x in range(cols)] for _ in range(rows)]
        self.player_1 = p1
        self.player_2 = p2
        
    def draw_board(self):
        print(
            '  ',' |', ' A',' |', ' B',' |', ' C',' |', ' D',' |', ' E' ,' |', ' F',' |', ' G',' |', ' H', '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '1', ' |', self.board[0][7],' |',  self.board[1][7],' |', self.board[2][7],' |', self.board[3][7],' |', self.board[4][7],' |', self.board[5][7],' |', self.board[6][7],' |', self.board[7][7], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '2', ' |', self.board[0][6],' |',  self.board[1][6],' |', self.board[2][6],' |', self.board[3][6],' |', self.board[4][6],' |', self.board[5][6],' |', self.board[6][6],' |', self.board[7][6], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '3', ' |', self.board[0][5],' |',  self.board[1][5],' |', self.board[2][5],' |', self.board[3][5],' |', self.board[4][5],' |', self.board[5][5],' |', self.board[6][5],' |', self.board[7][5], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '4', ' |', self.board[0][4],' |',  self.board[1][4],' |', self.board[2][4],' |', self.board[3][4],' |', self.board[4][4],' |', self.board[5][4],' |', self.board[6][4],' |', self.board[7][4], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '5', ' |', self.board[0][3],' |',  self.board[1][3],' |', self.board[2][3],' |', self.board[3][3],' |', self.board[4][3],' |', self.board[5][3],' |', self.board[6][3],' |', self.board[7][3], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '6', ' |', self.board[0][2],' |',  self.board[1][2],' |', self.board[2][2],' |', self.board[3][2],' |', self.board[4][2],' |', self.board[5][2],' |', self.board[6][2],' |', self.board[7][2], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '7', ' |', self.board[0][1],' |',  self.board[1][1],' |', self.board[2][1],' |', self.board[3][1],' |', self.board[4][1],' |', self.board[5][1],' |', self.board[6][1],' |', self.board[7][1], '\n', \
            '-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n', \
            '8', ' |', self.board[0][0],' |', self.board[1][0],' |', self.board[2][0], ' |', self.board[3][0],' |', self.board[4][0],' |', self.board[5][0],' |', self.board[6][0],' |', self.board[7][0], '\n', \
        )

    def make_move(self):
        pass
    
    def check_for_promote(self):
        pass
    
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
    def __init__(self):
        self.name = 'BlankSpace'

    def __repr__(self):
        return ' x'


# class Game:...
b = Board(8,8)
# b.draw_board()

s = Stone('b', 'q')
print(s)
