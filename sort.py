"""
Practicing sort algorithms
"""

def bubble_sort(array):
    """
    Compare the first two items, then swap them if they're out of order.
    Continue doing this until you've reached the end of the array.
    At this point the last entry is the largest item in the array.
    We continue this unti the array is fully sorted.

    The largest bubbles it's way up to the end of the array.
    This is why the call it bubble sort.

    Method: Exchange (swap) sort
    Best case: O(n)
    Average case: O(n2)
    Worst case: O(n2)
    """
    sorted = False
    length = len(array)-1
    iterations = 0

    while not sorted:
        sorted = True
        # optimize; only iterate over the subset
        # the left portion aka unsorted portion of the array
        # length = length - 1
        for index in range(length):
            iterations = iterations + 1
            if array[index] > array[index+1]:
                sorted = False  # 2 indexs in wrong order
                array[index], array[index+1] = array[index+1], array[index]  # swap

    return array, '%s iterations' % iterations


def insertion_sort(array):
    """
    Inserts items starting from the left.
    The first list is considered a list of one item and is therefore sorted.
    Next we add another item and compare it to the left, if the new item
    is larger to it's left item then we swap.  We continue this until we've reached
    the end.

    22--2--

    Method: Insertion sort
    Best case: O(n)
    Average case: O(n^2)
    Worst case: O(n^2)
    """
    iterations = 0
    for i in range(len(array)):
        j = i
        while j > 0 and array[j] < array[j-1]:
            iterations = iterations + 1
            array[j-1], array[j] = array[j], array[j-1]
            j = j-1

    return array, '%s iterations' % iterations


def merge(l, r):
    """
    The left array and the right array
    are sorted and then merged together.

    The main purpose of the merge function
    is to continue putting arrays together.

    This function continues to merge arrays
    while it continues to recieve 2-arrays that
    it itself created.
    """
    result = []
    i = j = 0

    # print
    # print 'left merge', l
    # print 'right merge', r

    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            result.append(l[i])
            i += 1
        else:
            result.append(r[j])
            j += 1

    result += l[i:]  # add whatever is left from list 1
    result += r[j:]  # add whatever is left from list 2

    # print 'result', result

    return result


def merge_sort(array):
    """
    Split array up until you have multiple
    arrays, each of size 1.  Then merge the arrays
    in order until you have on array again.


    The main purpose of this function is to break up
    the arrays into 1-item arrays.

    Method: Merge sort
    Best case: O(n log n)
    Average case: O(n log n)
    Worst case: O(n log n)
    """
    # print 'array', array

    if len(array) < 2:
        return array

    m = len(array) / 2

    # print 
    # print 'left', array[:m]
    # print 'right', array[m:]

    return merge(merge_sort(array[:m]), merge_sort(array[m:]))


def quick_sort(array, first, last):
    """
    Type: Exchange (swap) sort
    Best case: O(n log n)
    Average case: O(n log n)
    Worst case: O(n^2)
    """
    if first < last:
        split_index = partition(array, first, last)
        quick_sort(array, first, split_index-1)
        quick_sort(array, split_index+1, last)

    return array

def partition(array, first, last):
    """
    """
    pivot_value = array[first]
    left_index = first+1
    right_index = last

    done = False
    while not done:
        while left_index <= right_index and array[left_index] <= pivot_value:
            left_index = left_index + 1  # scootch to the right

        while right_index >= left_index and array[right_index] >= pivot_value:
            right_index = right_index -1  # scoot to the left

        if right_index < left_index:
            done = True
        else:
            array[left_index], array[right_index] = array[right_index], array[left_index]

    array[first], array[right_index] = array[right_index], array[first]

    return right_index


def selection_sort(array):
    """
    Traverse the entire array looking for the smallest value
    Swap the first unsorted item with the smallest value.
    Continue traversing the entire unsorted array and swaping
    the next smal value with the first unsorted value until you're
    at the second to last item.  It is assumed that the last item is sorted.

    Type: Selection sort
    Best case: O(n^2)
    Average case: O(n^2)
    Worst case: O(n^2)
    """

    # for i in range(len(array)):
    #     mini = min(array[i:])  # find smallest item
    #     min_index = array[i:].index(mini)  # get index of smallest item
    #     array[i+min_index] = array[i]
    #     array[i], array[i+min_index] = mini, array[i]


    for i, value in enumerate(array):
        mini = min(array[i:])
        min_index = array[i:].index(mini)
        array[i+min_index] = value
        array[i], array[i+min_index] = mini, value

    return array


def HeapSort(A, T):
    """
    Type: Selection sort
    Best case: O(n log n)
    Average case: O(n log n)
    Worst case: O(n log n)
    """
    def heapify(A):
        start = (len(A) - 2) / 2
        while start >= 0:
            sift_down(A, start, len(A) - 1)
            start -= 1

    def sift_down(A, start, end):
        root = start
        while root * 2 + 1 <= end:
            child = root * 2 + 1
            if child + 1 <= end and T.count(A[child]) < T.count(A[child + 1]):
                child += 1
            if child <= end and T.count(A[root]) < T.count(A[child]):
                A[root], A[child] = A[child], A[root]
                root = child
            else:
                return  # get out of loop & and function

    heapify(A)
    print 'heapify', A
    end = len(A) - 1
    while end > 0:
        A[end], A[0] = A[0], A[end]
        sift_down(A, 0, end - 1)
        end -= 1


def is_heap(array):
    """
    Checks if array is in heap order.
    The heap property is that each node should be greater
    than or equal to its parent. The parent of element i
    in a binary heap stored in an array is element (i-1)/2
    source: http://stackoverflow.com/questions/16414671/determining-if-a-list-of-numbers-is-in-heap-order-python-3-2
    """
    needs = []
    # example array: [0, 1, 10, 2, 3, 11, 12, 4, 5, 19, 15]
    # code skips the zero index; that's the root index, it has no parent
    for i in range(1, len(array)):
        # print '%s(%s) %s(%s)' % (array[i], i, array[(i-1)/2], (i-1)/2)
        needs.append(array[i] >=array[(i-1)//2])

    return all(needs)




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

    # print 'unsorted', unsorted
    # print 'bubble_sort', bubble_sort(list(unsorted))
    # print 'insertion_sort', insertion_sort(list(unsorted))
    # print 'merge_sort', merge_sort(list(unsorted))
    # print 'quick_sort', quick_sort(list(unsorted), 0, len(list(unsorted))-1)
    # print 'selection_sort', selection_sort(list(unsorted))

    text = 'the quick brown fox jumped over the quick brown quick log log'
    heap = list(set(text.split()))
    print 'unsorted', heap
    HeapSort(heap, text)
    print heap

