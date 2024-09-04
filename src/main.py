'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import os
from loglady import logg
import logging
import asyncio
import connections as conn
import platform
import json
import configparser as parse
import initialize


blog = logg.DasLog()
blob.level = logging.DEBUG
blog.info(f'blogging level is {blog.get_level()}')
process_q = asyncio.Queue()
results_q = asyncio.Queue()
TARGET_USER = ""
TARGET_PASS = ""
dict_ref = {}

async def do_cmd(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    # logging.warning(f"== {process_q.qsize()} ==")
    data = await StreamReader.read(300)
    if TARGET_USER == "" or TARGET_PASS == "":
        if Creds not in data:
            logging.warning("Waiting for a Creds packet")
            return
        try:
            creds = json.loads(data)
            TARGET_USER = creds["TARGET_USER"]
            TARGET_PASS = creds["TARGET_PASS"]
        except JSONDecodeError as jde:
            logging.warning(f"unable to decode {data}")
        finally:
            return

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
        while TARGET_USER == "" or TARGET_PASS == "":
            logging.warning(f"TARGET_USER {TARGET_USER}, TARGET_PASS {TARGET_PASS}")
            await asyncio.sleep(5)

        tasks.append(tg.create_task(connxion.run(q_cmds, q_returns)))
        await asyncio.gather(*tasks)
    return

async def buoy():
    while True:
        await asyncio.sleep(5)
        # logging.warning(",,,,,,")

async def debug_on(level):
        '''
        '''
        logging.basicConfig()
        asyncssh.set_log_level('DEBUG')
        asyncssh.set_debug_level(level)

async def main():
    '''
        Read in config file.
    '''
    region = 'local'
    protocol = "ssh"
    await debug_on(2)
    params = await initialize.get_params(region)
    host = params["connect"]["Host"]
    port = params["connect"]["Port"]
    daemon_host = params["daemon"]["Host"]
    daemon_port = params["daemon"]["Port"]
    # uri = await initialize.build_uri(host, port, protocol, user, pword)
    # await remote.debug_on(2)
    logging.warning(f"params in place.")
    exit(1)
    await run_tasks(daemon_host, daemon_port, process_q, results_q, remote)

async def mmain():
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
# 
#     params = await initialize.get_params(region)
#     host = params["connect"]["Host"]
#     port = params["connect"]["Port"]
#     uri = await initialize.build_uri(host, port, protocol, user, pword)
#     remote = conn.Connection(uri)
#     # await remote.debug_on(2)
#     await remote.connect()
#     daemon_host = params["daemon"]["Host"]
#     daemon_port = params["daemon"]["Port"]
# 
