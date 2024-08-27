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
    data = await StreamReader.read(300)
    process_q.append(str(data))
    StreamWriter.write(b'done')

async def service(addr, port):
    server = await asyncio.start_server(do_cmd, addr, port)
    async with server:
        await server.serve_forever()
    return

async def run_tasks(ahost, aport, q_cmds, q_returns, connxion):
    async with asyncio.TaskGroup() as tg:
        # Create the local cli listener
        tasks.append(tg.create_task(service(ahost, aport)))
        tasks.append(tg.create_task(bouy()))
        # Create the ssh command pipes
        tasks = tasks.append(tg.create_task(connxion.run(q_cmds, q_returns)))
        await asyncio.gather(*tasks)
    return

async def bouy():
    while True:
        await asyncio.sleep(5)
        print(",,,,,,")

async def main():
    '''
        Read in config file.
    '''
    region = 'local'
    protocol = "ssh"
    user = "wings"
    pword = "mccartney"
    # uri = await initialize.build_uri(host, port, protocol, user, pword)
    host, port = await initialize.get_params(region)
    uri = await initialize.build_uri(host, port, "ssh", "wings", "mccartney")
    print(f'uri turns out to be {uri}')
    remote = conn.Connection(uri)
    await remote.connect()
    await run_tasks(host, port, process_q, results_q, remote)

asyncio.run(main())
