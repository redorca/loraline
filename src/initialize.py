'''
    For setup tasks common to the server and client and so to avoid
    duplicating setup code that code is placed here so that both ends
    of the connection are reading the same config file, using the same
    config parameters
'''
'''
'''
'''
'''
import asyncio
import configparser as parse

Config_file = "/etc/loraline/netmanage.conf"

async def get_params(func):
    '''
        Read in config file. Choose the set of parameters to use based on
        the location of the listener. A remote listener would use ssh_xxx
        and a local listener would be a client hence cli_xxx
    '''
    key_host = "cli_host"
    key_socket = "cli_socket"

    if func == "remote":
        key_host = "ssh_host"
        key_socket = "ssh_socket"

    configs = parse.ConfigParser(allow_no_value=True)
    foo = configs.read(Config_file)
    listen_port = configs["network"][key_socket]
    listen_system = configs["network"][key_host]

    return listen_system, listen_port


