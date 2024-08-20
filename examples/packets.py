'''
    decode packets
'''
'''
'''

import json

SRC_FILE = "/tmp/output.txt"
Keys = ["gway", "type", "payload"]
# gway = str(21)


def decode_entry(fun):
    '''
        fun represents a return message from a command.

        The list.index() function doesn't return errors it raises one if
        the symbol is not present. So ignore bad entries.
    '''
    whence = fun.index('{')
    addr =  ''.join(fun[:whence]).split(' ')[-1].strip(':')
    part3 =''.join(fun[whence:])
    breakout = json.loads(part3)
    print(f'breakout {len(breakout)} {breakout["stationID"]}')
    part_addr = dict([ list(("addr", addr)) ])

    # results = { **part3, **part_addr}
    # print(f'results {results}')
    exit()
    return results


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
    return fala


nodes = []
with open(SRC_FILE, 'r') as src:
    partials = []
    while (results := src.readline().strip()):
        cmd = pkt_decode(results)
        # cmd = decode_entry(results)
        xoo = dict(list(map(mktuple, Keys, cmd)))

        if len(cmd) == 3:
            if '}' not in cmd[2] and '{' not in cmd[2]:
                    continue
            if not cmd[2].endswith('}'):
                partials.append(xoo)
                continue
            if not cmd[2].startswith('{'):
                for partial in partials:
                    if partial['type'] == xoo['type']:
                        total = ''.join([partial['payload'] , xoo['payload']])
                        partial = ''
                        xoo['payload'] = json.loads(total)
                        nodes.append(xoo)
                continue
            xoo["payload"] = json.loads(xoo["payload"])
            # print(f'xoo {type(xoo["payload"])} {xoo["payload"]}')
            # xoo["payload"] = json.loads(xoo["payload"])
            nodes.append(xoo)
            # part3 = json.loads(xoo['payload'])
            # print(f'payload {part3}')

for x in nodes:
    if "power" not in x["payload"].keys():
        continue
    print(f'=== x: {x["payload"]["power"]}')

