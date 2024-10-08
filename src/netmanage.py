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

from loglady import logg
import initialize
from cmds   import commands
import socket
import asyncio
import sys

blog = logg.DasLog('netmanage')

def client(host, port, cmd):
    '''
        establish a connection to the service that writes a user specified command
        and receives all the dataa speicified.
    '''

    blog.info(f'client on host {host}, and port {port}')
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((host, int(port)))
        sock.send(cmd)
        data = sock.recv(512)
        blog.info(f'returned data {data}')

async def main():
    '''
    '''
    # connect_type = 'remote'
    connect_type = 'local'
    try:
        if len(sys.argv) > 1 and not sys.argv[1] in commands.lora_cmds:
            print(f"This command '{sys.argv[1]}' is unrecognized.")
            # return
        if len(sys.argv) > 2 and not sys.argv[2] in commands.lora_cmds[sys.argv[1]]:
            print(f'Incorrect subcommand \"{sys.argv[2]}\" of {sys.argv[1]}')
            # return
    except KeyError as keye:
        print(f'{keye}')

    cmd_string = ' '.join(sys.argv[1:])
    print(f'cmd string:: {cmd_string}')
    # host, port = await initialize.get_params(connect_type)
    params = await initialize.get_params(connect_type)
    host = params["daemon"]["Host"]
    port = params["daemon"]["Port"]
    try:
        client(host, port, bytes(cmd_string.encode('UTF8')))
    except ConnectionRefusedError as cre:
        print('The request handling service may not be running.')
        print(f'== {cre}')
    exit()
    if connect_type == "remote":
        client(host, port, bytes(cmd_string.encode('UTF8')))
    else:
        client(host, port, bytes('ls -l'.encode('UTF8')))

asyncio.run(main())
