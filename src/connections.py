'''
    Manage connections to the network either through ssh or serial, for the moment.
'''

import asyncio, asyncssh, sys

class Connection():
    '''
        Address is of the form <protocol>:<path to endpoint>[<port to use>][<:user,password>]
        so a serial connection would be serial:/dev/ttySx and an ssh connection
        would be ssh:<URI>:user:password
    '''
    def __init__(self, address):
        '''
        '''
        self.address = address
        self.connection = ''
        self.proto_serial = self.__serial_connect
        self.proto_ssh = self.__ssh_connect
        self.route = dict()
        self.route['ssh'] = self.proto_ssh
        self.route['serial'] = self.proto_serial

    def flub(self, proto_address):
        '''
        '''
        roto_address = proto_address.split(':')
        if roto_address[0] == 'serial':
            proto_address = ':'.join(roto_address[1:])
        return proto_address, roto_address[0]

    async def connect(self):
        '''
        '''
        conn_addr, proto = self.flub(self.address)
        await self.route[proto](conn_addr)

    async def __serial_connect(self, addr):
        '''
        '''
        print(f'serial address {addr}')
        return

    async def __ssh_connect(self, addr):
        '''
        '''
        print(f'ssh address {addr}')
        return
