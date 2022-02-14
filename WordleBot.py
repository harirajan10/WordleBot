import random
import time 

with open('words.txt') as f:
    FIVE_LETTER_WORDS = f.read().splitlines()

PRINT_CHAR_DELAY = 0.03

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
        
def validate_starter_word(starter_word):
    if starter_word not in FIVE_LETTER_WORDS:
        print_chars("Hmm, " + starter_word + " is not a five letter word in the dictionary. Try choosing another word: \n")
        new_starter_word = input()
        validate_starter_word(new_starter_word)
    else:
        print_chars("Okay, " + starter_word + " it is!\n")

# Main 

def main():
    candidate_starter_words = get_candidate_starter_words(10)
    print_chars("Welcome to Hari's Wordle Bot!\n")
    print_chars("Let's get started by giving you a few options for a starter word. Here are some good options: \n")
    for word in candidate_starter_words:
        if (word == candidate_starter_words[-1]):
            print_chars(word + "\n")
        else:
            print_chars(word + ", ")
    print_chars("Go ahead and choose one of the recommended starter words, or choose your own word to start with!.\n")
    print_chars("What word did you choose to start with?\n")
    starter_word = input()
    validate_starter_word(starter_word)

if __name__ == "__main__":
    main()

