'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import asyncio
from collections import deque
import platform
import configparser as parse

Config_file = "/etc/loraline/netmanage.conf"
def main():
    '''
        Read in config file.
    '''
    configs = parse.ConfigParser(allow_no_value=True)
    foo = configs.read(Config_file)
    listen_address = '127.0.0.1'
    listen_port = configs["network"]["cli_socket"]
    ssh_server = configs["network"]["ssh_host"]

main()

