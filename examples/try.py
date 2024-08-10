'''
    figure out how to use a plain text file as a config file suitable for ConfigParser
'''

import json
import os
import configparser
import tomllib

ACKFILE  = "/tmp/ack"
NACKFILE = "/tmp/nack"
NODES    = "/tmp/Nodes.txt"
SIGNALS  = "/tmp/Signals.txt"
network = list()

def toml_parse(filepath):
    '''
        read in a file into configparser
    '''
    with open(filepath, 'rb') as foop:
        results = tomllib.load(foop)
    return results


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
    except configparser.MissingSectionHeaderError as mse:
        cparse = None
    return cparse


def mktuple(key, item):
    return (key, item)


def decode(filename, delim=':'):
    '''
        The info file contains a set of json objects and decode ala json.dumps()
    '''
    if not os.path.exists(filename):
        return None
    nodes = list()
    with open(filename, 'r') as spot:
        while( info := spot.readline().strip()):
            fun = list(info)
            if fun[0] != '#':
                try:
                    whence = fun.index('{')
                    addr =  ''.join(fun[:whence]).split(' ')[-1].strip(':')
                    part2 = ''.join(fun[whence:])
                    part3 =json.loads(part2)
                    part_addr = dict([ list(("addr", addr)) ])
                    nodes.append({ **part3, **part_addr})
                except ValueError as ver:
                    continue
                    
    return nodes



def old_decode_map(squiggle):
    '''
        data specific decode intended for return by return parsing akin to line by line.
        Expect the arg passed to be split at '{' into two parts.
        Returns a dictionary mapping the "map" and "SNR" data to "map" and "SNR"
    '''
    #Split in 2 at the '{'
    alpha = squiggle[1].strip("}")
    #split each part into two at the ':' char
    dummy = alpha.split(",")[0].split(":")
    rummy = alpha.split(",")[1].split(":")
    # Assemble a bunch of tuples into a list that can then be turned into a dict
    sterr = [(dummy[0].strip('"'), dummy[1]),
             (rummy[0].strip('"'), rummy[1]),
             ("id", squiggle[0].split(' ')[3].strip(':'))]
    return dict(sterr)

def decode_map(squiggle):
    '''
        data specific decode intended for return by return parsing akin to line by line.
        Expect the arg passed to be split at '{' into two parts.
        Returns a dictionary mapping the "map" and "SNR" data to "map" and "SNR"
    '''
    shoe = list(squiggle)
    print(f'shoe[1] {shoe[1]}')


def find_name(ident, mapping):
    '''
        lookup an entry in the network list that matches the ident passed in.
        So, basically an address to name map
    '''
    # print(f'Ident {ident}')
    for cache in mapping:
        # print(f'{ident}, {cache["ID"]}')
        if cache['ID'].strip() == ident.strip():
            # print(f'found a mapping {cache}')
            return cache


def smersh(filename, legend, delim=':'):
    '''
        Convert a text file of data lines into a list of dictoinaries using
        legend as the keys in the dictionary in the order to be decoded from the text line.
    '''
    if not os.path.exists(filename):
        return None
    nodes = list()
    with open(filename, 'r') as spot:
        while (foo := spot.readline().strip()):
            if foo[0] != '#':
                xoo = list(map(mktuple, legend, foo.split(delim)))
                nodes.append(dict(xoo))
    return nodes


def locate_files(file_list):
    phie = list()
    for fyy in [NODES, SIGNALS]:
        if not os.path.exists(fyy):
            print(f'Can\'t find {fyy}.')
            phie.append(fyy)

    return phie


def main():
    '''
        read in a file into configparser
    '''
    # see if a list of missing files is returned.
    if (yikes := locate_files([NODES, SIGNALS])) is not None : exit(1)
    atchafalala= dict()
    network = smersh(NODES, ["Name", "ID", "GPS"], delim=':')
    for result in decode(SIGNALS, delim='{'):
        spore = find_name(result['addr'], network)
        whole = {**spore, **result}
        atchafalala[int(whole['addr'])] = whole
    # [ print(f'  {x}') for x in atchafalala.keys() ]
main()
