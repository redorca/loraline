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


blog = logg.DasLog()
blog.info(f'blogging level is {blog.get_level()}')

async def do_cmd(StreamReader, StreamWriter):
    '''
        Wait for input in preparation for queueing a command that
        a command pipe will process.
    '''
    blog.info('=======')
    data = await StreamReader.read(300)
    process_q.append(str(data))
    blog.info(f'received {data} queue {process_q}')
    StreamWriter.write(b'done')

async def service(addr, port):
    server = await asyncio.start_server(do_cmd, addr, port)
    async with server:
        await server.serve_forever()
    return

async def run_tasks(ahost, aport):
    blog.info(f'running tasks on {ahost} and port {aport}')
    async with asyncio.TaskGroup() as tg:
        tg.create_task(service(ahost, aport))


    return

async def main():
    '''
        Read in config file.
    '''
    host, addr, port = await initialize.set_params()
    await run_tasks(addr, port)

process_q = deque()
asyncio.run(main())

#       client, connection = await connect(host)

#       cmd = ['ls -l', 'find Documents']
#       for entry in cmd:
#           results = await client.issue(entry)
#           print(f'{results}')
