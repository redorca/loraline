
class net():
    '''
        A base class providing elements common to all commands and return messages.
    '''
    __init__(self, gateway):
        self.gateway = gateway
        return

    @property()
    def gateway(self, gateway):
        '''
            Commands are issued onto the LoRa network from one of its nodes
            and we access the need remotely so the command has to mention
            the source node the command is coming from.
        '''
        self.gateway = gateway

