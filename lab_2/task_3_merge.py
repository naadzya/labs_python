#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import io
import argparse
from memory_profiler import profile
from task_2_largefile import *

def lines_merge(A, B, key=lambda word: word):
    """
    Merges two sorted lists.
    Key is a function that will be applied to each item in the
    Iterable and it returns a value based on the passed argument
    """
    C = [0]*(len(A)+len(B))
    i = k = n = 0
    while i < len(A) and k < len(B):
        if key(A[i]) <= key(B[k]):
            C[n] = A[i]
            i += 1
        else:
            C[n] = B[k]
            k += 1
        n += 1
    #One of the loops works 0 times
    while i < len(A):
        C[n] = A[i]
        i += 1
        n += 1
    while k < len(B):
        C[n] = B[k]
        k += 1
        n += 1
    return C

def line_merge_sort(line, key=lambda word: word):
    """
    Merge sort for a list.
    Key is a function that will be applied to each item in the
    Iterable and it returns a value based on the passed argument
    """
    if len(line) <= 1:
        return
    middle = len(line) // 2
    left = line[:middle]
    right = line[middle:]
    line_merge_sort(left, key)
    line_merge_sort(right, key)
    sorted_line = lines_merge(left, right, key)
    line[:] = sorted_line[:]

def sort_smallfile(file: open, key=lambda word: word):
    """
    Merge sort for one small file.
    """
    A = []
    for line in file:
        #Check the emptiness of a line
        if len(line) >= 1:
            #Sort each line
            words = line.split()
            line_merge_sort(words, key)
            words = ' '.join(words)
            A.append(words)
    line_merge_sort(A, key)        #Sort the list of lines
    A.append('')
    file.seek(0)
    for item in range(len(A) - 1):
        if A[item+1] != '': 
            file.write(A[item] + '\n')
        else:
            file.write(A[item])

@profile
def external_merge_sort(inputf: open, outputf: open,
                        key=lambda word: word):
    """
    External merge sort for large file 'inputf'.
    Divide inputf file into n parts and sort them in outputf.
    Key is a function that will be applied to each item in the
    Iterable and it returns a value based on the passed argument
    """
    blocks = []
    while True:
        newblock = inputf.readline()
        if not len(newblock):
            break
        if newblock.find('\n') == -1:
            newblock += '\n'
        smallf = io.StringIO()
        smallf.write(newblock)
        smallf.seek(0)
        sort_smallfile(smallf, key)
        blocks.append(smallf)
        smallf.seek(0)
    #n-way merge sort
    #Reading by charachters
    lines = [text.readline() for text in blocks]
    N = len(lines)
    counter = 0
    while lines:
        progress_bar(counter, N)
        min_char = min(lines, key=key)
        outputf.write(min_char)
        min_index = lines.index(min_char)
        next_char = blocks[min_index].read(1)
        if next_char:
            lines[min_index] = next_char
        else:
            del(lines[min_index])
            blocks[min_index].close()
            del(blocks[min_index])
        counter += 1
    progress_bar(N, N)
    print('\n')


def main():
    parser = argparse.ArgumentParser(description='External merge sort')
    parser.add_argument('-size', '--MB', type=float, help='Size of the file')
    parser.add_argument('-nameop', type=str,
                        help='Name of file that supposed to be sorted')
    parser.add_argument('-namecl', type=str,
                        help='Name of file that supposed to be sorted')
    args = parser.parse_args()
    if not any([args.nameop, args.namecl, args.MB]):
        val = float(input("Enter the size of your file in MB: "))
        generate_file(val, (3, 8), (4, 14), "smallfile.txt")
        f = open("smallfile.txt", 'r')
        fs = open("smallsorted.txt", 'w+')
        external_merge_sort(f, fs, key=len)
        f.close()
        fs.close()
        return
    print('The size of your file: ', args.MB)
    if not args.nameop:
        args.nameop = "smallfile.txt"
        generate_file(args.MB, (3, 8), (4, 14), args.nameop)
    if not args.namecl:
        args.namecl = "smallsorted.txt"
    f = open(args.nameop, 'r')
    fs = open(args.namecl, 'w+')
    external_merge_sort(f, fs, key=len)
    f.close()
    fs.close()    

if __name__ == "__main__":
    main()

