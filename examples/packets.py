'''
    decode packets
'''
'''
'''

import json
import datetime as dt
import dump_net as dn

SRC_FILE = "/tmp/output.txt"


def mktuple(key, item):
    '''
        Build and return a set of the args that the caller
        can then process into a dictionary
    '''
    return (key, item)


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
    pieces = line.rstrip('.').split('.')
    if len(pieces) != 2:
        return None, None
    if "Path" in pieces[1]:
        left  = pieces[0].split(' ', maxsplit=3)
        right = pieces[1].strip().split(' ', maxsplit=2)
        Path = right[2].split(' ')
        Keys = ["ID", "condition", "Path"]
        xoo = dict(list(map(mktuple, Keys, [left[2], left[3], Path])))
        Prefix = RU_ON
    else:
        # print(f'== pieces[1] {pieces[1]}')
        left = pieces[0].split(' ', maxsplit=3)
        Keys = ["ID", "response" ]
        xoo = dict(list(map(mktuple, Keys, [left[2], " ".join([left[3], pieces[1]])])))
        Prefix = RU_OK

    return Prefix, xoo


def decode_loglines(line):
    '''
        Decode further responses of the form "21:  7: xxxxxx" or "21: 8 xxxxx" into log entries,
        wifi network entries, and log details (e.g. 5 of 8 entries)
    '''
    station = None
    xoo = None
    '''
        This little dance strips out any  '>' embedded in the string between the
        log entry ordinal and the date-time stamp. This makes generically splitting
        the string on ':' will always separate the data-time string from the offset. 
    '''
    tmp  = line.split('>', maxsplit=2)
    log_ndx = ' '.join(tmp).split(':', maxsplit=2)
    if len(log_ndx) > 2:
        the_dateformat="%b %d %H:%M:%S %Y"
        Keys = ["count", "stamp", MSG]
        log_ndx[2] = log_ndx[2][1:]
        pieces = log_ndx[2].split(' ', maxsplit=4)
        timestr = ' '.join(pieces[0:4])
        message = ' '.join(pieces[4:])
        try:
            timestamp  = dt.datetime.strptime(timestr, the_dateformat)
            xoo = dict(list(map(mktuple, Keys, [log_ndx[1], timestamp, message])))
            station = LOGS
        except ValueError as vle:
            '''
                May be a response to a "get wifi" command. The response is of the form
                "node_#, network_#, SSID, signal_strength, channel_#". SSID may be more
                thant a single word; it may contain spaces.
            '''
            Keys = ["#", "SSID", "dB", "channel"]
            msg = log_ndx[2].split(',')
            xoo = dict(list(map(mktuple, Keys,
            [log_ndx[1], msg[0], msg[1].strip(" ").split(" ")[0], msg[2].strip(" ").split(" ")[1]])))
            station = WIFI
    else:
        '''
            Likely an initial response to a "get log from xx" command which details
            how many log entries are on the node and what offset into that array of
            log entries the next 9 logs correspond to.
        '''
        xoo = {}

    return station, xoo


def decode_system(line):
    '''
        Capture messages a node emits spontaneously
    '''
    station = None
    xoo = None
    pieces = line.split(' ', maxsplit=2)
    if len(pieces) > 2:
        # station pieces[2].split(':')[0]
        station = LOGS
        msg = pieces[2].split(':')[1]
        node = pieces[2].split(':')[0]
        if pieces[1] == "found":
            node = ""
            msg = pieces[2]
        Keys = [ pieces[1], MSG]
        xoo = dict(list(map(mktuple, Keys, [node, msg])))
    return station, xoo

global log_node, wifi_node 
log_node = "0"
wifi_node = "0"
def pkt_decode(line):
    '''
        Given a return string break it down into a command dictionary and return
    '''
    filter_0 = {"Info": decode_cmd_resp, "ID": decode_on_ok, "From": decode_system, "found": decode_system}
    pieces = line.strip().split(' ', maxsplit=3)
    if len(pieces) < 3:
        return None, None
    station = None
    fala = None
    begins = pieces[0].strip("#:")
    if begins == "21":
        # print(f"shell line: {line}, {len(pieces)}")
        fala = None
        if len(pieces) > 2 and pieces[1] in filter_0:
            station, fala = filter_0[pieces[1]](line)
        elif len(pieces) > 2 and pieces[1].split('>')[0].strip(':').isdigit():
            station, fala = decode_loglines(line)
    elif begins.startswith('['):
        station, fala = decode_timestamp(line)
    else:
        # print(f'else {line}')
        station = None

    return station, fala


network = {}
META="Meta"
WIFI = "Wifi"
LOGS  = "Logs"
RU_ON = "RU_ON"
RU_OK = "RU_OK"
MSG = "Message"
LOG_FROM="Logged From"
WIFI_LOG="Wifi Log For"
ANNOUNCE = "announcements"
CATEGORIES = [ANNOUNCE, RU_ON, RU_OK, LOGS, WIFI]
with open(SRC_FILE, 'r') as src:
    partials = []
    network[ANNOUNCE] = []
    network[WIFI] = []
    network[LOGS] = []
    network[RU_ON] = []
    network[RU_OK] = []
    network[META] = {}
    network[META][LOG_FROM] = ""
    network[META][WIFI_LOG] = ""

    while (results := src.readline()):
        '''
        '''
        station, cmd = pkt_decode(results.strip())
        if station is None or cmd is None:
            continue
        if station in CATEGORIES and not cmd is None:
            network[station].append(cmd)
        else:
            network[station] = cmd


dn.dump_net(network)

