'''
    Use as a singleton so everybody has access to the same values
    no matter where they're set.
'''

gateway = None

class network():
    def __init__(self):
        self._gateway_ = gateway
        self.admin_prefix = '#'

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

if __name__=="__main__":
    print("=====")
