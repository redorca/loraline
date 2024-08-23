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


def decode_loglines(msg):
    '''
        Decode log entries
    '''
    format = "%b %d %H:%M:%S %Y"
    Keys = ["gateway", "count", "stamp", "message"]
    pieces = msg.split(':', maxsplit=2)
    foof = pieces[2].strip().split(' ')[:4]
    stamp = ' '.join(foof)
    phoo = dt.datetime.strptime(stamp, format)
    msg = pieces[2].split(' ')[5:]
    message = ' '.join(pieces[2].split(' ')[5:])
    xoo = dict(list(map(mktuple, Keys, [pieces[0], pieces[1], phoo, message])))
    return xoo

def decode_timestamp(stamp):
    '''
        given a time string of the form [mm-dd h:m:s] convert it
        to a date suitable for conversion to an iso format date object
        via a strptime call
    '''
    Keys = ["timestamp", "msg" ]
    if len(stamp) < 8:
        return None
    the_dateformat="%m-%d-%Y %H:%M:%S"
    to_be_iso_time = stamp.split(']')
    time_pieces = to_be_iso_time[0][1:].split(' ')
    near_iso_time = '-'.join([time_pieces[0], "2024"])
    newstamp = dt.datetime.strptime(' '.join([near_iso_time, time_pieces[1]]), the_dateformat)
    return "timestamp", (newstamp, to_be_iso_time[1])

def decode_cmd_resp(msg):
    '''
        Translate a command response string into a dictionary object
        for this node.
    '''
    pieces = msg.split(':', maxsplit=2)
    if len(pieces) != 3:
        return None
    Keys = ["gateway", "signature", "payload"]
    xoo = dict(list(map(mktuple, Keys, pieces)))
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
    if len(line) < 3:
        print(f'line is too short {line}')
        return

    if line[0] == '[' :
        fala = decode_timestamp(line)
    else:
        fala = None
    # elif '}' in line or '{' in line:
        # fala = decode_cmd_resp(line)
        # fala =  None
    # else:
        fala =  None

    return fala

tmp = "21: 1: Aug 15 15:50:57 2024 temperature From 21: Internal temperature 84C now below 85C"
# decode_loglines(tmp)
print(f'decode loglines {decode_loglines(tmp)}')
exit()
nodes = []
with open(SRC_FILE, 'r') as src:
    partials = []
    while (results := src.readline()):
        cmd = pkt_decode(results.strip())
        if cmd is not None:
            print(f'cmd {cmd}')

exit()
for x in nodes:
    print(f'=== x: {x["signature"]}')

