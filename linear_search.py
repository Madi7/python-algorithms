


def linear_search(array, n, target):
    """
    array, size of array, and target (item you're searching for)
    """

    comparisons = 0
    for index in range(n):
        comparisons = comparisons + 1
        if array(index) == target:
            return index
    return -1


def binary_search(array, n, target):
    start = 0
    end = n-1
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

    return comparisons, answer


if __name__ == '__main__':
    array = tuple(range(1000))

    print 'linear_search', linear_search(array, len(array), 32)
    print 'binary_search', binary_search(array, len(array), 32)
