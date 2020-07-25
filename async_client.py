import asyncio
import socket
import json
import pickle

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
        print(response)
        if response != 'Name already used!':
            incorrect_name = False
            send_dict['player_status'] = 'existing'
        else:
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

    while connected:
        
        # print(send_dict)
        print('board')
        
        if send_dict['color']=='white':
            print('Your move')
            send_dict['move'] = input('msg: ')
            print('board_updated')

            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())

            print("Waiting for oponent's move")
            data = await reader.read(2048)
            data = json.loads(data.decode())
            print('Enemy move:',data['move'])
        else:
            print("Waiting for oponent's move")
            data = await reader.read(2048)
            data = json.loads(data.decode())
            print('Enemy move:',data['move'])
            print('board_updated')
            print('Your move')
            send_dict['move'] = input('msg: ')
            print('board_updated')
            message = json.dumps(send_dict)
            loop.call_soon(client.send, message.encode())

        
        
        
        
        
        
        if send_dict['msg'] == 'close':
            writer.close()
            client.close()
            connected = False



        if send_dict['msg'] == 'close':
            writer.close()
            client.close()
            connected = False



asyncio.run(wait_for_data())