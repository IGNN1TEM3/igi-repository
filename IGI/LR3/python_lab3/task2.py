# Task 2
def input_loop():
    """Input function for initialize sequence"""
    arr = list()
    print("Start input int sequence... (>1000 to end)")
    x = check_validation(input())

    if x is None:
        print("Invalid input!")
        return None

    while x <= 1000:
        arr.append(x)
        x = check_validation(input())
        if x is None:
            print("Invalid input!")
            return None
    return arr


def count_even(arr):
    """Count even numbers"""
    return sum(1 for num in arr if num % 2 == 0)


def check_validation(st):
    try:
        st = int(st)
        return st
    except ValueError:
        return None


def task2_solve():
    """Task 2 output function."""
    print("---Task 2---")
    arr = input_loop()
    if arr is None:
        return
    n = count_even(arr)
    print(f"Number of even numbers in the sequence is {n}")
