#!/usr/bin/env python
# coding: utf-8

# In[2]:


import asyncio, asyncssh
import sys, os, time

class MySSHClientSession(asyncssh.SSHClientSession):

    def __init__(self):
#         print('init session')
        pass

    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        global from_lora
        print(f'{data}', end='')
        from_lora = data

    def write(self, msg: str) -> None:
        print("in write")
        print('to device ['+msg.strip()+']') # debug
        from_lora = ""
        try:
            ret = self.stdout.write(msg) # need to get rid of return value
        except:    # seems like a connection went down
            pass


class MySSHClient(asyncssh.SSHClient):

    def __init__(self):
#         print('init client')
        pass

    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print(f'Connection made to server IP {conn.get_extra_info("peername")[0]}')
        self._conn = conn
        self._username = conn.get_extra_info('peername')[0]

    def auth_completed(self) -> None:
#         print('Authentication successful.')
        pass


async def lora_answer(timeout) -> str:
    global from_lora
    #print("in lora_answer")
    from_lora = ""
    start_time = asyncio.get_event_loop().time()
    while from_lora == "":
        if asyncio.get_event_loop().time() - start_time > timeout:
            return False  # Return False if timeout is reached
        await asyncio.sleep(0.1)  # Check every 0.1 seconds
    return True  # Return True if variable changes


async def runCommands(chan):
    if "Palo Alto" in site:
        adminID = 6
        online = "1 3 4 5 6 11 23 24 "
    elif "Sonoma" in site:
        adminID = 20
        online = "2 20 21 22 100 101 102 103 104 105 106 107 108 109 110 "
    devices = online.split()
    #await asyncio.sleep(15)          # wait for initial login message
    for device in devices:
        lora = f'#{adminID} get new map from {device}'
        print(lora)
        chan.write(lora + '\n')
        await lora_answer(15)    # 15 second timeout
        """
        lora = f"#{adminID} get online from 6"
        chan.write(lora + '\n')
        await lora_answer(15)
        """
        await lora_answer(30)    # wait for any final responses to arrive


async def waitwait(time):
    await asyncio.sleep(time)     # end 10 seconds later


async def main():
    if sys.platform == 'win32':
        port = 8022; server = 'switchboard.saal.org'; key_path = 'C:/Users/'+os.getlogin()
    else:      # suppose we are linux
        # port = 8022; server = 'localhost'; key_path = '/home/' + os.getlogin()
        port = 8022; server = 'localhost'; key_path = os.getenv('HOME')
    os.chdir(key_path + '/OTA' )
    # port = 22
#     print(port, server, key_path, os.getcwd())
    # Create a connection
    conn, client = await asyncssh.create_connection(MySSHClient,
            server, port = port, username = os.getenv('TARGET_USER'), password = os.getenv('TARGET_PASS'), known_hosts=None)
#     print('connected')
    chan, session = await conn.create_session(MySSHClientSession)
    print('session made')
    await lora_answer(15)    # 15 second timeout
    while not "connected" in from_lora:
        await asyncio.sleep(1)
    await runCommands(chan)
    print('Done...')
    await asyncio.sleep(5)            # wait before final completion
    #asyncio.get_event_loop().stop()
    return

    chan.close()            # Close the session
    print('channel closed')
    conn.close()           # Close the connection
    print('connection closed')
    print('Done...')
    asyncio.get_event_loop().stop()  # Stop the event loop

site = "Palo Alto"
site = "Sonoma"
from_lora = ""
if sys.platform == 'win32':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
else:
    asyncio.run(main())
    waitwait(10)
