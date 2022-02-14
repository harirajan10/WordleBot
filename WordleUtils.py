def print_chars(string):
    for char in string:
        print(char, end="", flush=True)
        time.sleep(PRINT_CHAR_DELAY)

def unique_letters(word):
    chars = []
    for char in word:
        if char in chars:
            return False
        chars.append(char)
    return True

def find_char_indices(string, char):
    return [i for i, ltr in enumerate(string) if ltr == char]