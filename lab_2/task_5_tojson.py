#!/usr/bin/env python
#-*- coding:utf-8 -*-

from math import modf

__all__ = ['to_json']

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
    jstr = "{"
    for key, value in obj.items():
        flag = (isinstance(key, (str, int, float, bool))
                    or key is None)
        if not flag:           #If key can be serialized for json object
            raise ValueError
        if isinstance(key, str):
            jstr += to_json(key) + ": " + to_json(value) + ", "
        else:
            jstr += (str_to_json(to_json(key)) + ": "
                     + to_json(value) + ", ")
    return jstr[:-2] + "}"

def is_there_iter(A):
    """Returns True if there is at least one nested list,
    tuple or dict in A
    """
    if isinstance(A, dict):
        return any(isinstance(A[k], dict) for k in A.keys())
    return any(isinstance(i, (list, tuple, dict)) for i in A)

def is_there_dict(A):
    return any(isinstance(A[k], dict) for k in A.keys())

def array_json(obj):
    """Serialize list or tuple to a JSON formatted str
    """
    jstr = "["
    if is_there_iter(obj):
        for subobj in obj:
            if not isinstance(subobj, (list, tuple, dict)):
                jstr += to_json(subobj)
            elif not (is_there_iter(subobj)):
                jstr += onedim_to_json(subobj)
            elif isinstance(subobj, dict):
                jstr += dict_to_json(subobj)
            else:
                jstr += array_json(subobj)
            jstr += ", "
        return jstr[:-2] + "]"
    return onedim_to_json(obj)


def dict_to_json(obj):
    """Serialize a dict to a JSON formatted str
    """
    jstr = '{'
    if is_there_dict(obj):
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
    return onedim_to_json(obj)
        

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
    print(to_json({1: "one", "2": "two", 3: [True, "str", (None, [])],
                   4: {"sub": 5, "newsub": (1,)}}))

if __name__ == '__main__':
    main()
