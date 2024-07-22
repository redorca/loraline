'''
'''

import sys
import asyncio
import connections as conn
import initialize

async def connect(uri):
    '''
        Establish an authenticated connection for later use.
        For ssh uri's returns an SSHClient object from asyncssh
        # foo = conn.Connection('ssh://localhost:22,wings,Venus&Mars')
        # foo = conn.Connection('ssh://localhost:22,rock,lobster')
        # foo = conn.Connection('ssh://switchboard.loraline.net:8022,$admin,as')
    '''
    try:
        foo = conn.Connection(uri)
        connection = await foo.connect()
    except ValueError as val:
        print(f'{val}')
        exit(1)

    return foo, connection

async def boo(client, cmd):
    '''
        Open a channel to the self identified host. An SSHClientConnection object is returned.
    '''
    whole = str()
    channelW, channelR, channelEr = await client.make_channel(cmd)
    buff = await channelR.readline()
    while channelR.at_eof() is False:
        whole += buff
        buff = await channelR.readline()

    whole += buff
    return whole

def build_uri(host, port, protocol, username, password):
    elements = ":".join([protocol, ''.join(["//", host]), port])
    uri = ",".join([elements, username, password])
    return uri

if __name__ == "__main__":
    async def main():
        '''
            pass through command line commands
        '''
        region = 'local'

        if len(sys.argv) > 1:
            cmd = [ " ".join(sys.argv[1:]) ]
        else:
            print('  No commands passed in, now\'s the time to exit')
            raise ValueError

        host, port = await initialize.get_params(region)
        uri = await initialize.build_uri(host, port, "ssh", "rock", "lobster")
        client, connection = await connect(uri)
        if type(client) is None:
            print(f'error error error: No connection made.')
            exit(1)
        for entry in cmd:
            results = await client.issue(entry)
            print(f'{results}')
    try:
        asyncio.run(main())
    except ValueError as val:
        print(f'{val}')

