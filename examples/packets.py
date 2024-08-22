'''
    decode packets
'''
'''
'''

import json
import datetime as dt

SRC_FILE = "/tmp/output.txt"

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

def decode_timestamp(stamp):
    '''
        given a time string of the form [mm-dd h:m:s] convert it
        to a date suitable for conversion to an iso format date object
        via a strptime call
    '''
    if len(stamp) < 8:
        return None
    the_dateformat="%m-%d-%Y %H:%M:%S"
    to_be_iso_time = stamp.split(']')
    time_pieces = to_be_iso_time[0][1:].split(' ')
    near_iso_time = '-'.join([time_pieces[0], "2024"])
    newstamp = dt.datetime.strptime(' '.join([near_iso_time, time_pieces[1]]), the_dateformat)
    return "timestamp", newstamp

def decode_cmd_resp(msg):
    '''
        Translate a command response string into a dictionary object
        for this node.
    '''
    pieces = msg.split(':', maxsplit=2)
    if len(pieces) != 3:
        return None
    Keys = ["gateway", "signature", "payload"]
    # xoo = dict(list(map(mktuple, Keys, cmd)))
    if not pieces[2].endswith('}'):
        partials.append(xoo)
        return None
    if not pieces[2].startswith('{'):
        for partial in partials:
            if partial['type'] == xoo['type']:
                total = ''.join([partial['payload'] , xoo['payload']])
                partial = ''
                xoo['payload'] = json.loads(total)
                nodes.append(xoo)
    xoo["payload"] = json.loads(xoo["payload"])
    return xoo



def pkt_decode(line):
    '''
        Given a return string break it down into a command dictionary and return
    '''
    if line[0] == '[' :
        fala = decode_timestamp(line)
    elif '}' in msg or '{' in msg:
        fala = decode_cmd_resp(msg)
    else:
            fala =  None

    return fala

foof = pkt_decode("[08-15 17:26:41]")
print(f'foof {type(foof)}  {foof}')

exit()
nodes = []
with open(SRC_FILE, 'r') as src:
    partials = []
    while (results := src.readline().strip()):
        cmd = pkt_decode(results)
        # cmd = decode_entry(results)
        Keys = ["gway", "type", "payload"]
        xoo = dict(list(map(mktuple, Keys, cmd)))
        # print(f':: {xoo["signature"]}')
        if len(xoo) > 1:
            print(f':: {len(xoo)} {xoo["signature"]}')
        else:
            print(f':: {len(xoo)} {xoo}')
        continue
        if len(cmd) == 3:
            if '}' not in cmd[2] and '{' not in cmd[2]:
                    continue
            if not cmd[2].endswith('}'):
                partials.append(xoo)
                continue
            if not cmd[2].startswith('{'):
                for partial in partials:
                    if partial['signature'] == xoo['signature']:
                        total = ''.join([partial['payload'] , xoo['payload']])
                        partial = ''
                        xoo['payload'] = json.loads(total)
                        nodes.append(xoo)
                continue
            xoo["payload"] = json.loads(xoo["payload"])
            # print(f'xoo {signature(xoo["payload"])} {xoo["payload"]}')
            # xoo["payload"] = json.loads(xoo["payload"])
            nodes.append(xoo)
            # part3 = json.loads(xoo['payload'])
            # print(f'payload {part3}')

for x in nodes:
    print(f'=== x: {x["signature"]}')

