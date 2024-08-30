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


def mktuple(key, item):
    '''
        Build and return a set of the args that the caller
        can then process into a dictionary
    '''
    return (key, item)


async def build_uri(host, port, protocol, user, password):
    elements = ":".join([protocol, ''.join(["//", host]), port])
    uri = ",".join([elements, user, password])
    print(f'returning uri {uri}')
    return uri


async def get_params(region):
    '''
        Read in config file. Choose the set of parameters to use based on
        the location of the listener. A remote listener would use ssh_xxx
        and a local listener would be a client hence cli_xxx
    '''

    configs = parse.ConfigParser(allow_no_value=True)
    configs.read(Config_file)
    entries = configs.options("network")
    Keywords = ["Port", "Host"]
    want = map(mktuple, Keywords, [configs.get("network", x) for x in entries if x.split('.')[0] == region])
    entries = configs.options("daemon")
    daemon = map(mktuple, Keywords, [configs.get("daemon", x) for x in entries if x.split('.')[0] == "daemon"])
    frah = dict()
    frah["connect"] = dict(list(want))
    frah["daemon"] = dict(list(daemon))
    return frah
    # return want[1], want[0]


if __name__ == "__main__":
    async def main():
        wants = await get_params("remote")
        print(f'---- wants {wants}')

    asyncio.run(main())
