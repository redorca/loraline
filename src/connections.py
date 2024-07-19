'''
    Manage connections to the network either through ssh or serial, for the moment.
'''

import asyncio, asyncssh, sys
from collections import deque
from loglady import logg

xlog = logg.DasLog()
results_q = deque()

class Connection():
    '''
        Address is of the form <protocol>://<path to endpoint>[:<port to use>][<,user,password>]
        so a serial connection would be serial:///dev/ttySx and an ssh connection
        would be ssh:<URI>:user:password
    '''
    def __init__(self, uri):
        '''
        '''
        self.uri = uri
        self.proto_serial = self.__serial_connect
        self.proto_ssh = self.__ssh_connect
        self.route = dict()
        self.route['ssh'] = self.proto_ssh
        self.route['serial'] = self.proto_serial

        xlog.info(f'== URI {self.uri}')

    def parse_addr(self):
        '''
        '''
        roto_address = self.uri.split(':')
        if len(roto_address) != 3:
            xlog.error(f"wrong # of components in address {roto_address}")
            return None, None

        xlog.info(f'== roto_address {roto_address}')
        self.protocol = roto_address[0]
        # Strip off the leading '//'
        self.address = ':'.join(roto_address[1:])[2:]
        return self.address, self.protocol

    async def connect(self):
        '''
        '''
        conn_addr, proto = self.parse_addr()
        if proto == None:
            return False

        return await self.route[proto](conn_addr)

    async def __serial_connect(self, addr):
        '''
        '''
        xlog.info(f'serial address {addr}')
        return

    async def __ssh_connect(self, addr):
        '''
            Run an ssh connection agent and return the connection. An SSHClientConnection object
            is returned against which sessions may be created or opened
        '''
        self.target = addr.split(':')[0]
        self.protocol = "ssh"
        self.port = int(addr.split(':')[1].split(':')[1])
        self.username = addr.split(':')[1].split(',')[0]
        self.password = addr.split(':')[1].split(',')[1]
        self.connection = await asyncssh.connect(self.target, port=self.port, username=self.username, password=self.password)
        self.state = 'open'
        return self.connection

    async def issue(self, cmd):
        '''
            run a command on the host of this channel and return the results in string form. 
            open a unique channel on the connection. Expect it to be unique across multiple
            calls so that parallel actions may be supported.
        '''
        whole = str()
        channelW, channelR, channelEr = await self.connection.open_session(command=cmd)
        buff = await channelR.readline()
        while channelR.at_eof() is False:
            whole += buff
            buff = await channelR.readline()

        whole += buff
        results_q.append(whole)
        return

    async def run(self):
        while True:
            while len(results_q) == 0:
                await asyncio.sleep(1)
            do_it = que_popleft()
            xlog.info(f'run command {do_it}')
            continue
            results = await issue(do_it)
            return_q.append(results)
            asyncio.sleep(0)

    async def close_connection(self):
        if self.state is open:
            await  self.connection.wait_closed()
            return

