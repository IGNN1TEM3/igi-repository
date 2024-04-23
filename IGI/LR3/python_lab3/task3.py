# Task 3
def input_text():
    """Input text and return it as a string"""
    return input("Enter your text: ")


def analize_text(text):
    """Counts the number of space characters in a given string"""
    return text.count(" ")


def task3_solve():
    """Task 3 output function"""
    print("---Task 3---")
    text = input_text()
    print(f"Number of space characters in given text is {analize_text(text)}")
