import asyncio
import socket
import json

async def wait_for_data():
    loop = asyncio.get_running_loop()


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost',5000))

    reader, writer = await asyncio.open_connection(sock=client)
    
    connected = True
    name = input('name: ')
    while connected:
        msg = input('msg: ')

        send_dict = {
            'name':name,
            'msg':msg
            }
        message = json.dumps(send_dict)
        loop.call_soon(client.send, message.encode())

        data = await reader.read(2048)

        if send_dict['msg'] == 'close':
            writer.close()
            client.close()
            connected = False
        else:
            data = await reader.read(2048)

        print("Received:", data.decode())
        if msg == 'close':
            writer.close()
            client.close()
            connected = False



asyncio.run(wait_for_data())