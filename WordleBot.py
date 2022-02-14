import random
import time 

with open('words.txt') as f:
    FIVE_LETTER_WORDS = f.read().splitlines()

PRINT_CHAR_DELAY = 0.02
ORDINAL_NUMBERS_STRING_MAP = {1 : "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "last" }

# General Utils

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

# Bot Logic Helper Fucntions

def get_character_count_map(words):
    char_count_map = {}
    for word in words:
        for char in word:
            if char in char_count_map:
                char_count_map[char] += 1
            else:
                char_count_map[char] = 1

    # sort the dictionary in descending order by character count
    char_count_map = sorted(char_count_map.items(), key=lambda x: x[1], reverse=True)
    return char_count_map

def get_most_common_chars():
    char_count_map = get_character_count_map(FIVE_LETTER_WORDS)
    return [char for (char, count) in char_count_map]

def get_candidate_starter_words(num_words):
    common_chars = get_most_common_chars()
    # only consider words with only unique letters
    # assign point value based on letter frequency
    # choose num_words random words with low point value
    word_value_map = {}
    for word in FIVE_LETTER_WORDS:
        if not unique_letters(word):
            continue
        word_point_value = 0
        for char in word:
            word_point_value += common_chars.index(char)
        word_value_map[word] = word_point_value
    
    word_value_map = sorted(word_value_map.items(), key=lambda x: x[1], reverse=False)
    candidate_start_words = [word for (word, value) in word_value_map if value <= 25]
    random_candidate_start_words = random.sample(candidate_start_words, num_words)

    return random_candidate_start_words
        
def validate_word(word):
    if word not in FIVE_LETTER_WORDS:
        print_chars("Hmm, " + word + " is not a five letter word in the dictionary. Try choosing another word: \n")
        new_word = input()
        return validate_word(new_word)
    else:
        print_chars("Okay, " + word + " it is!\n")
        return word

def word_possible(word, letter_possibilities_map, letters_in_word):
    for letter, letter_possiblities in letter_possibilities_map.items():
        if len(letter_possiblities) == 1 and word[letter_possiblities[0]] != letter:
            return False
    for letter in letters_in_word:
        if letter not in word:
            return False
    for i in range(0, len(word)):
        if word[i] not in letter_possibilities_map:
            return False
        if i not in letter_possibilities_map[word[i]]:
            return False
    return True

def get_next_guess_words(letter_possibilities_map, letters_in_word, possible_words):
    # get letters in the word that are not already known
    # assume they turn out to be Bs
    # see how many possibe words would be left
    # return the word(s) with the lowest number of possible words
    possible_words_map = {}
    possible_words_map_db = {}
    for word in FIVE_LETTER_WORDS:
        # TODO: fix this logic to address the letters not in new_letters
        new_letters = [char for char in word if char not in letters_in_word]
        next_letter_possibilities_map = letter_possibilities_map.copy()
        for letter in new_letters:
            next_letter_possibilities_map.pop(letter, None)
        next_possible_words = [w for w in possible_words if word_possible(w, next_letter_possibilities_map, letters_in_word)]
        possible_words_map[word] = len(next_possible_words)
        possible_words_map_db[word] = next_possible_words

    # Prefer to suggest a word its also a possible word
    minval = min(possible_words_map.values())
    candidate_guesses = [k for k, v in possible_words_map.items() if v == minval and word_possible(k, letter_possibilities_map, letters_in_word)]

    # debug
    if minval == 0:
        db_arr = [(w, possible_words_map_db[w]) for w, v in possible_words_map.items() if v == minval]
        # print(db_arr)
    if len(candidate_guesses) > 0:
        ret = []
        for i in range(0, min(len(candidate_guesses), 3)):
            ret.append((candidate_guesses[i], minval))
        return ret
    possible_words_map = [(k,v) for (k,v) in possible_words_map.items() if v != 0 or word_possible(k, letter_possibilities_map, letters_in_word)]
    possible_words_map = sorted(possible_words_map, key=lambda x: x[1], reverse=False)
    return possible_words_map[:4]


def main_loop(guess_word, guess_number, letter_possibilities_map, letters_in_word, possible_words):
    print_chars("How did your " + ORDINAL_NUMBERS_STRING_MAP[guess_number] + " guess go? (Type 'B' for blank, 'G' for green, and 'Y' for yellow)\n")
    # TODO: add error handling
    # TODO: need to handle the case of two Ys for the same letter
    # TODO: need to handle the case of two Gs for the same letter
    guess_result = input()
    if guess_result == 'GGGGG':
        print_chars("Woooohooooo! We beat today's wordle in " + str(guess_number) + " guesses! Come back tomorrow and let's keep our streak alive :) \n")
        return
    if guess_number == 6:
        print_chars("Oh no, seems like we've lost! Sorry I couldn't help you, let's try again tomorrow :( \n")
        return

    b_indices = find_char_indices(guess_result, 'B')
    g_indices = find_char_indices(guess_result, 'G')
    y_indices = find_char_indices(guess_result, 'Y')
    for i in g_indices:
        letters_in_word.add(guess_word[i])
        for letter, possible_indices in letter_possibilities_map.items():
            if letter == guess_word[i]:
                letter_possibilities_map[letter] = [i]
            elif i in letter_possibilities_map[letter]:
                letter_possibilities_map[letter].remove(i)
    for i in y_indices:
        letters_in_word.add(guess_word[i])
        if i in letter_possibilities_map[guess_word[i]]:
            letter_possibilities_map[guess_word[i]].remove(i)
    for i in b_indices:
        if guess_word[i] in letters_in_word:
            continue
        else: 
            letter_possibilities_map.pop(guess_word[i], None)

    possible_words = [word for word in possible_words if word_possible(word, letter_possibilities_map, letters_in_word)]
    if len(possible_words) == 1:
        print_chars("Alright, I think today's Wordle is..." + possible_words[0] +"!\n")
        print_chars("We solved the Wordle in " + str(guess_number + 1) + " guesses! Come back tomorrow and let's keep our streak alive :) \n")
        return

    next_guess_words = get_next_guess_words(letter_possibilities_map, letters_in_word, possible_words)

    if len(next_guess_words) == 0:
        raise Exception("Oh no, something went wrong! I don't have any words to suggest :(")

    best_guess_word, _ = next_guess_words[0]
    print_chars("Alright! For our next guess, let's go with " + best_guess_word +"!\n")

    if len(next_guess_words) > 1:
        print_chars("Some other good options would be: ")
        print(next_guess_words[1:])
    print_chars("What word did you choose to go with?\n")
    next_guess_word = input()
    next_guess_word = validate_word(next_guess_word)

    main_loop(next_guess_word, guess_number + 1, letter_possibilities_map, letters_in_word, possible_words)

# Main 

def main():
    print('\033[92m')
    print(" _    _            _        __          __           _ _            ____        _   ")
    print("| |  | |          (_)       \ \        / /          | | |          |  _ \      | |  ")
    print("| |__| | __ _ _ __ _  __     \ \  /\  / /__  _ __ __| | | ___      | |_) | ___ | |_ ")
    print("|  __  |/ _` | '__| / __\     \ \/  \/ / _ \| '__/ _` | |/ _ \     |  _ < / _ \| __|")
    print("| |  | | (_| | |  | \__ \      \  /\  / (_) | | | (_| | |  __/     | |_) | (_) | |_ ")
    print("|_|  |_|\__,_|_|  |_|___/       \/  \/ \___/|_|  \__,_|_|\___|     |____/ \___/ \__|")
    print('\n')
    candidate_starter_words = get_candidate_starter_words(10)
    print_chars("Welcome to Hari's Wordle Bot!\n")
    print_chars("Let's get started by giving you a few options for a starter word. Here are some good options: \n")
    for word in candidate_starter_words:
        if (word == candidate_starter_words[-1]):
            print_chars(word + "\n")
        else:
            print_chars(word + ", ")
    print_chars("Go ahead and choose one of the recommended starter words, or choose your own word to start with!\n")
    print_chars("What word did you choose to start with?\n")
    starter_word = input()
    starter_word = validate_word(starter_word)
    letter_possibilities_map = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        letter_possibilities_map[letter] = [0, 1, 2, 3, 4, 5, 6]
    main_loop(starter_word, 1, letter_possibilities_map, set([]), FIVE_LETTER_WORDS)

if __name__ == "__main__":
    main()

