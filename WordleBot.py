import copy
import random
import time 
from WordleUtils import *

with open('candidate_starter_words.txt') as f:
    CANDIDATE_STARTER_WORDS = f.read().splitlines()

# Bot Util Functions

def bot_speak(text):
    print_chars(BOT_SPEAKING + "Go ahead and choose one of the recommended starter words, or choose your own word to start with!\n")


# Bot Logic Helper Fucntions

def get_character_count_map(words):
    char_count_map = {}
    for word in words:
        for char in word:
            if char in char_count_map:
                char_count_map[char] += 1
            else:
                char_count_map[char] = 1

    return char_count_map

def get_most_common_chars():
    char_count_map = get_character_count_map(CANDIDATE_GUESS_WORDS)
    char_count_map = sorted(char_count_map.items(), key=lambda x: x[1], reverse=True)
    return [char for (char, count) in char_count_map]

def get_candidate_starter_words(num_words):
    random_candidate_start_words = random.sample(CANDIDATE_STARTER_WORDS[1:], num_words)
    return [CANDIDATE_STARTER_WORDS[0]] + random_candidate_start_words
        
def validate_word(word):
    if word not in CANDIDATE_GUESS_WORDS:
        print_chars("Hmm, " + word + " is not a five letter word in the dictionary. Try choosing another word: \n")
        new_word = input()
        return validate_word(new_word)
    else:
        print_chars("Okay, " + word + " it is!\n")
        return word

def validate_guess_result(guess_result):
    if len(guess_result) != 5:
        print_chars("Hmm, " + guess_result + " is not a five letter string containing only 'B', 'G', and 'Y'. Try entering the result again: \n")
        new_guess_result = input()
        return validate_guess_result(new_guess_result)
    for letter in guess_result:
        if letter not in ['B', 'G', 'Y']:
            print_chars("Hmm, " + guess_result + " is not a five letter string containing only 'B', 'G', and 'Y'. Try entering the result again: \n")
            new_guess_result = input()
            return validate_guess_result(new_guess_result)
    return guess_result

def validate_secret_word(secret_word):
    if secret_word not in CANDIDATE_SECRET_WORDS:
        print_chars("Hmm, " + secret_word + " is not a a valid secret word. Try choosing another word: \n")
        return validate_secret_word(input())
    return secret_word


def word_possible(word, possibilities_map, known_letters_map):
    for letter in known_letters_map:
        if word.count(letter) < len(known_letters_map[letter]):
            return False
    for i in range(0,len(word)):
        if word[i] not in possibilities_map[i]:
            return False
    return True

def filter_bad_guess_candidates(candidate_words, possibilities_map):
    # its a bad gas if we know we are going to get >1 'B'
    filtered_candidate_words = []
    for candidate_word in candidate_words:
        known_blanks = 0
        for i in range(0, len(candidate_word)):
            if candidate_word[i] not in possibilities_map[i]:
                known_blanks += 1
        if known_blanks <= 1:
            filtered_candidate_words.append(candidate_word)
    
    return filtered_candidate_words

def get_next_guess_words(possible_words, possibilities_map, known_letters_map):
    candidate_guess_word_scores = {}
    candidate_guess_words = filter_bad_guess_candidates(CANDIDATE_GUESS_WORDS, possibilities_map)
    for candidate_guess_word in candidate_guess_words:
        guess_word_is_potential_secret_word = word_possible(candidate_guess_word, possibilities_map, known_letters_map) and candidate_guess_word in CANDIDATE_SECRET_WORDS
        skip_guess_word = False
        total_possibilities = 0
        clue_str_dict = {}
        guess_word_scores = sorted(candidate_guess_word_scores.values())
        threshold_guess_word_score = 99999999
        if len(guess_word_scores) > 5:
            threshold_guess_word_score = guess_word_scores[5]
        for candidate_secret_word in possible_words:
            clue_str = get_result_clue_string(candidate_guess_word, candidate_secret_word)
            if clue_str not in clue_str_dict:
                next_possibilities_map = copy.deepcopy(possibilities_map)
                next_known_letter_map = copy.deepcopy(known_letters_map)
                update_tracking_maps(candidate_guess_word, clue_str, next_possibilities_map, next_known_letter_map)
                clue_str_dict[clue_str] = len(get_possible_words(possible_words, next_possibilities_map, next_known_letter_map))
            total_possibilities +=  0.9 * clue_str_dict[clue_str] if guess_word_is_potential_secret_word else clue_str_dict[clue_str]
            if total_possibilities > threshold_guess_word_score:
                skip_guess_word = True
                break
        if skip_guess_word:
            continue

        candidate_guess_word_scores[candidate_guess_word] = 1.0 * total_possibilities
    
    return sorted(candidate_guess_word_scores.items(), key=lambda item: item[1])

def populate_first_guess_word_suggestions_fast():
    common_chars = get_most_common_chars()
    # only consider words with only unique letters
    # assign point value based on letter frequency
    # choose num_words random words with low point value
    word_value_map = {}
    for word in CANDIDATE_GUESS_WORDS:
        if not unique_letters(word):
            continue
        word_point_value = 0
        for char in word:
            word_point_value += common_chars.index(char)
        word_value_map[word] = word_point_value
    
    word_value_map = sorted(word_value_map.items(), key=lambda x: x[1], reverse=False)
    candidate_start_words = [word for (word, value) in word_value_map if value <= 25]
    with open("first_guess_words.txt", "w") as first_guess_words_file:
        for word in candidate_start_words:
            first_guess_words_file.write(word + '\n')
    first_guess_words_file.close()

def populate_first_guess_word_suggestions_slow():
    word_value_map = {}
    print("Calculating avg number of possibilities for " + str(len(CANDIDATE_GUESS_WORDS)) + " candidate starter words")
    for candidate_starter_word in CANDIDATE_GUESS_WORDS:
        total_possibilities = 0
        print("Calculating avg number of possibilities for guess_word: " + candidate_starter_word + '\n')
        clue_str_dict = {}
        for potential_secret_word in CANDIDATE_SECRET_WORDS:
            clue_str = get_result_clue_string(candidate_starter_word, potential_secret_word)
            if clue_str not in clue_str_dict:
                possibilities_map = init_possibilities_map()
                known_letter_map = {}
                update_tracking_maps(candidate_starter_word, clue_str, possibilities_map, known_letter_map)
                clue_str_dict[clue_str] = len(get_possible_words(CANDIDATE_SECRET_WORDS, possibilities_map, known_letter_map))
            total_possibilities += clue_str_dict[clue_str]
        
        word_value_map[candidate_starter_word] = (total_possibilities * 1.0) / len(CANDIDATE_SECRET_WORDS)
        print("starter_word: " + candidate_starter_word + ", value: " + str(word_value_map[candidate_starter_word]) + '\n')
    
    word_value_map = sorted(word_value_map.items(), key=lambda x: x[1], reverse=False)
    print(word_value_map[:25])
    with open("candidate_starter_words.txt", "w") as first_guess_words_file:
        for word, _ in word_value_map[:25]:
            first_guess_words_file.write(word + '\n')
    first_guess_words_file.close()

def get_possible_words(possible_words, possibilities_map, known_letters_map):
    return [word for word in possible_words if word_possible(word, possibilities_map, known_letters_map)]

def update_tracking_maps(guess_word, clue_str, possibilities_map, known_letters_map):
    yg_letters = []
    y_letters = []
    for i in range(0, len(clue_str)):
        result = clue_str[i]
        letter = guess_word[i]
        if result == 'B':
            # remove letter from possibilities map unless the letter is known at a certain index
            for k, v in possibilities_map.items():
                if len(v) == 1:
                    continue
                if letter in v:
                    # don't remove if k != i and we've seen this letter in yellow
                    if k == i or letter not in y_letters:
                        v.remove(letter)
            if letter in known_letters_map:
                for possible_indices in known_letters_map[letter]:
                    if i in possible_indices:
                        possible_indices.remove(i)

        elif result == 'Y':
            # add to known letters map
            if letter in yg_letters:
                num_previous_occurrences_in_guess = yg_letters.count(letter)
                num_known_occurrences = len(known_letters_map[letter])
                # if we've already seen this letter, add a new occurrence of the letter 
                # to known_letters_map if necessary
                if num_previous_occurrences_in_guess == num_known_occurrences:
                    known_letters_map[letter].append([0,1,2,3,4])
            else:
                if letter not in known_letters_map:
                    known_letters_map[letter] = [[0,1,2,3,4]]
            for possible_indices in known_letters_map[letter]:
                if i in possible_indices and len(possible_indices) > 1:
                    possible_indices.remove(i)
            # remove letter from possibilities map at index i
            if letter in possibilities_map[i]:
                possibilities_map[i].remove(letter)
            yg_letters.append(letter)
            y_letters.append(letter)
        elif result == 'G':
            # add to known letters map
            if letter in yg_letters:
                num_previous_occurrences_in_guess = yg_letters.count(letter)
                num_known_occurrences = len(known_letters_map[letter])
                # remove index from possible indices unless it's already known
                for possible_indices in known_letters_map[letter]:
                    if i in possible_indices and len(possible_indices) > 1:
                        possible_indices.remove(i)
                # add a new known occurrence if this is indeed a new known occurrence
                # otherwise, set the known index
                if num_previous_occurrences_in_guess == num_known_occurrences:
                    known_letters_map[letter].append([i])
                else:
                    if [i] not in known_letters_map[letter]:
                        known_letters_map[letter][0] = [i]
            else:
                if letter not in known_letters_map:
                    known_letters_map[letter] = [[i]]
                elif [i] not in known_letters_map[letter]:
                    known_letters_map[letter][0] = [i]
            for l, possible_indices_list in known_letters_map.items():
                if l != letter:
                    for possible_indices in possible_indices_list:
                        if i in possible_indices:
                            possible_indices.remove(i)
            # make letter only possibilities for index i
            possibilities_map[i] = [letter]
            yg_letters.append(letter)
    
def suggest_next_guess_word(guess_number, guess_word, clue_str, possibilities_map, known_letters_map, possible_words):
    if guess_number == 1:
        next_guess_words = get_candidate_starter_words(10)
        best_guess_word = next_guess_words[0]
    else:
        print_chars(BOT_SPEAKING + "Give me a second to think of a good guess word...\n")
        update_tracking_maps(guess_word, clue_str, possibilities_map, known_letters_map)

        possible_words = get_possible_words(possible_words, possibilities_map, known_letters_map)
        if len(possible_words) == 1:
            print_chars(BOT_SPEAKING + "Alright, I think today's Wordle is..." + possible_words[0] +"! Go ahead and try that for your next guess!\n")
            return

        next_guess_words = get_next_guess_words(possible_words, possibilities_map, known_letters_map)

        if len(next_guess_words) == 0:
            raise Exception("Oh no, something went wrong! I don't have any words to suggest, you may have entered a guess result incorrectly :(")

        best_guess_word, _ = next_guess_words[0]

    print_chars(BOT_SPEAKING + "I suggest trying " + best_guess_word +"!\n")

    if len(next_guess_words) > 1:
        print_chars(BOT_SPEAKING + "Some other good options would be: ")
        print(next_guess_words[1:5])

# Main 

def test_bot():
    print("Testing Bot....")
    results = []
    guess_memo_table = {}
    # sampled_candidate_secret_words = random.sample(CANDIDATE_SECRET_WORDS, 200)
    for secret_word in CANDIDATE_SECRET_WORDS:
        guess_number = 1
        guess_word = CANDIDATE_STARTER_WORDS[0]
        clue_str = get_result_clue_string(guess_word, secret_word)
        possible_words = CANDIDATE_SECRET_WORDS
        possibilities_map = init_possibilities_map()
        known_letters_map = {}
        guess_words = [guess_word]
        while clue_str != 'GGGGG':
            update_tracking_maps(guess_word, clue_str, possibilities_map, known_letters_map)
            possible_words = get_possible_words(possible_words, possibilities_map, known_letters_map)
            guess_words_string = "".join(guess_words)
            guess_key = (guess_words_string, clue_str)
            if guess_key in guess_memo_table:
                guess_word = guess_memo_table[guess_key]
            else:
                next_guess_words = get_next_guess_words(possible_words, possibilities_map, known_letters_map)
                guess_word, _ = next_guess_words[0]
                guess_memo_table[(guess_key, clue_str)] = guess_word
            clue_str = get_result_clue_string(guess_word, secret_word)
            guess_words.append(guess_word)
            guess_number += 1
        results.append(guess_number)
        running_average = sum(results) / float(len(results))
        print("secret_word: " + secret_word + " num_guesses: " + str(guess_number) + " running_average: " + str(running_average))
    result_frequency_map = {}
    for r in results:
        if r not in result_frequency_map:
            result_frequency_map[r] = 0
        result_frequency_map[r] += 1

    print("Guess Number Frequencies: ")
    print(result_frequency_map)
    print("Average number of guesses: ")
    print(running_average)
    print("Win rate: ")
    failures = [x for x in results if x > 6]
    print(1 - (len(failures) / float(len(results))))


def main_loop(guess_word, guess_number, possibilities_map, known_letters_map, possible_words):
    print_chars("How did your " + ORDINAL_NUMBERS_STRING_MAP[guess_number] + " guess go? (Type 'B' for blank, 'G' for green, and 'Y' for yellow)\n")
    guess_result = validate_guess_result(input())
    if guess_result == 'GGGGG':
        print_chars("Woooohooooo! We beat today's wordle in " + str(guess_number) + " guesses! Come back tomorrow and let's keep our streak alive :) \n")
        return
    if guess_number == 6:
        print_chars("Oh no, seems like we've lost! Sorry I couldn't help you, let's try again tomorrow :( \n")
        return

    suggest_next_guess_word(guess_number + 1, guess_word, guess_result, possibilities_map, known_letters_map, possible_words)
    possible_words = get_possible_words(possible_words, possibilities_map, known_letters_map)
    print_chars("What word are you choosing to go with for your next guess?\n")
    next_guess_word = validate_word(input())
    main_loop(next_guess_word, guess_number + 1, possibilities_map, known_letters_map, possible_words)

def play_against_bot():
    print_chars("Go ahead and choose a secret word for Hari's Wordle Bot to guess:\n")
    secret_word = validate_secret_word(input())
    possible_words = CANDIDATE_SECRET_WORDS
    possibilities_map = init_possibilities_map()
    known_letters_map = {}
    guess_number = 1
    guess_result = ''
    while guess_result != 'GGGGG':
        if guess_number == 1:
            guess_word = CANDIDATE_STARTER_WORDS[0]
        elif guess_number > 6:
            print_chars(BOT_SPEAKING + "Oh no! I couldn't guess your secret word :(\n")    
            return
        else:
            update_tracking_maps(guess_word, guess_result, possibilities_map, known_letters_map)
            possible_words = get_possible_words(possible_words, possibilities_map, known_letters_map)
            next_guess_words = get_next_guess_words(possible_words, possibilities_map, known_letters_map)
            guess_word, _ = next_guess_words[0]
        print_chars(BOT_SPEAKING + "Alright, my " + ORDINAL_NUMBERS_STRING_MAP[guess_number] + " guess is " + guess_word + "!\n")
        print_chars(BOT_SPEAKING + "How did I do? (Type 'B' for blank, 'G' for green, and 'Y' for yellow)\n")
        guess_result = validate_guess_result(input())
        if guess_result == 'GGGGG':
            break    
        guess_number += 1    
    print_chars("Wooohooo! Hari's Wordle Bot guessed your secret word, " + secret_word + ", in " + str(guess_number) + " guesses!\n")

def start_bot():
    candidate_starter_words = get_candidate_starter_words(10)
    print_chars(BOT_SPEAKING + "Hello!\n")
    print_chars(BOT_SPEAKING+ "Let's get started by giving you a few options for a starter word. Here are some good options: \n")
    for word in candidate_starter_words:
        if (word == candidate_starter_words[-1]):
            print_chars(word + "\n")
        else:
            print_chars(word + ", ")
    print_chars(BOT_SPEAKING + "Go ahead and choose one of the recommended starter words, or choose your own word to start with!\n")
    print_chars(BOT_SPEAKING + "What word did you choose to start with?\n")
    starter_word = input()
    starter_word = validate_word(starter_word)
    main_loop(starter_word, 1, init_possibilities_map(), {}, CANDIDATE_SECRET_WORDS)

if __name__ == "__main__":
    test_bot()
