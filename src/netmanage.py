'''
    A command line tool to comunicate with the netmanage service the commands
    dictated by the user.
'''
'''
'''
'''
'''
'''
'''

import initialize
from cmds   import commands
import socket
import asyncio
import sys
import os

def client(host, port, cmd):
    '''
        establish a connection to the service that writes a user specified command
        and receives all the dataa speicified.
    '''

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((host, int(port)))
        sock.send(cmd)
        buff = sock.recv(512)
        #
        # Throw away first line because it's the shell echoing back the command
        buff = b""
        while len(data := sock.recv(512)) == 512:
            buff += data.strip()
            # print(f'length of data {len(data)}')
        buff += data.strip()
        print(f'{buff.decode("UTF8")}')


async def main():
    '''
    '''
    # connect_type = 'remote'
    connect_type = 'local'

    params = await initialize.get_params(connect_type)
    host = params["daemon"]["Host"]
    port = params["daemon"]["Port"]

    cmd_string = ' '.join(sys.argv[1:])

    try:
        client(host, port, bytes(cmd_string.encode('UTF8')))
    except ConnectionRefusedError as cre:
        print('The request handling service may not be running.')
        print(f'== {cre}')

asyncio.run(main())
