'''
Created on Oct 29, 2016

@author: andrew
'''
import os
import errno


def print_table(table):
    tableStr = ''
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        tableStr += "| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |"
        tableStr += '\n'
    return tableStr

def discord_trim(str):
    result = []
    trimLen = 0
    lastLen = 0
    while trimLen <= len(str):
        trimLen += 1999
        result.append(str[lastLen:trimLen])
        lastLen += 1999
    return result

def embed_trim(str):
    result = []
    trimLen = 0
    lastLen = 0
    while trimLen <= len(str):
        trimLen += 1023
        result.append(str[lastLen:trimLen])
        lastLen += 1023
    return result

def list_get(index, default, l):
    try:
        a = l[index]
    except IndexError:
        a = default
    return a

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        
def get_positivity(string):
    if isinstance(string, bool): # oi!
        return string
    lowered = string.lower()
    if lowered in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
        return True
    elif lowered in ('no', 'n', 'false', 'f', '0', 'disable', 'off'):
        return False
    else:
        return None
    
def fuzzy_search(list_to_search:list, key, value):
    """Fuzzy searches a list for a dict with a key "key" of value "value" """
    try:
        result = next(a for a in list_to_search if value.lower() == a.get(key, '').lower())
    except StopIteration:
        try:
            result = next(a for a in list_to_search if value.lower() in a.get(key, '').lower())
        except StopIteration:
            return None
    return result    

def parse_args(args):
    out = {}
    index = 0
    for a in args:
        if a == '-b' or a == '-d':
            if out.get(a.replace('-', '')) is None: out[a.replace('-', '')] = list_get(index + 1, None, args)
            else: out[a.replace('-', '')] += ' + ' + list_get(index + 1, None, args)
        elif a.startswith('-'):
            nextArg = list_get(index + 1, None, args)
            if nextArg is None or nextArg.startswith('-'): nextArg = True
            out[a.replace('-', '')] = nextArg
        else:
            out[a] = True
        index += 1
    return out

    