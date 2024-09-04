'''
    Contains data about the node. E.g. gps coordinates, SNR relative to neighbors, id,
    and general device status.
'''

import configparser as parse
import asyncio

class Network():
    '''
        Hold network focused information such as set of nodes in the network, node layout,
        neighbors, SNR maps, missing nodes, powered down nodes, general power states and contexts.

        The class Node() holds its meta data like power state, power condition, type, etc.
    '''

    def __init__(self, node_file):
        self.parse = parse.ConfigParser(allow_no_value=True)
        # self.data_set = self.parse.read(node_file)
        self.nodes = list()
        self.node_file = node_file
        self.network = dict()

        return

    def __get_config__(self):
        with open(self.node_file) as file:
            node_list = file.read()
            self.nodes = node_list.split('\n')
        return self.nodes

    def __populate__(self):
        for entry in self.__get_config__():
            self.network[entry.split(':')[0]] = list(entry.split(':')[1:])
        return self.network

    def dump_entries(self):
        print(f'{self.__get_config__(self. node_file)}')



if __name__ == "__main__":
    named = "/tmp/LoRa Device GPS.txt"
    def main():
        foo = Network(named)
        bigsky = foo.__populate__()
        print(f'{[x[0] for x in bigsky.values()]}')

    main()

