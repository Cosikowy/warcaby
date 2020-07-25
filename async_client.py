import asyncio
import socket
import json
import pickle

async def wait_for_data():
    loop = asyncio.get_running_loop()


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost',5000))

    reader, writer = await asyncio.open_connection(sock=client)
    
    connected = True
    name = input('name: ')
    # game_state = 'Game State v1'
    while connected:
        print('board')
        print('Your move')
        msg = input('msg: ')
        print('board_updated')
        send_dict = {
            'name':name,
            'msg':msg
            }
        message = json.dumps(send_dict)
        loop.call_soon(client.send, message.encode())

        print("Waiting for oponent's move")
        data = await reader.read(2048)
        # print(game_state)

        # print("Oponent's move:", data.decode())
        # loop.call_soon(client.send, 'sync'.encode())
        if send_dict['msg'] == 'close':
            writer.close()
            client.close()
            connected = False
        else:
            sync = await reader.read(2048)
        
        print('board_synced, data recived 1st turn:', data)
        print("Oponent's move:", sync.decode())

        # loop.call_soon(client.send, 'awaiting'.encode())
        # awaiting = await reader.read(2048)
        
        if msg == 'close':
            writer.close()
            client.close()
            connected = False



asyncio.run(wait_for_data())