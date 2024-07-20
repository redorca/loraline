'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

from loglady import logg
import asyncio
import connections as conn
from collections import deque
import platform
import configparser as parse
import initialize


# blog = logg.DasLog()
# blog.info(f'blogging level is {blog.get_level()}')
process_q = deque()
results_q = deque()

async def do_cmd(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    print('=======')
    data = await StreamReader.read(300)
    process_q.append(str(data))
    print(f'received {data} queue {process_q}')
    StreamWriter.write(b'done')

async def service(addr, port):
    server = await asyncio.start_server(do_cmd, addr, port)
    async with server:
        await server.serve_forever()
    return

async def run_tasks(ahost, aport, q_cmds, q_returns, connxion):
    print(f'running tasks on {ahost} and port {aport}')
    async with asyncio.TaskGroup() as tg:
        # Create the local cli listener
        tg.create_task(service(ahost, aport))
        tg.create_task(bouy())
        # Create the ssh command pipes
        tg.create_task(connxion.run(q_cmds, q_returns))
        # tg.create_task(connxion.run(process_q))
        # tg.create_task(connxion.run(process_q))

    return

async def bouy():
    while True:
        await asyncio.sleep(5)
        print(",,,,,,")

async def main():
    '''
        Read in config file.
    '''
    # connect_type = 'remote'
    connect_type = 'local'
    host, port = await initialize.get_params(connect_type)
    part1 = ':'.join(["ssh", ''.join(['//', host]), port])
    part = ','.join([part1, "rock", "lobster"])
    print(f'part {part}')
    remote = conn.Connection(part)
    await remote.connect()
    await run_tasks(host, port, process_q, results_q, remote)

asyncio.run(main())
# async def run_tasks(ahost, aport, passw='Venus&Mars', uname='rock'):
