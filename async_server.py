import asyncio
import json
import ast
import pickle
import random
import datetime


class Server:
    players = {}
    queue = []
    lobby = {}
    games = {}
    def __init__(self):
        asyncio.run(self.main())
    
    async def main(self):
        self.server = await asyncio.start_server(
            self.handle_connection, '0.0.0.0', 5000,
            reuse_address=True)

        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with self.server:
            await self.server.serve_forever()

    async def response_to_player(self, name, response):
        writer = self.players[name]
        print('response to:',name)
        if isinstance(response, dict):
            return_msg = json.dumps(response).encode()
        else:
            try:    
                return_msg = response.encode()
            except:
                return_msg = response
        writer.write(return_msg)
        await writer.drain()

    async def read_data(self, reader_obj):
        data = await reader.read(2048)
        message = data.decode()
        try:
            msg_json = json.loads(message)
        except:
            msg_json = message
        return msg_json

    async def handle_connection(self, reader, writer):
        self.running_games = set()
        response = {
            'move':'',
            'game_id':'',
            'game_status':'',
            'color':'white',
            'turn':'w',
        }
        
        incorrect_name = True
        while True:
            data = await reader.read(2048)
            message = data.decode()
            msg_json = json.loads(message)
            while incorrect_name:
                if msg_json['player_status']!='existing':
                    if (msg_json['player_status'] == 'new' and 
                       msg_json['name'] not in self.players.keys()):
                        self.players[msg_json['name']] = writer
                        incorrect_name = False
                        return_msg = 'ok'.encode()
                        writer.write(return_msg)
                        await writer.drain()
                    elif (msg_json['player_status'] == 'new' and 
                         msg_json['name'] in self.players.keys()):
                        print('naming went wrong')
                        return_msg = 'Name already used!'.encode()
                        writer.write(return_msg)
                        await writer.drain()
                        data = await reader.read(2048)
                        message = data.decode()
                        msg_json = json.loads(message)
                    elif msg_json['player_status'] == 'exist':
                        incorrect_name = False
            
            if msg_json['name'] not in self.players.keys():
                self.players[msg_json['name']] = writer

            if msg_json['command'] == 'new game':
                self.response_to_player(msg_json['name'], {'msg': 'ok'})
                if msg_json['game_id']=='':
                    print('game_creation')
                    self.queue.append(msg_json['name'])
                    if len(self.queue)==2:
                        game_id = random.randint(1000,9999)
                        not_valid = True
                        while not_valid:
                            if game_id in self.running_games:
                                game_id = random.randint(1000,9999)
                            else:
                                not_valid = False
                        self.running_games.add(game_id)
                        response['game_id'] = game_id
                        self.lobby[game_id] = [x for x in self.queue]
                        self.queue.clear()
                        print(self.lobby)
                        
                        player_one = self.lobby[game_id][0]
                        player_two = self.lobby[game_id][1]
                        self.games[game_id] = {
                            'players':(player_one, player_two),
                            'game_id': game_id,
                            'started': datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'),
                            'status': 'ongoing/tie'
                        }
                        await self.response_to_player(player_one, response)
                        response_p2 = response
                        response_p2['color'] = 'black'
                        await self.response_to_player(player_two, response_p2)

                    else:
                        return_msg = 'wait'.encode()
                        writer.write(return_msg)
                        await writer.drain()
                    print('game created')

                elif msg_json['game_id']!='':
                    finished = False
                    player_one = self.lobby[msg_json['game_id']][0]
                    player_two = self.lobby[msg_json['game_id']][1]
                    
                    addr = writer.get_extra_info('peername')
                    print(f"Received {msg_json} from {msg_json['msg']} - {addr}")
                    response['move'] = msg_json['move']
                    print(f"Send: {response}")
                    if 'finished' in msg_json['game_status']:
                        response['game_status'] = msg_json['game_status']
                        finished = True

                    response = json.dumps(response).encode()
                    self.games[msg_json['game_id']]['last move'] = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
                    
                    if finished:
                        self.games[msg_json['game_id']]['status'] = 'finished'
                        self.running_games.discard(msg_json['game_id'])
                        self.lobby.pop(msg_json['game_id'], None)
                        self.players.pop(player_one, None)
                        self.players.pop(player_two, None)
                    if msg_json['color']=='white':
                        await self.response_to_player(player_two, response)
                    else:
                        await self.response_to_player(player_one, response)

                    response = json.loads(response.decode())

                if message == '':
                    print("Connection lost")
                    writer.close()

                if msg_json['msg'] == 'close':
                    print("Close the connection")
                    writer.close()
            elif msg_json['command'] == 'history':
                history = self.games
                await self.response_to_player(msg_json['name'], history)             
            
            elif msg_json['command'] == 'currently playing':
                curr_players = str([', '.join(x for x in self.players.keys())])
                await self.response_to_player(msg_json['name'], curr_players)

            elif msg_json['command'] == 'games':
                games = self.games
                games = str([', '.join(x for x in self.games)])
                await self.response_to_player(msg_json['name'], games)

Server()