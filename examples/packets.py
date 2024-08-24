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
    return xoo["gateway"], xoo

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
    return ANNOUNCE, {"timestamp": (newstamp, to_be_iso_time[1])}

def decode_cmd_resp(msg):
    '''
        Translate a command response string into a dictionary object
        for this node.
    '''
    station = None
    pieces = msg.split(':', maxsplit=2)
    if len(pieces) != 3:
        return station, None
    Keys = ["gateway", "signature", "payload"]
    xoo = dict(list(map(mktuple, Keys, pieces)))
    if not pieces[2].endswith('}'):
        partials.append(xoo)
        return station, None
    if not pieces[2].startswith('{'):
        for partial in partials:
            if partial['signature'] == xoo['signature']:
                total = ''.join([partial['payload'] , xoo['payload']])
                partial = ''
                xoo['payload'] = json.loads(total)
    station = xoo['signature'].strip().split(' ')[2]
    return station, xoo


def decode_on_ok(line):
    '''
        The response to both "send RU_OK to 0" and "send RU_ON to 0" starts with
        the signature "[0-9]*: ID". RU_ON contains 'Path' and RU_OK does not.

        RUN_ON also contains a period ('.') so can be split into 2 on that and RU_OK
        cannot.
    '''
    # Split on '.' into two pieces if this is an RU_ON response.
    pieces = line.split('.')
    if len(pieces) == 2:
        left  = pieces[0].split(' ', maxsplit=3)
        right = pieces[1].strip().split(' ', maxsplit=2)
        Path = right[2].split(' ')
        Keys = ["ID", "condition", "Path"]
        xoo = dict(list(map(mktuple, Keys, [left[2], left[3], Path])))
        Prefix = RU_ON

    else:
        left = pieces[0].split(' ', maxsplit=3)
        Keys = ["ID", "response" ]
        xoo = dict(list(map(mktuple, Keys, [left[2], left[3]])))
        Prefix = RU_OK

    if left[1] != "ID":
        return None, None

    return Prefix, xoo


def pkt_decode(line):
    '''
        Given a return string break it down into a command dictionary and return
    '''
    if len(line) < 3:
        # print(f'line is too short [{line}]')
        return None, None
    station = None
    if line[0] == '[' :
        station, fala = decode_timestamp(line)
    elif '}' in line or '{' in line:
        # print(f'elif {line}')
        try:
            station, fala = decode_cmd_resp(line)
            # print(f'=== station {station}')
        except TypeError as te:
            fala = None
            station = None
            print(f'type error {te}')
    elif "ID" in line:
        station, fala = decode_on_ok(line)
    else:
        # print(f'else {line}')
        station = None
        fala =  None

    return station, fala

# tmp = "21: 1: Aug 15 15:50:57 2024 temperature From 21: Internal temperature 84C now below 85C"
# # decode_loglines(tmp)
# print(f'decode loglines {decode_loglines(tmp)}')
# exit()
network = {}
RU_ON = "RU_ON"
RU_OK = "RU_OK"
ANNOUNCE = "announcements"
with open(SRC_FILE, 'r') as src:
    partials = []
    network[ANNOUNCE] = []
    network[RU_ON] = []
    network[RU_OK] = []

    while (results := src.readline()):
        station, cmd = pkt_decode(results.strip())
        if station == ANNOUNCE:
            network[station].append(cmd)
        elif station == RU_ON:
            network[RU_ON].append(cmd)
        elif station == RU_OK:
            network[RU_OK].append(cmd)
        else:
            network[station] = cmd
        # if cmd is not None:
            # print(f'station {station}, cmd {cmd}')


for item in network.keys():
    if item is None or item == 0:
        continue
    if "payload" in network[item]:
        print(f'{item} {network[item]["payload"]}')
    if item == ANNOUNCE:
        print(f'\n============= {ANNOUNCE} ===============')
        for ndx in range(0, len(network[ANNOUNCE]), 1):
            print(f'{ndx} {network[ANNOUNCE][ndx]}')
        print()
    if item == RU_ON:
        for element in range(0, len(network[item]), 1):
            print(f'== == {element} {item} {network[item][element]["Path"]}')
        print('-----------------------')
    if item == RU_OK:
        for element in range(0, len(network[item]), 1):
            print(f'== == {element} {item} {network[item][element]}')
        print('-----------------------')


exit()
