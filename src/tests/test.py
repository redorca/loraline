'''
'''

import asyncio
import connections as conn

async def connect():
    '''
        Establish an authenticated connection for later use.
        Returns an SSHClient object from asyncssh
    '''
    foo = conn.Connection('ssh://localhost:22,wings,Venus&Mars')
    connection = await foo.connect()
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

async def main():
    client, connection = await connect()
    cmd = ['ls -l', 'find Documents']
    for entry in cmd:
        results = await client.issue(entry)
        print(f'{results}')

asyncio.run(main())
