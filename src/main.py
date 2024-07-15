'''
    Create tasks including a listener socket for receiving cmds from the CLI
'''

import asyncio
from collections import deque
import platform
import configparser as parse

def main():
    '''
        Read in config file.
    '''
    configs = parse.ConfigParser(allow_no_value=True)
    foo = configs.read('/etc/loraline/netmanage.conf')
    print(f'sections {configs.sections()} {configs.items("lora")}')
    for sect in configs.sections():
        print(f'items in {sect} : {configs.items(sect)}')



main()

