import asyncio
import json
import ast
import pickle
import random



# async def handle_connection(reader, writer):
#     global players
    
#     while True:

#         data = await reader.read(2048)
#         # data2 = data
#         message = data.decode()

#         msg_json = json.loads(message)
#         players[msg_json['name']] = writer
#         addr = writer.get_extra_info('peername')

#         print(f"Received {msg_json['msg']} from {msg_json['name']}   - {addr}")
#         print(f"Send: {message}")

        

#         for player in players.keys():
#             if player!=msg_json['name']:
#                 writer2 = players[player]
#                 writer2.write(data)                 # Ta część jest jak będzie już 2 graczy w lobby
#                 await writer2.drain()
#             if msg_json['msg']=='close':
#                 writer2 = players[player]
#                 writer2.write(data)
#                 await writer2.drain()

#         writer.write(data)
#         await writer.drain()


#         if message == '':
#             print("Connection lost")
#             writer.close()

#         if msg_json['msg'] == 'close':
#             print("Close the connection")
#             writer.close()


# players = {}
# async def main():
#     server = await asyncio.start_server(
#         handle_connection, '127.0.0.1', 5000)

#     addr = server.sockets[0].getsockname()
#     print(f'Serving on {addr}')

#     async with server:
#         await server.serve_forever()

# asyncio.run(main())


class Server:
    players = {}
    queue = []
    lobby = {}
    def __init__(self):
        asyncio.run(self.main())
    
    async def main(self):
        self.server = await asyncio.start_server(
            self.handle_connection, '127.0.0.1', 5000,
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

    def check_names(self, name):
        if name in players.keys():
            return True 
        else:
            return False

    async def handle_connection(self, reader, writer):
        self.running_games = set()
        response = {
            'move':'',
            'game_id':'',
            'game_status':'',
            'color':'white'
        }
        
        incorrect_name = True
        while True:
            data = await reader.read(2048)
            message = data.decode()
            msg_json = json.loads(message)
            
            print('ping')
            while incorrect_name:
                if msg_json['player_status']!='existing':
                    if msg_json['player_status'] == 'new' and msg_json['name'] not in self.players.keys():
                        self.players[msg_json['name']] = writer
                        incorrect_name = False
                    elif msg_json['player_status'] == 'new' and msg_json['name'] in self.players.keys():
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
                    response['game_id'] = game_id
                    self.lobby[game_id] = [x for x in self.queue]
                    self.queue.clear()
                    print(self.lobby)
                    
                    player_one = self.lobby[game_id][0]
                    player_two = self.lobby[game_id][1]
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
                player_one = self.lobby[msg_json['game_id']][0]
                player_two = self.lobby[msg_json['game_id']][1]
                
                print('ping2')

                addr = writer.get_extra_info('peername')
                print(f"Received {msg_json} from {msg_json['msg']} - {addr}")
                response['move'] = msg_json['move']
                print(f"Send: {response}")
                
                response = json.dumps(response).encode()
                
                if msg_json['color']=='white':
                    await self.response_to_player(player_two, response)
                else:
                    await self.response_to_player(player_one, response)

                # writer.write(response)
                # await writer.drain()
                response = json.loads(response.decode())




            if message == '':
                print("Connection lost")
                writer.close()

            if msg_json['msg'] == 'close':
                print("Close the connection")
                writer.close()

Server()