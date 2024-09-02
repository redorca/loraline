'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import os
from loglady import logg
import logging
import asyncio
import connections as conn
import platform
import configparser as parse
import initialize


# blog = logg.DasLog()
# blog.info(f'blogging level is {blog.get_level()}')
process_q = asyncio.Queue()
results_q = asyncio.Queue()

async def do_cmd(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    # logging.warning(f"== {process_q.qsize()} ==")
    data = await StreamReader.read(300)
    process_q.put_nowait(data.decode('UTF8'))
    # logging.warning(f'== data {type(data)} {data}')
    StreamWriter.write(data)
    buff = await results_q.get()
    StreamWriter.write(buff)

async def service(addr, port):
    server = await asyncio.start_server(do_cmd, addr, port)
    async with server:
        await server.serve_forever()
    return

async def run_tasks(ahost, aport, q_cmds, q_returns, connxion):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        # Create the local cli listener
        tasks.append(tg.create_task(service(ahost, aport)))
        tasks.append(tg.create_task(buoy()))
        # Create the ssh command pipes
        tasks.append(tg.create_task(connxion.run(q_cmds, q_returns)))
        await asyncio.gather(*tasks)
    return

async def buoy():
    while True:
        await asyncio.sleep(5)
        # logging.warning(",,,,,,")

async def main():
    '''
        Read in config file.
    '''
    region = 'local'
    protocol = "ssh"
    user = os.getenv("TARGET_USER")
    pword = os.getenv("TARGET_PASS")
    if user is None or pword is None:
        print(' user or password, or both, are invalid.')
        print(' Please set TARGET_USER to desired user,')
        print(' and TARGET_PASS to the password.')
        exit(1)
    params = await initialize.get_params(region)
    host = params["connect"]["Host"]
    port = params["connect"]["Port"]
    uri = await initialize.build_uri(host, port, protocol, user, pword)
    remote = conn.Connection(uri)
    # await remote.debug_on(2)
    await remote.connect()
    daemon_host = params["daemon"]["Host"]
    daemon_port = params["daemon"]["Port"]

    await run_tasks(daemon_host, daemon_port, process_q, results_q, remote)

asyncio.run(main())
