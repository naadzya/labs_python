#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import argparse

__all__ = ['is_power_of_two']

def is_power_of_two(n: int):
    inbin = str(bin(n))[3:]
    return inbin == '0'*len(inbin)

def main():
    parser = argparse.ArgumentParser(description='Power of two')
    parser.add_argument('-n', type=int,
                        help='A number that supposed to be checked')
    args = parser.parse_args()
    if not args.n:
        val = input('Enter your number: ')
        while val != 'exit':
            while not val.isdigit():
                print('Wrong input. Try again')
                val = input()
            print('It\'s power of 2' if is_power_of_two(int(val))
                  else 'It\'s not power of two')
            val = input('Enter your number or write "exit" to close the programm: ')
        return
    print('It\'s power of 2' if is_power_of_two(args.n)
          else 'It\'s not power of two')

if __name__ == '__main__':
    main()
