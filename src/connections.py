'''
    Manage connections to the network either through ssh or serial, for the moment.
'''

import asyncio, asyncssh, sys
import logging

class Connection():
    '''
        Address is of the form <protocol>://<path to endpoint>[:<port to use>][<,user,password>]
        so a serial connection would be serial:///dev/ttySx and an ssh connection
        would be ssh:<URI>:port,user,password
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

    def parse_addr(self):
        '''
        '''
        roto_address = self.uri.split(':')
        if len(roto_address) != 3:
            print(f'bad address provided: {roto_address}, {self.uri}. Expected a split of 2 for ":"')
            raise ValueError

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
        return

    async def __ssh_connect(self, addr):
        '''
            Run an ssh connection agent and return the connection. An SSHClientConnection object
            is returned against which sessions may be created or opened
        '''
        if len(addr.split(':')) != 2:
            print(f'=== bad address provided: {addr}')
            raise ValueError

        self.target = addr.split(':')[0]
        self.protocol = "ssh"
        self.port = int(addr.split(':')[1].split(',')[0])
        self.username = addr.split(':')[1].split(',')[1]
        self.password = addr.split(':')[1].split(',')[2]
        self.connection = await asyncssh.connect(self.target, port=self.port, username=self.username, password=self.password)
        # logging.warning(f'++++ ssh_connect {type(self.connection)}')
        self.state = 'open'
        return self.connection

    async def debug_on(self, level):
        '''
        '''
        logging.basicConfig()
        asyncssh.set_log_level('DEBUG')
        asyncssh.set_debug_level(level)

    async def issue(self, cmd):
        '''
            run a command on the host of this channel and return the results in string form. 
            open a unique channel on the connection. Expect it to be unique across multiple
            calls so that parallel actions may be supported.
        '''
        whole = str()
        channelW, channelR, channelEr = await self.connection.open_session(command=cmd)
        # buff = await channelR.readline()
        buff = await channelR.read(500)
        while channelR.at_eof() is False:
            whole += buff
            # buff = await channelR.readline()
            buff = await channelR.read(500)

        whole += buff
        return whole

    async def run(self, cmds_q, results_q):
            while True:
                # logging.warning("=== :: Check the queue for pending commands.")
                do_it = await cmds_q.get()
                # logging.warning(f"--- Write the command {type(do_it)} >>{do_it}<< into stdin")
                channelW, channelR, channelEr = await self.connection.open_session(command=do_it)
                # back = await channelW.write(Command.encode("UTF8"))
                # logging.warning(f'back {back}')
                buff = await channelR.readline()
                ebuff = await channelEr.readline()
                while channelR.at_eof() is False:
                    buff += await channelR.readline()
                    ebuff += await channelEr.readline()

                try:
                    await results_q.put(buff.encode('UTF8'))
                except asyncio.QueueFull as aqf:
                    logging.warning(f'#############################################')
                    logging.warning(f'{aqf}')

    async def make_channel(self, cmd):
        '''
            open a unique channel on the connection. Expect it to be unique across multiple
            calls so that parallel actions may be supported.
        '''
        return await self.connection.open_session(command=cmd)

    async def close_connectionn(self):
        if self.state is open:
            await  self.connection.wait_closed()
            return

    async def close_connection(self):
        self.connection.close()
        await  self.connection.wait_closed()

