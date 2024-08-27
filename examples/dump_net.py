'''
    A collection of introspection methods to reveal inner workings
'''

str_ref = "string"
dict_ref = {}
list_ref = []


def dump_net(network):
    '''
        network is a dictionary containing all of the data for the nodes and state of the network.
    '''
    for item in network.keys():
        if item is None or item == 0:
            continue
        '''
        if type(network[item]) == type(dict_ref):
            print(f"found a dict: {network[item]}")
        elif type(network[item]) == type(str_ref):
            print(f"found a str: {network[item]}")
        elif type(network[item]) == type(list_ref):
            print(f"found a list: {network[item]}")
        '''
        print(f'---> {item}')
        if type(network[item]) == type(dict_ref):
            print(f'\n============= {item} ===============')
            for entry in network[item].keys():
                print(f':: [{item}]{[entry]} {network[item][entry]}')
        elif type(network[item]) == type(list_ref):
            print(f'\n============= {item} ===============')
            for ndx in range(0, len(network[item]), 1):
                print(f'({ndx}) {network[item][ndx]}')
            print('-----------------------')
            print()
