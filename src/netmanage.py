'''
    A command line tool to comunicate with the netmanage service the commands
    dictated by the user.
'''
'''
# import argparse
# import json
#
# cli = argparse.ArgumentParser()
# cli.add_argument('--one', default="")
# cli.add_argument('--two', default="")
# cli.add_argument("cmd", nargs=argparse.REMAINDER)
#
# cmds = ''
# goo = ''
# foof = cli.parse_args()
# if len(foof.one) + len(foof.two) == 0:
#     if len(foof.cmd) != 0:
#         cmds = ' '.join(foof.cmd)
#         stuff = { "action": "lora", "cmds": cmds }
#         goo = json.dumps(stuff)
# elif len(foof.one) * len(foof.two) == 0:
#     print("You need to specify the user name and the password as arguments, not one or the other")
# else:
#     stuff = { "action": "setup", "TARGET_USER": foof.one, "TARGET_PASS": foof.two }
#     goo = json.dumps(stuff)
#
# print(f'   Packet:: >>{goo}<<')
'''
'''
'''
'''
'''

import argparse
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
    setup = argparse.ArgumentParser()
    setup.add_argument('--user')
    setup.add_argument('--pass')
    setup.add_argument('cmd', argparse.REMAINDER)
    stuff = setup.parse_args()
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
