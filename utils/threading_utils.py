import math
import multiprocessing
import threading
import copy
import os

CPU_COUNT = multiprocessing.cpu_count()


def distribute_element(some_list, chunks=CPU_COUNT, keep_order=True):
    """
    Splits element of given list into specified number of chunks. (arrays)

    :param list some_list:
    :param int chunks:
    :param bool keep_order:
    :rtype: list[list]
    """
    if chunks <= 0:
        return [some_list]

    if len(some_list) < chunks:
        return [[i] for i in some_list]

    chunk_size = math.ceil(float(len(some_list)) / float(chunks))

    arrays = [[] for _ in list(range(0, chunks))]

    # Fills in one chunk at the time.
    if keep_order:
        idx = 0
        count = 0
        for element in some_list:
            arrays[idx].append(element)
            if count == chunk_size:
                idx += 1
                count = 0
            count+=1
        return arrays

    # Changes array each iteration.
    array_idx = 0
    for i, item in enumerate(some_list, start=1):
        arrays[array_idx].append(item)
        if i % chunks == 0:
            array_idx = 0
        else:
            array_idx += 1

    return arrays


def threads_from_func_on_list(some_list, func, *args, **kwargs):

    threads = []

    arrays = distribute_element(some_list)

    for array in arrays:
        t = threading.Thread(target=func, args=([array]))
        threads.append(t)

    return threads


def my_test_func(some_list, kaka="sasa"):
    for el in some_list:
        print(el, f": toto {kaka}")



t = " ".join(map(lambda x: str(x), range(0, 10)))

t += "saas"
print(t)
