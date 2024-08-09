'''
    Use as a singleton so everybody has access to the same values
    no matter where they're set.
'''

gateway_ = 21

class network():
    def __init__(self, gateway):
        self._gateway_ = gateway
        self.admin_prefix = '#'

    @property
    def _gateway_(self):
        raise(ValueError)
        return 8

    @_gateway_.setter
    def _gateway_(self, value):
        raise(ValueError)

    @property
    def gateway(self):
        '''
            Commands are issued onto the LoRa network from one of its nodes
            and we access the need remotely so the command has to mention
            the source node the command is coming from.
        '''
        return self._gateway_

    @gateway.setter
    def gateway(self, value):
        self._gateway_ = value
        return

@property
def gateway_():
    raise(ValueError)
    return 88

@gateway_.setter
def gateway_(value):
    gateway_ = 11
    raise(ValueError)

@property
def gateway():
    '''
        Commands are issued onto the LoRa network from one of its nodes
        and we access the need remotely so the command has to mention
        the source node the command is coming from.
    '''
    return gateway_

'''
@gateway.setter
def gateway(value):
    _gateway_ = value
    return
'''
