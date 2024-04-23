# Task 1
import math
import pandas as pd


def my_ln(x, esp=1e-6, max_iterations=500):
    """
    Calculate ln(1-x) function

    Positional Arguments:
    x {float} -- x value (-1<=x<=1)
    Keyword Arguments:
    esp {float} -- calculation accuracy (default: {1e-6})
    max_iterations {int} -- maximum number of iterations (default: {500})


    Returns:
    result {float} -- ln(1-x) value
    iteration {int} -- number of iterations
    """

    result = -x
    term = -x
    iteration = 1
    while abs(term) > esp and iteration <= max_iterations:
        term = term * x * iteration / (iteration + 1)
        result += term
        iteration += 1

    return result, iteration


def check_validation(st):
    try:
        x, eps = st.split(" ")
        x = float(x)
        eps = float(eps)
        if eps <= 0 or abs(x) > 1:
            return None, None
        else:
            return x, eps
    except ValueError:
        return None, None


def task1_solve():
    """Task 1 output function."""
    print("---Task 1---")
    x, eps = check_validation(input("Input x(-1<x<1) and eps(>0) separated by space: "))
    if x is None:
        print("- |x| must be under 1")
        print("- and eps must be positive")
        return

    f, n = my_ln(x, eps)
    data = {
        "x": [x],
        "n": [n],
        "F(x)": [f],
        "Math F(x)": [math.log(1 - x)],
        "eps": [eps],
    }
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
