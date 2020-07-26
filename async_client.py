import asyncio
import socket
import json
import pickle
from game import Game
import os
import pprint

async def run_game():
    loop = asyncio.get_running_loop()
    send_dict = {
            'name':'',
            'msg':'',
            'game_id': '',
            'player_status':'new',
            'game_status':'',
            'command':'',
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
        if response != 'Name already used!':
            incorrect_name = False
            send_dict['player_status'] = 'existing'
        else:
            print('Name already in use!')
            send_dict['name'] = input('name: ')
    
    while True:                                         # Used to maintain connection between client and server 
        send_dict['command'] = ''
        print('NEW GAME | CURRENTLY PLAYING | HISTORY | GAMES')
        command = input('').lower()
        msg = json.dumps(send_dict)
        if command == 'new game':                       # Starting new game
            send_dict['command'] = 'new game'
            msg = json.dumps(send_dict)
            writer.write(msg.encode())
            await writer.drain()
            response = await reader.read(2048)
            response = response.decode()
            print(response)
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
                os.system('cls')
                moves = []
                attacked = True
                
                if send_dict['color']=='white':                 # Logic for white stones
                    game.game_board.draw_board()

                    while attacked:
                        print('Turn: white')
                        print('Your move:')
                        move =input()
                        game, correct_move, event = game.make_move(move)
                        
                        if correct_move:
                            moves.append(move)

                        if isinstance(event,bool):
                            attacked = event

                        if correct_move:
                            attacked = False
                        else:
                            print('Wrong move!')
                        os.system('cls')
                        game.game_board.draw_board()

                    send_dict['move'] = moves
                    if event == 'white' or event == 'black':
                        send_dict['game_status'] = f'finished, winner {event}'
                        
                    message = json.dumps(send_dict)
                    loop.call_soon(client.send, message.encode())
                    if 'finished' in send_dict['game_status']:
                        print('Game is ', send_dict['game_status'])
                        writer.close()
                        connected = False
                        break

                    print('Turn: black')
                    print("Waiting for oponent's move")
                    data = await reader.read(2048)
                    data = json.loads(data.decode())
                    if 'finished' in data['game_status']:
                        print('Game is ', data['game_status'])
                        writer.close()
                        connected = False
                        break

                    print('Enemy move(s):',data['move'])
                    if isinstance(data['move'], list):
                        for move in data['move']:
                            game, _, _ = game.make_move(move)
                    
                else:                                           # Logic for black stones
                    game.game_board.draw_board()
                    print('Turn: white')
                    print("Waiting for oponent's move")
                    data = await reader.read(2048)
                    data = json.loads(data.decode())
                    os.system('cls')
                    if 'finished' in data['game_status']:
                        print('Game is ', data['game_status'])
                        writer.close()
                        connected = False
                        break

                    print('Enemy move(s):',data['move'])
                    if isinstance(data['move'], list):
                        for move in data['move']:
                            game, _, _ = game.make_move(move)
                    
                    game.game_board.draw_board()
                    
                    while attacked:
                        print('Turn: black')
                        print('Your move:')
                        move = input()
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

                        os.system('cls')
                        game.game_board.draw_board()
                    
                    if event == 'white' or event == 'black':
                        send_dict['game_status'] = f'finished, winner {event}'

                    send_dict['move'] = moves
                    message = json.dumps(send_dict)
                    loop.call_soon(client.send, message.encode())
                    if 'finished' in send_dict['game_status']:
                        print('Game is ', send_dict['game_status'])
                        writer.close()
                        connected = False
                        break
                    
        elif command == 'currently playing':                         # Requesting list of currently playing players 
            send_dict['command'] = 'currently playing'
            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())
            data = await reader.read(2048*2)
            data = data.decode()
            pprint.pprint(data)
            input()
        
        elif command == 'history':                                   # Requesting games history
            send_dict['command'] = 'history'
            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())
            data = await reader.read(2048*2)
            data = json.loads(data.decode())
            pprint.pprint(data)
            input()
        
        elif command == 'games':                                     # Requesting current games in progress
            send_dict['command'] = 'games'
            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())
            data = await reader.read(2048*2)
            data = data.decode()
            pprint.pprint(data)
            input()



asyncio.run(run_game())