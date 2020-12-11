from pprint import pprint

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
        # for white, black in zip(self.white_starting_pos, self.black_starting_pos):
        #     self.board[white[0]][white[1]] = Stone()
        #     self.board[black[0]][black[1]] = Stone('black')
        
    def draw_board(self):
        # columns_row = ('  ',' |', ' A',' |', ' B',' |', ' C',' |', ' D',' |', ' E' ,' |', ' F',' |', ' G',' |', ' H', '\n')
        columns_row = ('  ',' |', ' 0',' |', ' 1',' |', ' 2',' |', ' 3',' |', ' 4' ,' |', ' 5',' |', ' 6',' |', ' 7', '\n')
        
        spacer = ('-',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +',' -',' +', ' -', '\n')
        board = [*columns_row, *spacer]
        def print_row(number):
            row = []
            for x in range(8):
                row.append(' |')
                row.append(self.board[x][number])
            row.append('\n')
            return (f'{number}', *row)
        for row in reversed(range(8)):
            board.extend(print_row(row))
            board.extend(spacer)
        print(*board)
    
    def move_list(self, pos):
        move_list = []    
        x = pos[0]
        y = pos[1]
        self.board[x][y] = Stone()
        
        stone = self.board[x][y]
        
        iterations = 1
        for new_pos in range(x+1, 8, 1):  # right moves
            # if y+iterations==8:
            #     break
            if isinstance(self.board[new_pos][y+iterations], Placeholder):
                move_list.append((new_pos,y+iterations))
            elif isinstance(self.board[new_pos][y+iterations+1], Placeholder):
                move_list.append((new_pos,y+iterations+1))

            if isinstance(self.board[new_pos][y-iterations],Placeholder):
                move_list.append((new_pos,y-iterations))
            elif isinstance(self.board[new_pos][y-(iterations+1)], Placeholder):
                move_list.append((new_pos,y-(iterations+1)))
            iterations+=1
        
        print(x)
        
        iterations = 1
        for new_pos in range(x-1, -1, -1):  # left moves
            if y+iterations==8:
                break
            
            if isinstance(self.board[new_pos][y+iterations], Placeholder):
                move_list.append((new_pos,y+iterations))
            elif isinstance(self.board[new_pos][y+iterations+1], Placeholder):
                move_list.append((new_pos,y+iterations+1))

            if isinstance(self.board[new_pos][y-iterations],Placeholder):
                move_list.append((new_pos,y-iterations))
            elif isinstance(self.board[new_pos][y-(iterations+1)], Placeholder):
                move_list.append((new_pos,y-(iterations+1)))
        
            iterations+=1

        return move_list
    
    
    
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
    def __init__(self, name = 'x'):
        self.name = name
        
    def __repr__(self):
        return f' {self.name}'


# class Game:...
b = Board()
moves = b.move_list((3,3))
for (x,y) in moves:
    b.board[x][y] = Placeholder('C')

b.draw_board()
print(moves)

# s = Stone('b', 'q')
# print(s)
