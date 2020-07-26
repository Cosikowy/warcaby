import unittest
from game import Board, Stone, Game, Placeholder


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game_board = Game(1)
        self.game_board.board = [[Placeholder() for x in range(8)] for _ in range(8)]
    
    def test_move_decoder(self):
        self.pos_1 = 'a8'
        self.pos_2 = 'b7'
        self.pos_3 = 'c6'
        self.pos_4 = 'd5'

        pos_1, pos_2 = self.game_board.decode_move(self.pos_1, self.pos_2)
        pos_3, pos_4 = self.game_board.decode_move(self.pos_3, self.pos_4)

        self.assertEqual(pos_1, (0,0))
        self.assertEqual(pos_2, (1,1))
        self.assertEqual(pos_3, (2,2))
        self.assertEqual(pos_4, (3,3))
    
    def test_input_validation(self):
        self.input_1 = 'a1,b2'
        self.input_2 = 'c1,4f'
        self.input_3 = '1a,b2'
        self.input_4 = '1a,2b'
        self.input_5 = 'j2,k2'

        input_1 = self.game_board.validate_input(self.input_1)
        input_2 = self.game_board.validate_input(self.input_2)
        input_3 = self.game_board.validate_input(self.input_3)
        input_4 = self.game_board.validate_input(self.input_4)
        input_5 = self.game_board.validate_input(self.input_5)

        self.assertTrue(input_1)
        self.assertFalse(input_2)
        self.assertFalse(input_3)
        self.assertFalse(input_4)
        self.assertFalse(input_5)
    

class TestStone(unittest.TestCase):
    def setUp(self):
        self.game_board = Board(8,8)
        self.game_board.board = [[Placeholder() for x in range(8)] for _ in range(8)]
        self.test_stone = Stone(1,7,'white','normal')
        self.test_stone_2 = Stone(1,2,'white','queen')
        self.test_stone_3 = Stone(6,5,'black','normal')
        self.test_stone_4 = Stone(6,1,'black','queen')

        self.game_board.board[1][7], self.game_board.board[1][2] = self.test_stone, self.test_stone_2
        self.game_board.board[6][5], self.game_board.board[6][1] = self.test_stone_3, self.test_stone_4

        self.game_board, self.attacked, self.new_pos, self.event \
        =  self.test_stone_2.make_move((1,0), self.game_board)
        
        self.game_board, self.attacked_2, self.new_pos_2, self.event_2 \
        =  self.test_stone_3.make_move((7,6), self.game_board)

            
    def test_move(self):
        self.assertFalse(self.attacked)
        self.assertEqual(self.new_pos, (1,0))
        self.assertEqual(self.event, None)

    def test_upgrade(self):
        upgrade = self.test_stone_2.check_for_upgrade((1,0))
        self.assertTrue(upgrade)
        upgrade_2 = self.test_stone_2.check_for_upgrade((1,7))
        self.assertFalse(upgrade_2)
        upgrade_3 = self.test_stone_3.check_for_upgrade((0,7))
        self.assertTrue(upgrade_3)
        upgrade_4 = self.test_stone_4.check_for_upgrade((1,7))
        self.assertFalse(upgrade_4)

    def test_enviroment(self):
        env_1 = self.test_stone.stone_enviroment((1,7), self.game_board, 'white')
        self.assertEqual(len(env_1.keys()), 2)
        env_2 = self.test_stone_2.queen_enviroment((1,0), self.game_board, 'white')
        self.assertEqual(len(env_2[0].keys()), 7)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.game_board = Board(8,8)
        
    def test_stones(self):
        for item in self.game_board.stones():
            self.assertTrue(isinstance(item, Stone))

    def test_winner(self):
        self.game_board.board = [[Placeholder() for x in range(8)] for _ in range(8)]
        
        self.game_board.board[0][0] = Stone(0,0,'white','queen')
        finished, winner = self.game_board.winner()
        self.assertTrue(finished)
        self.assertEqual(winner, 'white')

        self.game_board.board[0][0] = Stone(0,0,'black','queen')
        finished, winner = self.game_board.winner()
        self.assertTrue(finished)
        self.assertEqual(winner, 'black')



if __name__ == '__main__':
    unittest.main()
