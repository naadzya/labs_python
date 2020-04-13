#Task 1
def input_list():
    """ Reads entered numbers from console
        in list
    """
    userstr = input('Enter a list of numbers or elements '\
                    'separated by space:\n')
    userlist = userstr.split()
    for i in range(len(userlist)):
        if userlist[i].isdigit():   #If the list contains only the numbers
            userlist[i] = int(userlist[i])
        else:
            try:
                float(userlist[i])
            except ValueError:
                print('It\'s not a list of numbers. Try again')
                return
            userlist[i] = float(userlist[i])
    return userlist

def list_from_file(filename: str):
    """ Reads numbers from a file in list
    """
    try:
        f = open(filename)
    except FileNotFoundError:
        print('The file is not found. Try again')
        return
    userlist = []
    for line in f:
        for i in line.split():
            try:
                int(i)
            except ValueError:
                continue
            userlist.append(int(i))
    f.close()
    if not userlist:
        print('There is no numbers in your file, Try again')
        return
    return userlist

def sqrt_decomposition(a: list, l: int, r: int) -> int:
    """ Counts sum of the elements in list a in range from l to r
    """
    n = len(a)
    length = int(n ** 0.5) + 1
    # Length of one block. Adding 1 for the remaining elements
    b = [0] * (length)
    for i in range(n):
        b[i // length] += a[i]   # Counting sum in each block
    #lrSum = 0
    lside = l // length          # The number of block with element a[l]
    rside = r // length          # The number of block with element a[r]
    lrSum = 0
    if lside == rside:
        # If l and r are in one block just counting the sum in list a
        lrSum = sum(a[l:r+1])
        return lrSum
    #Counting the sum in the block with element a[l] from this element
    lrSum = sum(a[l:(lside+1) * length]) 
    #Counting the sum in the blocks between l and r
    lrSum += sum(b[lside+1 : rside])
    #Counting the sum in the block with element a[r] from this element
    lrSum += sum(a[rside*length : r+1])
    return lrSum

def sqrt_decomp_test(a: list, l, r):
    """ Test for sqrt_decomposition
    """
    first_sum = sqrt_decomposition(a, l, r)
    second_sum = sum(a[l:r+1])
    return first_sum == second_sum

def main():
    newlist = []
    var = input('Press 1 if you want to enter your list of numbers\n'\
            'If you want to read your list from a file, enter the name '\
            'of the file\n')
    while var != 'exit':
        print(var)
        while not newlist:
            if var == '1':
                newlist = input_list()
            else:
                newlist = list_from_file(var)
                if not newlist:
                    var = input()
        print('Your list: ', newlist)
        l_bound = input('Enter the left boundary for your sum: ')
        while not l_bound.isdigit():
            print('It\'s not number. Try again')
            l_bound = input()
        l_bound = int(l_bound)
        r_bound = input('Enter the right boundary for your sum: ')
        while not r_bound.isdigit():
            print('It\'s not number. Try again')
            r_bound = input()
        r_bound = int(r_bound)
        print(f'The sum from {l_bound}th element to {r_bound}th element',
              f'in your list: {sqrt_decomposition(newlist, l_bound, r_bound)}')
        var = input('\nPress 1 if you want to enter your list of numbers\n'\
                'If you want to read your list from a file, enter the name '\
                'of the file. Enter "exit" to close the program.\n')
        
if __name__ == '__main__':
    main()












    
