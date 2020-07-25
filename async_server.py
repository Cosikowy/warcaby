import asyncio
import json
import ast
import pickle


async def handle_connection(reader, writer):
    global players
    
    while True:

        data = await reader.read(2048)
        # data2 = data
        message = data.decode()

        msg_json = json.loads(message)
        addr = writer.get_extra_info('peername')

        print(f"Received {msg_json['name']} from {addr}")
        print(f"Received {msg_json['msg']} from {addr}")

        players[msg_json['name']] = writer


        print(f"Send: {message!r}")
        for player in players.keys():
            if player!=msg_json['name']:
                writer2 = players[player]
                writer2.write(data)                 # Ta część jest jak będzie już 2 graczy w lobby
                await writer2.drain()
            if msg_json['msg']=='close':
                writer2 = players[player]
                writer2.write(data)
                await writer2.drain()
        
        # sync = await reader.read(2048)
        # sync = sync.decode()
        writer.write(data)
        await writer.drain()


        if message == '':
            print("Connection lost")
            writer.close()

        if msg_json['msg'] == 'close':
            print("Close the connection")
            writer.close()


players = {}
async def main():
    server = await asyncio.start_server(
        handle_connection, '127.0.0.1', 5000)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())