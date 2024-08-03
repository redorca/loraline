'''
    figure out how to use a plain text file as a config file suitable for ConfigParser
'''

import configparser
import tomllib

ACKFILE  = "/tmp/ack"
NACKFILE = "/tmp/nack"


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

def smersh(filename, legend, delim=':'):
    '''
        Convert a text file of data lines into a list of dictoinaries using
        legend as the keys in the dictionary in the order to be decoded from the text line.
    '''
    nodes = list()
    with open(filename, 'r') as spot:
        while (foo := spot.readline().strip()):
            # print(f'foo {foo.split(delim)}')
            xoo = list(map(mkdict, legend, foo.split(delim)))
            nodes.append(dict(xoo))
    return nodes

def main():
    '''
        read in a file into configparser
    '''
    # network = smersh('/tmp/nodes', ["Name", "ID", "GPS"])
    # [ print(f'Name {line["Name"]}') for line in network ]
    # exit(0)
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
