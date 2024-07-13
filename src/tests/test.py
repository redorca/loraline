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
    client = await  frup()
    connection = await client.connect()
    channel = await client.make_channel()

asyncio.run(roo())
