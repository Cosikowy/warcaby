import asyncio
import socket
import json
import pickle
from game import Game
import os

async def wait_for_data():
    loop = asyncio.get_running_loop()
    send_dict = {
            'name':'',
            'msg':'',
            'game_id': '',
            'player_status':'new'
            }
        

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost',5000))

    reader, writer = await asyncio.open_connection(sock=client)
    
    connected = True
    send_dict['name'] = input('name: ')
    incorrect_name = True
    while incorrect_name:
        name_msg = json.dumps(send_dict)
        loop.call_soon(client.send, name_msg.encode())
        response = await reader.read(2048)
        response = response.decode()
        # print(response)
        if response != 'Name already used!':
            incorrect_name = False
            send_dict['player_status'] = 'existing'
        else:
            print('Name already in use!')
            send_dict['name'] = input('name: ')

    no_enemy = True
    
    try:
        response = json.loads(response)
        if response['game_id']!='':
            no_enemy = False
    except:
        pass

    while no_enemy:
        response = await reader.read(2048)
        response = response.decode()
        print('waiting for enemy')
        if response != 'wait':
            no_enemy = False
    try:
        response = json.loads(response)
    except:
        pass
    send_dict['game_id'] = response['game_id']
    send_dict['color'] = response['color']
    send_dict['player_status'] = 'existing'

    game = Game(ID = send_dict['game_id'])
    while connected:
        game.game_board.draw_board()
        moves = []
        attacked = True
        if send_dict['color']=='white':
            while attacked:
                print('Turn: white')
                print('Your move:')
                move =input()
                game, correct_move, event = game.make_move(move)
                os.system('cls')
                if correct_move:
                    moves.append(move)
                if isinstance(event,bool):
                    attacked = event
                if correct_move:
                    attacked = False
                else:
                    print('Wrong move!')
                game.game_board.draw_board()

            
            # print(game.board.draw_board())


            send_dict['move'] = moves
            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())
            print('Turn: black')
            print("Waiting for oponent's move")
            data = await reader.read(2048)
            data = json.loads(data.decode())
            print('Enemy move(s):',data['move'])
            if isinstance(data['move'], list):
                for move in data['move']:
                    game, _, _ = game.make_move(move)

        else:
            print('Turn: white')
            print("Waiting for oponent's move")
            data = await reader.read(2048)
            data = json.loads(data.decode())
            print('Enemy move(s):',data['move'])
            if isinstance(data['move'], list):
                for move in data['move']:
                    game, _, _ = game.make_move(move)
            
            game.game_board.draw_board()
            
            while attacked:
                print('Turn: black')
                print('Your move:')
                move =input()
                game, correct_move, event = game.make_move(move)
                os.system('cls')
                if correct_move:
                    moves.append(move)
                if correct_move:
                    attacked = False
                if isinstance(event,bool):
                    attacked = event
                else:
                    print('Wrong move!')
                game.game_board.draw_board()

            # print('Turn: black')
            # print('Your move')


            send_dict['move'] = moves
            # print(game.board.draw_board())

            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())


        if send_dict['msg'] == 'close':
            writer.close()
            client.close()
            connected = False





asyncio.run(wait_for_data())