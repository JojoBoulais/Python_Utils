from profiling import matplotthis

@matplotthis(100, amp_factor=10)
def some_lin_func(list1, list2):
    for el in list1:
        print(el)

    for el in list2:
        print(el)

@matplotthis(100, amp_factor=10)
def some_n2_func(list1, list2):
    for el in list1:
        print(el)

        for el in list2:
            print(el)

#some_lin_func([10]*10, [20]*10)
some_n2_func([10]*10, [20]*10)
