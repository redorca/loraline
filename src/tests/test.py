'''
'''

import asyncio
import connections as conn

async def frup():
    # foo = conn.Connection('ssh:foo.com:me,free')
    foo = conn.Connection('serial:/dev/ttyS0')
    return foo

async def roo():
    connect = await  frup()
    await connect.connect()

asyncio.run(roo())
