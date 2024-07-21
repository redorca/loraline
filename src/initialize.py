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

async def build_uri(host, port, protocol, user, password):
    elements = ":".join([protocol, ''.join(["//", host]), port])
    uri = ",".join([elements, user, password])
    print(f'host {host}, port {port} & uri {uri} built')
    return uri


async def get_params(region):
    '''
        Read in config file. Choose the set of parameters to use based on
        the location of the listener. A remote listener would use ssh_xxx
        and a local listener would be a client hence cli_xxx
    '''
    key_host = "cli_host"
    key_socket = "cli_socket"

    if region == "remote":
        key_host = "ssh_host"
        key_socket = "ssh_socket"

    configs = parse.ConfigParser(allow_no_value=True)
    configs.read(Config_file)
    entries = configs.options("network")
    want = [configs.get("network", x) for x in entries if x.split('.')[0] == "local"]
    return want[1], want[0]


