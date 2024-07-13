'''
'''

import asyncio
import connections as conn

async def frup():
    '''
    '''
    foo = conn.Connection('ssh:localhost:wings,Venus&Mars')
    # foo = conn.Connection('serial:/dev/ttyS0')
    return foo

async def roo():
    '''
        connect to the self identified host. An SSHClientConnection object is returned.
    '''
    connection = await  frup()
    channel = await connection.connect()

asyncio.run(roo())
