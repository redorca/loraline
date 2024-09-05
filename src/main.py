'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import os
import logging
import asyncio
import connections as conn
import platform
import json
import configparser as parse
import initialize


process_q = asyncio.Queue()
results_q = asyncio.Queue()
TARGET_USER = ""
TARGET_PASS = ""
dict_ref = {}

async def do_setup(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    data = await StreamReader.read(80)
    print(f'== 0 data \"{data.decode("UTF8")\"}')
    try:
        pack = json.loads(data.decode('UTF8'))
        print(f'=== 1')
        logging.warning("Decoded json")
    except json.JSONDecodeError as jde:
        logging.warning(jde)
        return
    if "TARGET_USER" in pack:
        TARGET_USER = pack["TARGET_USER"]
    if "TARGET_PASS" in pack:
        TARGET_PASS = pack["TARGET_PASS"]
    print(f'=== 9 TARGET_USER {TARGET_USER}, TARGET_PASS {TARGEWT_PASS}')
    if TARGET_USER != "" and TARGET_PASS != "":
        raise ConnectionRefusedError 

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

async def service(addr, port, handler=do_cmd):
    try:
        server = await asyncio.start_server(handler, addr, port)
        async with server:
            await server.serve_forever()
        return
    except ConnectionRefusedError as vle:
        server.close()
        await server.wait_closed()

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

async def debug_on(level):
        '''
        '''
        logging.basicConfig()
        asyncssh.set_log_level('DEBUG')
        asyncssh.set_debug_level(level)

async def mmain():
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

async def main():
    '''
        Read in config file.
    '''
    region = 'local'
    protocol = "ssh"
    params = await initialize.get_params(region)
    host = params["connect"]["Host"]
    port = params["connect"]["Port"]
    daemon_host = params["daemon"]["Host"]
    daemon_port = params["daemon"]["Port"]
    region = 'local'
    protocol = "ssh"
    user = os.getenv("TARGET_USER")
    pword = os.getenv("TARGET_PASS")
    print(f'user >>{user}<<, pass >>{pword}<<')
    if user is None or pword is None:
        await service(daemon_host, daemon_port, handler=do_setup)
        # print(' user or password, or both, are invalid.')
        # print(' Please set TARGET_USER to desired user,')
        # print(' and TARGET_PASS to the password.')
        # exit(1)
    uri = await initialize.build_uri(host, port, protocol, user, pword)
    remote = conn.Connection(uri)
    # await remote.debug_on(2)
    await remote.connect()

    await run_tasks(daemon_host, daemon_port, process_q, results_q, remote)

asyncio.run(main())
