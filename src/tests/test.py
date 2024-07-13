'''
'''

import asyncio
import connections as conn

async def frup():
    '''
    '''
    foo = conn.Connection('ssh://localhost:22,wings,Venus&Mars')
    # foo = conn.Connection('serial:/dev/ttyS0')
    return foo

async def roo():
    '''
        connect to the self identified host. An SSHClientConnection object is returned.
    '''
    whole = str()
    client = await  frup()
    connection = await client.connect()
    channelW, channelR, channelEr = await client.make_channel('ls -l')
    # buff = await channelR.read(50)
    buff = await channelR.readline()
    while channelR.at_eof() is False:
        whole += buff
        buff = await channelR.readline()

    whole += buff
    print(f"read in {whole}")

asyncio.run(roo())
