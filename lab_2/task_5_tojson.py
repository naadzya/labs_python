#!/usr/bin/env python
#-*- coding:utf-8 -*-

from math import modf
import argparse

__all__ = ['to_json']

def read_from_file(filename: str):
    with open(filename) as f:
        line = f.readline()
        return eval(line)

def int_to_json(obj: int):
    """Serialize int object to a JSON formatted str
    """
    json_int = []
    num = abs(obj)
    while num:
        json_int.append(chr(ord("0") + num%10))
        num //= 10
    jstr = "".join(reversed(json_int))
    return "-" + jstr if obj < 0 else jstr

def float_to_json(obj: float):        #Doesn't work well
    """Serialize float object to a JSON formatted str
    """
    whole_str = int_to_json(int(obj))
    frac = modf(obj)[0]
    frac_str = ""
    while frac:
        obj *= 10
        #print(obj)
        frac_str += int_to_json(int(obj) % 10)
        frac = modf(obj)[0]
        #print(frac_str)
    return whole_str + "." + frac_str

def str_to_json(obj: str):
    return '\"' + obj +'\"'

def onedim_to_json(obj):
    """Serialize 1D list tuple or dict to a JSON formatted str
    """
    if isinstance(obj, (tuple, list)):
        jstr = "["
        for subobj in obj:
            jstr += to_json(subobj) + ", "
        return jstr[:-2] + "]"

def is_there_iter(A):
    """Returns True if there is at least one nested list,
    tuple or dict in A
    """
    return any(isinstance(i, (list, tuple)) for i in A)

def array_json(obj):
    """Serialize list or tuple to a JSON formatted str
    """
    jstr = "["
    if is_there_iter(obj):
        for subobj in obj:
            if isinstance(subobj, dict):
                jstr += dict_to_json(subobj)
            elif not isinstance(subobj, (list, tuple, dict)):
                jstr += to_json(subobj)
            elif not (is_there_iter(subobj)):
                jstr += onedim_to_json(subobj)
            else:
                jstr += array_json(subobj)
            jstr += ", "
        return jstr[:-2] + "]"
    return onedim_to_json(obj)


def dict_to_json(obj):
    """Serialize a dict to a JSON formatted str
    """
    jstr = '{'
    for key, value in obj.items():
        flag = (isinstance(key, (str, int, float, bool))
                    or key is None)
        if not flag:
            raise ValueError
        if isinstance(key, str):
            jstr += to_json(key) + ': '
        else:
            jstr += str_to_json(to_json(key)) + ': '
        if not isinstance(value, dict):
            jstr += to_json(value)
        else:
            jstr += dict_to_json(value)
        jstr += ", "
    return jstr[:-2] + "}"
        

def to_json(obj):
    """Serialize obj to a JSON formatted str
    """
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        if obj is True:
            return "true"
        return "false"
    if isinstance(obj, int):
        return int_to_json(obj)
    if isinstance(obj, float):
        return float_to_json(obj)
    if isinstance(obj, str):
        return str_to_json(obj)
    if isinstance(obj, (list, tuple)):
        return array_json(obj)
    if isinstance(obj, dict):
        return dict_to_json(obj)
    raise ValueError

def main():
    parser = argparse.ArgumentParser(description='From bject to a JSON formatted str')
    parser.add_argument('-obj', type=str, help='Python object')
    args = parser.parse_args()
    if not args.obj:
        val = input('Press 1 if you want to enter your object\n'\
            'If you want to read your object from a file, enter the name '\
            'of the file\n')
        val = (eval(input('Enter your object\n')) if val == '1'
               else read_from_file(val))
    else:
        val = eval(args.obj)
    print(f"A JSON formatted str:\n{to_json(val)}")

if __name__ == '__main__':
    main()
