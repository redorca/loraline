'''
    figure out how to use a plain text file as a config file suitable for ConfigParser
'''

import json
import os
import sys
import configparser
from loraline import network
import commands as cmd

ACKFILE  = "/tmp/ack"
NACKFILE = "/tmp/nack"
NODES    = "/tmp/nodes.txt"
SIGNALS  = "/tmp/signals.txt"
# CONFIG   = "/etc/loraline/netmanage.conf"

def parse(filepath):
    '''
        read in a file into configparser
    '''
    cparse = configparser.ConfigParser(allow_no_value=True)
    try:
        cparse.read(filepath)
    except configparser.MissingSectionHeaderError as mse:
        print(f'== {mse}')
        cparse = None

    return cparse


def reparse(filepath):
    '''
        read in a file into configparser
    '''
    try:
        cparse = configparser.ConfigParser(allow_no_value=True)
        with open(filepath, 'r', encoding='UTF8') as foop:
            buf = foop.read()
            cparse.read_string("\n".join([ "[DEFAULT]",buf ]))
    except configparser.MissingSectionHeaderError:
        cparse = None
    return cparse


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
    part3 =json.loads(''.join(fun[whence:]))
    part_addr = dict([ list(("addr", addr)) ])

    return { **part3, **part_addr}


def decode(filename, delim=':'):
    '''
        The info file contains a set of json objects and decode ala json.dumps()
    '''
    if not os.path.exists(filename):
        return None
    nodes = []
    with open(filename, 'r', encoding='UTF8') as spot:
        while( info := spot.readline().strip()):
            fun = list(info)
            if fun[0] != '#':
                try:
                    nodes.append(decode_entry(fun))
                except ValueError:
                    continue

    return nodes


def find_name(ident, mapping):
    '''
        lookup an entry in the network list that matches the ident passed in.
        So, basically an address to name map
    '''
    for cache in mapping:
        # print(f'cache[ID] {cache["ID"]}, ident {ident}')
        if cache['ID'] == ident:
            return cache
    return None

def smersh(filename, legend, delim=':'):
    '''
        Convert a text file of data lines into a list of dictoinaries using
        legend as the keys in the dictionary in the order to be decoded from the text line.
    '''
    nodes = []
    with open(filename, 'r', encoding='UTF8') as spot:
        while (fool := spot.readline().strip()):
            if fool[0] != '#':
                xoo = list(map(mktuple, legend, fool.split(delim)))
                nodes.append(dict(xoo))
    return nodes


def locate_files(file_list):
    '''
        Look for all of the given files and make sure they exist.
    '''
    missing = []
    found = []
    for fyy in file_list:
        if not os.path.exists(fyy):
            # print(f'Can\'t find {fyy}.')
            missing.append(fyy)
        else:
            found.append(fyy)

    return found, missing


def main():
    '''
        read in a file into configparser
    '''
    # see if a list of missing files is returned.
    found, missing = locate_files([NODES, SIGNALS])
    if len(missing) != 0:
        [ print(f'Missing file: {x}') for x in missing ]
        sys.exit(1)
    atchafalala= {}
    network = smersh(NODES, ["Name", "ID", "GPS"], delim=':')
    for result in decode(SIGNALS, delim='{'):
        if (spore := find_name(result['addr'], network)) is None: sys.exit(3)
        whole = {**spore, **result}
        atchafalala[int(whole['addr'])] = whole
    [ print(f'  {x}, {atchafalala[x]["Name"]}') for x in atchafalala ]

main()
network.gateway = 33
get = cmd.get()
get.From = 21
foof = get.info(network.gateway)
print(f'foof {foof}')
get.From = 12
foof = get.new_map(network.gateway)
print(f'foof {foof}')
