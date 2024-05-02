
def bubble_sort(array):
    """
    https://www.geeksforgeeks.org/python-program-for-bubble-sort/

    O(n*n)

    :param list[int] array:
    :rtype: list[int]
    """

    n = len(array)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
            if array[j] > array[j + 1]:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]

        if not swapped:
            return

    return array


def selection_sort(array):
    """
    https://www.geeksforgeeks.org/python-program-for-selection-sort/

    O(n*n)

    :param list[int] array:
    """
    size = len(array)
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            # select the minimum element in every iteration
            if array[j] < array[min_index]:
                min_index = j
        # swapping the elements to sort the array
        (array[ind], array[min_index]) = (array[min_index], array[ind])


def merge_sort(array):
    """
    https://www.programiz.com/dsa/merge-sort

    O(n log n)

    :param list[int] array:
    :return:
    """

    if len(array) > 1:

        #  r is the point where the array is divided into two subarrays
        r = len(array)//2
        L = array[:r]
        M = array[r:]

        # Sort the two halves
        merge_sort(L)
        merge_sort(M)

        i = j = k = 0

        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        while i < len(L) and j < len(M):
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1

        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1



# function to find the partition position
def __partition(array, low, high):
    """Used by quick_sort func."""

    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
            # if element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

        # swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])

        # return the position from where partition is done
        return i + 1

# function to perform quicksort
def quick_sort(array, low=None, high=None):
    """
    https://www.programiz.com/dsa/quick-sort

    O(n*log n)

    :param list[int] array:
    :param int low:
    :param int high:
    """

    if not low:
        low = 0

    if not high:
        high = len(array)-1

    if not low < high:
        return

    # find pivot element such that
    # element smaller than pivot are on the left
    # element greater than pivot are on the right
    pi = __partition(array, low, high)

    # recursive call on the left of pivot
    quick_sort(array, low, pi - 1)

    # recursive call on the right of pivot
    quick_sort(array, pi + 1, high)
