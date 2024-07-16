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
import cmds.commands
import socket
import asyncio
import sys

def client(host, address, port, cmd):
    '''
        establish a connection to the service that writes a user specified command
        and receives all the dataa speicified.
    '''

    print(f'client on host {host}, address {address}, and port {port}')
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.connect((address, int(port)))
        sock.send(cmd)
        data = sock.recv(512)
        print(f'returned data {data}')

async def main():
    if len(sys.argv) > 1 and not sys.argv[1] in cmds.commands.lora_cmds:
        print(f"This command '{sys.argv[1]}' is unrecognized.")
        return
    cmd_string = ' '.join(sys.argv[1:])
    print(f'cmd string:: {cmd_string}')
    host, address, port = await initialize.set_params()
    client(host, address, port, bytes(cmd_string.encode('UTF8')))

asyncio.run(main())
