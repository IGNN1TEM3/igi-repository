# Task 5
def input_elements():
    """Function for initializing input elements"""
    print("Enter float elements (e to end): ")
    arr = list()
    x = input()
    while x != "e":
        arr.append(x)
        x = input()
    return arr


def check_input_validation(arr):
    """Checks input validation and returns list or None"""
    if len(arr) == 0:
        return None
    float_list = []
    try:
        for item in arr:
            float_list.append(float(item))
        return float_list
    except ValueError:
        return None


def max_modulo_num_index(lst):
    """Returns the index of the maximum modulo number"""
    value = max(lst)
    index = lst.index(value)
    return index


def second_subtask(lst):
    """Returns the product of the elements located between the first and second zero elements or None"""
    try:
        start = lst.index(0) + 1
        end = lst.index(0, start)

        if start == end:
            return None

        product = 1
        for i in lst[start:end]:
            product *= i
        return product
    except ValueError:
        return None


def print_list(lst):
    """Prints out current list elements."""
    print("Current list: ", "[", sep="\n", end=" ")
    for item in lst:
        print(item, end=", ")
    print("]")


def task5_solve():
    """Task 5 output function"""
    print("---Task 5---")

    lst = check_input_validation(input_elements())
    if lst is None:
        print("Invalid input! ONly float numbers are accepted and list can't be empty.")
        return
    print_list(lst)

    mod_num = max_modulo_num_index(lst)
    print("Max modulo number index: ", mod_num)
    product_res = second_subtask(lst)
    if product_res is not None:
        print(
            "Product of the elements located between the first and second zero element: ",
            product_res,
        )
    else:
        print("The problem about zero elements cannot be solved")
