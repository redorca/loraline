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
async def set_params():
    '''
        Read in config file.
    '''
    configs = parse.ConfigParser(allow_no_value=True)
    foo = configs.read(Config_file)
    listen_address = '127.0.0.1'
    listen_port = configs["network"]["cli_socket"]
    ssh_server = configs["network"]["ssh_host"]

    return ssh_server, listen_address, listen_port


