"""
Work in progress algorithms. (WIP)
I don't want to use them, but I'm not ready to toss either.
"""


def selection_sort(array):
    """
    """
    iterations = 0
    for i in range(len(array)):
        iterations = iterations + 1
        for j in range(i+1, len(array)):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]

    return array, '%s iterations' % iterations


def merge(array, end1, end2):
    """
    """
    i = 0
    j = end1
    k = 0

    temp = []

    # print 'merge() called'

    print 'i', i
    print 'j', j
    print 'end1', end1
    print 'end2', end2

    while i < end1 and j < end2:
        if(array[i] < array[j]):
            temp[k] = array[i]
            i = i + 1
            k = k + 1
        else:
            temp[k] = array[j]
            j = j + 1
            k = k + 1
    while i < end1:
        temp[k] = array[i]
        i = i + 1
        k = k + 1
    while j < end2:
        temp[k] = array[j]
        j = j + 1
        k = k + 1

    # print 'array', array
    # print 'temp', temp
    # print 'end2', end2

    # for i in range(end2):
    #     array[i] = temp[i]

    array = temp


def merge_sort(array):
    """
    Split array up until you have multiple
    arrays, each of size 1.  Then merge the arrays
    in order until you have on array again.
    """
    size = len(array)

    for i in range(1, size):
        i = i * 2
        j = 0
        for j in range(size-i):
            j = j + i * 2
            merge(array, i, min(i * 2, size - j))

    return array


def quick_sort(array):
    """
    We partition arrays by picking a pivot point.
    Then we pick a point at the beginning and end of our array.
    We then compare the end-points to the pivot point until
    we find an item that is relatively smaller and bigger than
    our pivot point respectively.  We then swap the values.
    We continue to do this until our 2 end-points reach our pivot
    point.  Then we take our partions and find new pivot points
    on those partitions.  We repeat this until there is no partition
    with more than one element.  At this point our array is sorted.
    """
    from random import choice

    size = len(array)

    if size < 2:
        return array

    pivot = choice(array)  # just the value

    lower = 0
    upper = len(array) - 1  # array index starts with 0

    while lower < upper:
        while array[lower] < pivot:
            lower += 1
        while array[upper] > pivot:
            upper -= 1

        # swap
        array[lower], array[upper] = array[upper], array[lower]

    print 'manual', array[lower+1:size-lower-1]
    print 'automatic', array[lower+1:]

    quick_sort(array[:lower])
    quick_sort(array[lower+1:size-lower-1])

    return array


def quick_sort2(array):
    """
    We partition arrays by picking a pivot point.
    Then we pick a point at the beginning and end of our array.
    We then compare the end-points to the pivot point until
    we find an item that is relatively smaller and bigger than
    our pivot point respectively.  We then swap the values.
    We continue to do this until our 2 end-points reach our pivot
    point.  Then we take our partions and find new pivot points
    on those partitions.  We repeat this until there is no partition
    with more than one element.  At this point our array is sorted.

    This looks more like an alternate version of the merge sort.
    """
    # from random import choice
    less = []
    equal = []
    greater = []

    if len(array) < 2:
        return array  # this is where all 1-item arrays finally exit

    # pivot = choice(array)
    pivot = array[0]
    for i in array:
        print 'blah'
        if i < pivot:
            less.append(i)
        if i == pivot:
            equal.append(i)
        if i > pivot:
            greater.append(i)

    return quick_sort(less) + quick_sort(equal) + quick_sort(greater)


if __name__ == '__main__':
    """
    Calls sorting algorithms and prints return values
    """
    import sys
    from random import randint
    from getopt import getopt, GetoptError

    try:
        kwargs, args = getopt(sys.argv[1:], 'ho:v', ['help', 'output'])
    except GetoptError as e:
        kwargs, args = dict(), tuple()

    size = int(args[0]) if args else 100  # size of array
    unsorted = [randint(1, 1000) for i in range(1, size+1)]

    print 'unsorted', unsorted
    print 'selection_sort', selection_sort(list(unsorted))
    print 'merge_sort', merge_sort(list(unsorted))
    print 'quick_sort', quick_sort(list(unsorted), 0, len(list(unsorted))-1)
    print 'quick_sort2', quick_sort2(list(unsorted))

