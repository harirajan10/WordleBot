import time 

ORDINAL_NUMBERS_STRING_MAP = {1 : "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "last" }
PRINT_CHAR_DELAY = 0.02
BOT_SPEAKING = ">> Hari's Wordle Bot: "

with open('candidate_guess_words.txt') as f:
    CANDIDATE_GUESS_WORDS = f.read().splitlines()
    CANDIDATE_GUESS_WORDS = [w.lower() for w in CANDIDATE_GUESS_WORDS]

with open('candidate_secret_words.txt') as f:
    CANDIDATE_SECRET_WORDS = f.read().splitlines()
    CANDIDATE_SECRET_WORDS = [w.lower() for w in CANDIDATE_SECRET_WORDS]

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

def get_result_clue_string(guess_word, secret_word):
    guess_word_arr = list(guess_word)
    secret_word_arr = list(secret_word)
    clue_arr = ['B', 'B', 'B', 'B', 'B']
    for i in range(0, len(secret_word_arr)):
        if guess_word_arr[i] == secret_word_arr[i]:
            guess_word_arr[i] = '-'
            secret_word_arr[i] = '-'
            clue_arr[i] = 'G'
    for i in range(0, len(secret_word_arr)):
        if guess_word_arr[i] != '-' and guess_word_arr[i] in secret_word_arr:
            secret_word_arr[secret_word_arr.index(guess_word_arr[i])] = '-'
            clue_arr[i] = 'Y'

    return ''.join(clue_arr)

def all_chars_unique(s):
    return len(set(s)) == len(s)

def init_possibilities_map():
    possibilities_map = {}
    for i in [0,1,2,3,4]:
        possibilities_map[i] = list("abcdefghijklmnopqrstuvwxyz")
    return possibilities_map
