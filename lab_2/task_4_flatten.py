#Task 4
import argparse

__all__ = ['flatten_it', 'flatten']

def flatten_it(A):
    """Generator for flatten"""
    if isinstance(A, (list, tuple)):
        F = [iter(A)]        # Create an iterator
        while F:
            for it in F[-1]:    # The deepest list
                if isinstance(it, (list, tuple)):
                    F.append(iter(it))
                    break
                else:
                    yield it
            else:
                F.pop()

def flatten(A):
    """
    Returns a copy of an given list, tuple or their combinations
    collapsed into one dimension
    """
    flatt = []
    for x in flatten_it(A):
        flatt.append(x)
    return tuple(flatt) if isinstance(A, tuple) else flatt
    
                    
def test_flatten_it():
    """A test for the function flatten_it
    """
    arr = ([1, 2, (3, (4, 5, [6]), 7), [8, [[9, 10]]], 11,
           [12, (13, [14, [[15]]]), 16], [17, [[(18), 19]]]], 20)
    flatt = flatten(arr)
    print(f'The original:\n{arr}', f'Flattened:\n{flatt}', sep='\n')    

def main():
    parser = argparse.ArgumentParser(description=
                                     'Your list or tuple that needs to be flattened')
    parser.add_argument('-arr', '--array', type=str, help='Needs to be flattened')
    args = parser.parse_args()
    val = args.array
    if not val:
        val = input('Enter a list or tuple:\n')
        while True:
            try:
                eval(val)
            except (NameError, SyntaxError):
                print('Wrong input, try again')
                val = input('Enter your list or tuple:\n')
            else:
                val = eval(val)
                if not isinstance(val, (list, tuple)):
                    print('Wrong input, try again')
                    val = input('Enter a list or tuple:\n')
                else: break
        print(f'Flattened:\n{flatten(val)}')
        return
    while True:
        try:
            val = eval(val)
        except (NameError, SyntaxError):
            print('Wrong input, try again')
            val = input('Enter your list or tuple:\n')
        else:
            if not isinstance(val, (list, tuple)):
                print('Wrong input, try again')
                val = input('Enter a list or tuple:\n')
            else:
                break   
    print(f'Flattened:\n{flatten(val)}')

if __name__ == "__main__":
    main()



