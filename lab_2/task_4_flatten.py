#Task 4
import time

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

def is_there_iter(A):
    """Returns True if there is at least one nested list in A
    """
    return any(isinstance(i, (list, tuple)) for i in A)

@calculate_time
def flatten_it(A):
    """Returns a copy of an given list, tuple or their combinations
    collapsed into one dimension
    """
    if isinstance(A, (list, tuple)):
        F = list(A)        #Copy of A
        while is_there_iter(F):   #Flattens while there won't be
            i = 0                 #any nested objects
            while i < len(F):
                if isinstance(F[i], (list, tuple)):
                    F[i] = list(F[i])
                    nested = F.pop(i)       #Removes the nested list
                    for j in range(len(nested)):   #Inserts all elements
                        F.insert(i+j, nested[j])   #from the nested list
                i += 1
        if isinstance(A, tuple):
            return tuple(F)
        return F
                    
def test_flatten_it():
    """A test for the function flatten_it
    """
    arr = ([1, 2, (3, (4, 5, [6]), 7), [8, [[9, 10]]], 11,
           [12, (13, [14, [[15]]]), 16], [17, [[(18), 19]]]], 20)
    flattarr = flatten_it(arr)
    print(f'The original:\n{arr}', f'Flattened:\n{flattarr}', sep='\n')    

def main():
    test_flatten_it()

if __name__ == "__main__":
    main()
