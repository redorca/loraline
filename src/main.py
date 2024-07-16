'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import asyncio
from collections import deque
import platform
import configparser as parse
import initialize


async def do_cmd(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    print(f'=======')
    data = await StreamReader.read(300)
    process_q.append(str(data))
    print(f'received {data} queue {process_q}')
    StreamWriter.write(b'done')


async def main():
    '''
        Read in config file.
    '''
    host, addr, port = await initialize.set_params()
    server = await asyncio.start_server(do_cmd, addr, port)
    async with server:
        await server.serve_forever()


process_q = deque()
asyncio.run(main())

