'''
'''

import asyncio
import connections as conn
import initialize

async def connect(host):
    '''
        Establish an authenticated connection for later use.
        Returns an SSHClient object from asyncssh
    '''
    # foo = conn.Connection('ssh://localhost:22,wings,Venus&Mars')
    target = ''.join(['ssh://', host, ':22,wings,Venus&Mars'])
    print(f'set target: {target}')
    foo = conn.Connection(target)
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

if __name__ == "__main__":
    async def main():
        host, addr, port = await initialize.set_params()
        client, connection = await connect(host)
        cmd = ['ls -l', 'find Documents']
        for entry in cmd:
            results = await client.issue(entry)
            print(f'{results}')

    asyncio.run(main())
