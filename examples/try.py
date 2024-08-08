'''
    figure out how to use a plain text file as a config file suitable for ConfigParser
'''

import json
import configparser
import tomllib

ACKFILE  = "/tmp/ack"
NACKFILE = "/tmp/nack"
NODES    = "/tmp/nodes.txt"
SIGNAL   = "/tmp/signals.txt"

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


Topo = dict()

def mkdict(key, item):
    return (key, item)


def decode(filename, delim=':'):
    '''
        The info file contains a set of json objects and decode ala json.dumps()
    '''
    nodes = list()
    with open(filename, 'r') as spot:
        while( info := spot.readline().strip()):
            if info[0] != '#':
                duo = info.split('{')
                if len(duo) > 1:
                    nodes.append(decode_map(duo))
    return nodes


def decode_map(squiggle):
    '''
        data specific decode intended for return by return parsing akin to line by line.
    '''
    ruff = dict()
    ruff["ident"] = squiggle[0].split(' ')[3].strip(':')
    alpha = squiggle[1].strip("}")
    dummy = alpha.split(",")[0].split(":")
    ruff[dummy[0].strip('"')] = dummy[1]
    dummy = alpha.split(",")[1].split(":")
    ruff[dummy[0].strip('"')] = dummy[1]

    return ruff

def smersh(filename, legend, delim=':'):
    '''
        Convert a text file of data lines into a list of dictoinaries using
        legend as the keys in the dictionary in the order to be decoded from the text line.
    '''
    nodes = list()
    with open(filename, 'r') as spot:
        while (foo := spot.readline().strip()):
            if foo[0] != '#':
                # xoo = list(map(mkdict, legend, foo.split(delim)))
                # nodes.append(dict(xoo))
                nodes.append(foo.split(delim)[1])
    return nodes


def main():
    '''
        read in a file into configparser
    '''
    for result in decode(SIGNAL, delim='{'):
        print(f'== ident {result["ident"]}, SNR {result["SNR"]}')

    exit(0)
    foo = toml_parse(NACKFILE)
    print(f'foo {foo}')
    exit(0)
    if (config := parse(NACKFILE)) != None:
        print(f'parse defaults {config.defaults()}')
        exit(0)
    if (config := reparse(NACKFILE)) != None:
        print(f'reparse defaults {config.defaults()}')
        exit(0)
    if (config :=  toml_parse(NACKFILE)) != None:
        print(f'tomllll')
        exit(0)


main()
