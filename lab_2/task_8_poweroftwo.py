#Task 8
import time

def calculate_time(func):
    """Calculates the time during use the function func
    """
    def inner(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        ending = time.time()
        print(f'It takes {ending-start} seconds')
        return value
    return inner

@calculate_time
def is_power_of_two(n: int):
    inbin = str(bin(n))[3:]
    return inbin == '0'*len(inbin)

def main():
    val = input('Enter your number: ')
    while val != 'exit':
        while not val.isdigit():
            print('Wrong input. Try again')
            val = input()
        print('It\'s power of 2' if is_power_of_two(int(val))
              else 'It\'s not power of two')
        val = input('Enter your number or write exit to \
close the programm: ')

if __name__ == '__main__':
    main()
