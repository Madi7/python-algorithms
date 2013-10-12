"""
Practicing search algorithms
"""


def linear_search(array, target, size=None):
    """
    array, size of array, and target (item you're searching for)
    """
    size = size or len(array)
    comparisons = 0

    for index in range(size):
        comparisons = comparisons + 1
        if array[index] == target:
            return '%s comparisons' % comparisons, index
    return '%s comparisons' % comparisons, -1


def binary_search(array, target, size=None):
    start = 0
    end = size or len(array)-1
    answer = None

    comparisons = 0
    while start <= end:
        comparisons = comparisons + 1
        middle = (end+start)/2
        if array[middle] == target:
            answer = middle
            break
        elif target < array[middle]:
            end = middle - 1
        else:
            start = middle + 1

    return '%s comparisons' % comparisons, answer


if __name__ == '__main__':
    """
    Calls search methods.  Accepts CLI arguments
    """
    import sys
    from getopt import getopt, GetoptError

    try:
        kwargs, args = getopt(sys.argv[1:], 'ho:v', ['help', 'output=', 'array=', 'target='])
    except GetoptError as e:
        kwargs, args = dict(), tuple()

    kwargs = dict(kwargs)
    size, target = 1000, 50  # default: size, target

    if len(args) == 2:
        size, target = [int(i) for i in args]

    array = tuple(range(size))

    print 'linear_search', linear_search(array, target, len(array))
    print 'binary_search', binary_search(array, target, len(array))
