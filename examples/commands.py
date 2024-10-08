'''
    Support every lora command available.
'''
from loraline import network

class cmds():
    '''
        Methods and variables universal to the commnds
    '''
    def __init__(self):
        self._From = None
        self.cmd_prefix = '#'
        return

    @property
    def From(self):
        if self._From is None:
            raise(ValueError)
        return self._From

    @From.setter
    def From(self, value):
        self._From = value

    def issue(self, cmd):
        return

    def _cmd_string(self, gateway, cmd):
        return f"#{gateway} {self.action} {cmd} from {self._From}\n" 

class get(cmds):
    '''
        the get command has a number of sub commands that have unique
        generating and return processing needs to be handled here.`
    '''
    def __init__(self):
        super().__init__()
        self.action = "get"
        return

    def info(self, gateway):
        return self._cmd_string(gateway, "info")

    def map(self, gateway):
        return self._cmd_string(gateway, "map")

    def online(self, gateway):
        return self._cmd_string(gateway, "online")

    def nwinfo(self, gateway):
        return self._cmd_string(gateway, "nwinfo")

    def debug(self, gateway):
        return self._cmd_string(gateway, "debug")

    def id(self, gateway):
        return self._cmd_string(gateway, "id")

    def userinfo(self, gateway):
        return self._cmd_string(gateway, "userinfo")

    def new_map(self, gateway):
        return self._cmd_string(gateway, "new map")

    def grpinfo(self, gateway):
        return self._cmd_string(gateway, "grpinfo")


if __name__ == "__main__":
    def main():
        foo = network.network()
        foo.gateway = 32
        print(f'foo.gateway {foo.gateway}')

    main()
