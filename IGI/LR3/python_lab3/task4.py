# Task 4
def word_count_by_length(text, length=5):
    """Counts the number of words in a text with length less than a 5 and returns result"""
    raw_text = text.replace(".", "").replace(",", "")
    return sum(1 for word in raw_text.split(" ") if len(word) < 5)


def shortest_word_by_last_char(text, char="d"):
    """
    Returns the shortest word in the text ends with char

    Positional Arguments:
    text - text to analyze
    Keyword Arguments:
    char - character with which the word must end  (default: {"d"})

    Returns:
    the shortest word in the text ends with char or None

    """
    raw_text = text.replace(".", "").replace(",", "")
    target_words = [word for word in raw_text.split(" ") if word.endswith(char)]
    if target_words:
        return min(target_words, key=len)
    else:
        return None


def print_sorted_by_length(text):
    """Prints words sorted by their length in the text."""
    raw_text = text.replace(".", "").replace(",", "")
    words = raw_text.split(" ")

    print("Sorted by length words:")
    for word in sorted(words, key=lambda word: len(word), reverse=True):
        print(word, end=" ")
    print("")


def task4_solve():
    """Task 4 output function"""
    text = (
        "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy "
        "and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and "
        "picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    )
    print("---Task 4---")
    print("Entire text:", text, sep="\n")

    first_res = word_count_by_length(text)
    print(f"Number of words with length less than 5 is {first_res}.")

    second_res = shortest_word_by_last_char(text)
    if second_res is not None:
        print(f'The shortest word ends with "d" is {second_res}.')
    else:
        print(f'No words ends with "d".')

    print_sorted_by_length(text)
