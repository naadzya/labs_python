#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse

__all__ = ['from_json']

class JSONError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
           self.message = None

    def __str__(self):
        if self.message:
            return 'JSONError was raised by {0}'.format(self.message)
        return 'JSONError has been raised'

def read_from_file(filename: str):
    with open(filename) as f:
        line = f.readline()
    return line[:-1]

def to_int(text):
    """Deserialize text containing a JSON document to a Python object int.
    """
    int_text = 0
    if not text.startswith('-'):
        for ch in text:
            int_text *= 10
            int_text += (ord(ch)-48) * 10
        return int_text//10
    neg = to_int(text[1:])
    return -neg

def to_float(text):
    dot = text.find('.')       #The index of dot in text
    beforedot = to_int(text[:dot])
    afterdot = to_int(text[dot+1:])
    if beforedot < 0:
        afterdot *= -1
    return beforedot + afterdot * 0.1**len(text[dot+1:])
    

def onedim_to_obj(text):
    """Deserialize text containing a 1D array or dict to a Python list
    """
    if len(text) == 2:
        return []
    bracket_index = text.find('[')    #The index of first bracket
    brace_index = text.find('{')      #The index of first brace
    if brace_index == -1:             #If it is array
        intext = text[1:-1].split(', ')
        list_text = []
        for item in intext:
            list_text.append(from_json(item))
        return list_text
    intext = text[1:-1].split()       #All characters inside braces
    dict_text = {}
    for key, val in zip(intext[::2], intext[1::2]):
        key = key.replace(':', '')
        val = val.replace(',', '')
        dict_text.update({from_json(key): from_json(val)})
    return dict_text

def is_there_iter(text):
    """
    Return True if there is at least one nested
    list or dict in text
    """
    bracket_index = text[1:-1].find('[')    #The index of first bracket
    brace_index = text[1:-1].find('{')      #The index of first brace
    return bracket_index + brace_index != -2

def collect_brackets(text):
    """
    Return sorted dict for list in string format.
    Key is the index of '[' and value is a corresponding ']'
    """
    opened = []
    closed = []
    for i in range(1, len(text)-1):
        if text[i] == '[':
            opened.append(i)
        elif text[i] == ']':
            closed.append(i)
    i = 0
    brackets_index = []
    while opened:
        if (i + 1 == len(opened)
            or opened[i] < closed[0] < opened[i + 1]):
            open_bracket = opened.pop(i)
            cl_bracket = closed.pop(0)
            brackets_index.append((open_bracket, cl_bracket))
            i -= 1
        else:
            i += 1
    brackets_index.sort(key=lambda tup: tup[0])
    return brackets_index

def remove_sublists(indices: list):
    """
    Remove indices of sublists in list of tuples with indices
    of opened-closed brackets which corresponds to text containing an array
    """
    wrap_ind = 0   #The index if the first list-wrapper
    i = 1
    while i < len(indices):
        #Check for sublists
        if (indices[i][0] > indices[wrap_ind][0]
            and indices[i][1] < indices[wrap_ind][1]):
            indices.pop(i)
        else:
            wrap_ind = i
            i += 1

def array_to_list(text):
    """
    Deserialize text containing an array to a Python list
    """
    if not is_there_iter(text):
        return onedim_to_obj(text)
    #List of tuples with indices of opened-closed brackets
    indices = collect_brackets(text)
    remove_sublists(indices)
    list_obj = []
    start = 1
    for op, cl in indices:
        #The part of array without lists
        nolists = text[start:op].split(', ')
        for item in nolists[:-1]:
            list_obj.append(from_json(item))
        list_obj.append(array_to_list(text[op:cl+1]))
        start = cl + 3
    endnolists = text[indices[-1][1]+3:-1].split(', ')
    for item in endnolists:
        if item == '':
            break
        list_obj.append(from_json(item))
    return list_obj
    
def obj_to_dict(text):
    """Deserialize text containing a JSON object to a Python list
    """
    pass

def from_json(text: str):
    """Deserialize text containing a JSON document to a Python object.
    """
    if text.startswith('\"') and text.endswith('\"'):
        return text[1:-1]
    if text == 'null':
        return
    if text == 'true':
        return True
    if text == 'false':
        return False
    if text.isdigit() or text[1:].isdigit():
        return to_int(text)
    dot = text.find('.')       #The index of dot in text
    flag = ((text[:dot].isdigit() or text[1:dot].isdigit())
            and text[dot+1:].isdigit())
    if flag:
        return to_float(text)
    if text.startswith('[') and text.endswith(']'):
        return array_to_list(text)
    if text.startswith('{') and text.endswith('}'):
        return obj_to_dict(text)
    raise JSONError(text)

def main():
    parser = argparse.ArgumentParser(description='From JSON to a Python formatted str')
    parser.add_argument('-obj', type=str, help='JSON object')
    args = parser.parse_args()
    if not args.obj:
        val = input('Press 1 if you want to enter your JSON string-object\n'\
            'If you want to read your object from a file, enter the name '\
            'of the file\n')
        val = (input('Enter your JSON object\n') if val == '1'
               else read_from_file(val))
    else:
        val = args.obj
    print(f"A Python formatted str:\n{from_json(val)}")
    
if __name__ == '__main__':
    main()
        
