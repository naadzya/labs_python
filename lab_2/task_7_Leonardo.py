#Task 7
import time
import argparse

__all__ = ['leonardonum']

def calculate_time(func):
    """Calculates the time during use the function func
    """
    def inner(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        ending = time.time()
        print('It takes %.5f seconds' % (ending-start))
        return value
    return inner

@calculate_time
def leonardonum(n: int):
    """Returns n-th number in Leonardo sequence.
    By definition L(n) = 1 if n = 0 or n = 1 else L(n-1) + L(n-2) + 1
    """
    if not isinstance(n, int) or n < 0:
        print('Wrong input')
        return
    if n == 0 or n == 1:
        return 1
    L0 = L1 = 1
    for i in range(2, n+1):
        Ln = L1 + L0 + 1
        L0 = L1
        L1 = Ln
    return Ln

def main():
    parser = argparse.ArgumentParser(description='Leonardo sequence')
    parser.add_argument('-n', type=int,
                        help='to find n-th number in Leonardo sequence')
    args = parser.parse_args()
    if not args.n:
        val = input('Enter your number: ')
        while val != 'exit':
            while not val.isdigit():
                print('Wrong input. Try again')
                val = input()
            val = int(val)
            print(f'The {val}th number in Leonardo sequence:\n{leonardonum(val)}')
            val = input('Enter your number or write exit to close the programm: ')
        return
    val = args.n
    print(f'The {val}th number in Leonardo sequence:\n{leonardonum(int(val))}')

if __name__ == '__main__':
    main()
        
