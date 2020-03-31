#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import sys

__all__ = ['is_power_of_two']

def is_power_of_two(n: int):
    inbin = str(bin(n))[3:]
    return inbin == '0'*len(inbin)

def main():
    args = sys.argv[1:]
    if not args:
        val = input('Enter your number: ')
        while val != 'exit':
            while not val.isdigit():
                print('Wrong input. Try again')
                val = input()
            print('It\'s power of 2' if is_power_of_two(int(val))
                  else 'It\'s not power of two')
            val = input('Enter your number or write exit to \
close the programm: ')
        return
    val = args[0]
    if not val.isdigit():
        print('Wrong input')
        return
    print('It\'s power of 2' if is_power_of_two(int(val))
                  else 'It\'s not power of two')

if __name__ == '__main__':
    main()
