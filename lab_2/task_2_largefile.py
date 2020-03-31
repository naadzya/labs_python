#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random
import string
import argparse
import sys
import time

__all__ = ['generate_file']

def progress_bar(it, total):
    fillwith = '█'
    dec = 1
    leng = 50
    percent = ('{0:.' + str(dec) + 'f}').format(100 * (it/float(total)))
    fill_length = int(leng * it // total)
    bar = fillwith * fill_length + '-' * (leng - fill_length)
    print('\rProgress |%s| %s%% Complete' % (bar, percent), end="\r")

def calculate_time(func):
    """Calculates the time during use the function func
    """
    def inner(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        ending = time.time()
        print('\nDone! It takes %.5f seconds' % (ending-start))
        return value
    return inner

def random_string(strlen: int):
    """Generates a random string of length strlen
    """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(strlen))

def random_line(wordsnum: int, L: tuple):
    """Generates a random line
    The quantity of words in the line is wordsnum
    The length of each word is a random number in the range L
    L is a tuple
    """
    counter = 0
    strline = ''
    while counter < wordsnum - 1:
        wordlen = random.choice(range(L[0], L[1] + 1))
        strline += random_string(wordlen) + ' '
        #Creates new word with space
        
        counter += 1
    wordlen = random.choice(range(L[0], L[1] + 1))
    strline += random_string(wordlen)
    return strline

@calculate_time
def generate_file(Mb, K=(10,100), L=(3, 10), filename='largefile.txt'):
    """Generates a file with size Mb (in MB),
    the quantity of words in each line is a random number in the range K,
    the length of each word is a random number in the range L
    K and L are tuples
    """
    inbytes = int(Mb * 1024**2)   #Size of file in bytes
    f = open(filename, 'w+')
    counter = 0
    if K[0] > K[1] or L[0] > L[1]:
        print('Wrong range')
        return
    while counter < inbytes:
        progress_bar(counter, inbytes)
        wordsnum = random.choice(range(K[0], K[1] + 1))
        #The number of words in newline
        newline = random_line(wordsnum, L) + '\n'   #Create newline
        if counter + len(newline) + 1 < inbytes:
            #If the newline doesn't makes the size of file bigger than Mb
            f.write(newline)
            counter += len(newline) + 1  #Because in UTF8 len('\n') == 2
        else:
            diff = inbytes - counter   #The size of the remaining space
            linelen = 0
            while linelen < diff:
                #While the line doesn't complete the file
                wordlen = random.choice(range(L[0], L[1] + 1))
                newword = random_string(wordlen)
                if linelen + len(newword) <= diff:
                    #If the newword doesn't makes the size of file
                    #bigger than Mb
                    f.write(newword + ' ')
                    linelen += len(newword + ' ')
                else:
                    #Write the last word to complete the file
                    letters = (string.ascii_lowercase
                            + string.ascii_uppercase)
                    chardiff = diff - linelen
                    newword = ''.join(random.choice(letters)
                                      for i in range(chardiff))
                    f.write(newword)
                    linelen += chardiff
            counter += linelen
    progress_bar(counter, inbytes)
    f.close()

def main():
    args = sys.argv[1:]
    if not args:
        val = input('Enter the size of your file in MB: ')
        K = input('Enter the words range as (a, b): ')
        L = input('Enter the words\' length range as (a, b): ')
        while val != 'exit':
            while True:
                try:
                    val = float(val)
                    K = tuple(map(int, K[1:-1].split(',')))
                    L = tuple(map(int, L[1:-1].split(',')))
                except (ValueError, IndexError):
                    print('Wrong input. Try again')  
                    val = input('Enter the size of your file in MB: ')
                    K = input('Enter the words range as (a, b): ')
                    L = input('Enter the words\' length range as (a, b):')
                else:
                    break     
            generate_file(val, K, L)
            val = input('Enter the size of your file in MB or write \'exit\'\
 to close the programm: ')
    else:
        try:
            float(args[0])
            words_l_bound = args[1]
            words_r_bound = args[2]
            lett_l_bound = args[3]
            lett_r_bound = args[4]
            words = tuple(map(int, [words_l_bound[1:-1], words_r_bound[:-1]]))
            lett = tuple(map(int, [lett_l_bound[1:-1], lett_r_bound[:-1]]))
        except (ValueError, IndexError):
            print('Wrong input. Try again')
        else:
            size = float(args[0])
            print('The size of your file: ', size)
            words = tuple(map(int, [words_l_bound[1:-1], words_r_bound[:-1]]))
            print('The words range: ', words)
            lett = tuple(map(int, [lett_l_bound[1:-1], lett_r_bound[:-1]]))
            print('The words\' length range', lett)
            generate_file(size, words, lett)    

if __name__ == "__main__":
    main()
 







