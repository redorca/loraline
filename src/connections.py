'''
    Manage connections to the network either through ssh or serial, for the moment.
'''

import asyncio, asyncssh, sys

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
        self.connection = ''
        self.proto_serial = self.__serial_connect
        self.proto_ssh = self.__ssh_connect
        self.route = dict()
        self.route['ssh'] = self.proto_ssh
        self.route['serial'] = self.proto_serial

    def parse_addr(self):
        '''
        '''
        roto_address = self.uri.split(':')
        self.protocol = roto_address[0]
        self.address = ':'.join(roto_address[1:])[2:]
        print(f'self.address {self.address}')
        # self.port = roto_address[2].split(',')[0]
        # self.username = roto_address[2].split(',')[1]
        # self.password = roto_address[2].split(',')[2]
        return self.address, self.protocol

    async def connect(self):
        '''
        '''
        conn_addr, proto = self.parse_addr()
        print(f'conn_addr {conn_addr}')
        return
        return await self.route[proto](conn_addr)

    async def __serial_connect(self, addr):
        '''
        '''
        print(f'serial address {addr}')
        return

    async def __ssh_connect(self, addr):
        '''
            Run an ssh connection agent and return the connection. An SSHClientConnection object
            is returned against which sessions may be created or opened
        '''
        parts = addr.split(':')
        creds = parts[1].split(',')
        print(f'{parts[0]} username={creds[0]}, password={creds[1]}')
        self.connection = await asyncssh.connect(self.address, username=self.username, password=self.password)
        self.state = 'open'
        return self.connection

    async def make_channel(self):
        '''
            open a unique channel on the connection. Expect it to be unique across multiple
            calls so that parallel actions may be supported.
        '''
        return await self.connection.open_connection(self.addr, self.port)

    async def close_connection(self):
        if self.state is open:
            await  self.connection.wait_closed()
            return
