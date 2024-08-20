'''
    decode packets
'''
'''
'''

import json

SRC_FILE = "/tmp/output.txt"
Keys = ["gway", "type", "payload"]
# gway = str(21)

def mktuple(key, item):
    '''
        Build and return a set of the args that the caller
        can then process into a dictionary
    '''
    return (key, item)


def smersh(filename, legend, delim=':'):
    '''
        Convert a text file of data lines into a list of dictoinaries using
        legend as the keys in the dictionary in the order to be decoded from the text line.
    '''
    xoo = list(map(mktuple, legend, fool.split(delim)))
    return xoo


def pkt_decode(line):
    '''
        Given a return string break it down into a command dictionary and return
    '''
    fala = line.split(':', maxsplit=2)
    print(f' line < {line} > \n=== {fala}')
    return fala


with open(SRC_FILE, 'r') as src:
    nodes = []
    while (results := src.readline().strip()):
        cmd = pkt_decode(results)
        xoo = dict(list(map(mktuple, Keys, cmd)))

        if len(cmd) == 3:
            print(f'payload {xoo["payload"]}')
            nodes.append(xoo)
            # part3 = json.loads(xoo['payload'])
            # print(f'payload {part3}')
            exit()

