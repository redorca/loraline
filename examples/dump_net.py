'''
    A collection of introspection methods to reveal inner workings
'''

str_ref = "string"
dict_ref = {}
list_ref = []

class Dump():
    '''
        Expose network internal data
    '''
    def __init__(self, network, Keys):
        '''
        '''
        self.foo = "foo"
        self.network = network
        self.Keys = Keys

    def dump_nodes(self):
        '''
            Sift for nodes which are digit only strings.
        '''
        print(f'============= Nodes ====================')
        for node in self.network.keys():
            if node.isdigit():
                print(f'    {node}\t{self.network[node]}')

    def __node_parse(self, node, filter_keys):
        '''
        '''
        results = []
        for xxx in filter_keys:
            if xxx in node["payload"]:
                results.append(f'\t{xxx} {node["payload"][xxx]}')
        return results

    def dump_filter(self, filters):
        '''
            Dump data specified in filters for any node holding that data.
        '''
        for node in self.network.keys():
            if node.isdigit():
                if len(contents := self.__node_parse(self.network[node], filters))!= 0:
                    print(f'\t{node}::  ')
                    [print(f'\t{xxx}') for xxx in contents ]


    def dump_net(self):
        '''
            network is a dictionary containing all of the data for
            the nodes and state of the network.
        '''
        for item in self.network.keys():
            if item is None or item == 0:
                continue
            if type(self.network[item]) == type(dict_ref):
                print(f'\n============= {item} ===============')
                for entry in self.network[item].keys():
                    print(f':: [{item}]{[entry]} {self.network[item][entry]}')
            elif type(self.network[item]) == type(list_ref):
                print(f'\n============= {item} ===============')
                for ndx in range(0, len(self.network[item]), 1):
                    print(f'({ndx}) {self.network[item][ndx]}')
                print('-----------------------')
                print()
