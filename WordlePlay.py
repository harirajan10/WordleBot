import random
from WordleUtils import *
from WordleBot import *


# Play Logic Helper Fucntions

def validate_bot_choice_input(input):
    if input not in ['Y', 'N']:
        print_chars("Hmm, let's try again. Please type 'Y' to use Hari's Wordle Bot while playing, or 'N' if you would like to play without using Hari's Wordle Bot: \n")  
        return validate_bot_choice_input(input())
    return input

def validate_guess_word_input(guess_word):
    if guess_word not in CANDIDATE_GUESS_WORDS:
        print_chars("Hmm, that guess seems to be invalid, try another guess. Make sure your guess is a valid five letter word in the English dictionary.\n")  
        return validate_guess_word_input(input())
    return guess_word

def get_secret_word():
    return random.sample(CANDIDATE_SECRET_WORDS, 1)[0]

# Main 

def main_loop(secret_word, guess_number, prev_guess_word="", prev_clue_str="", possibilities_map={}, known_letters_map={}, possible_words=[], use_bot=False):
    print_chars("What's your " + ORDINAL_NUMBERS_STRING_MAP[guess_number] + " guess?\n")
    if use_bot:
        suggest_next_guess_word(guess_number, prev_guess_word, prev_clue_str, possibilities_map, known_letters_map, possible_words)
    
    guess_word = validate_guess_word_input(input())
    clue_str = get_result_clue_string(guess_word, secret_word)
    print_chars(clue_str + '\n')
    if clue_str == 'GGGGG':
        print_chars("Woooohooo! Congrats, you beat the wordle for " + secret_word + " in " + str(guess_number) + " guesses!\n")
    elif guess_number == 6:
        print_chars("Oh no, you're out of guesses! The secret word was " + secret_word + "\n")
    else: 
        if use_bot:
            update_tracking_maps(guess_word, clue_str, possibilities_map, known_letters_map)
            main_loop(secret_word, guess_number + 1, guess_word, clue_str, possibilities_map, known_letters_map, get_possible_words(possible_words, possibilities_map, known_letters_map), use_bot)
        else:
            main_loop(secret_word, guess_number + 1)

def play_game(debug):
    print_chars("Let's play Wordle!\n")
    print_chars("Would you like to play with Hari's Wordle Bot? (Y/N)\n")
    bot_choice = validate_bot_choice_input(input())

    if bot_choice == 'Y' or bot_choice == 'N':
        secret_word = get_secret_word()
        if debug:
            print_chars("Secret word is " + secret_word +"\n")
        print_chars("Alright! I've thought of my secret word!\n")
        if bot_choice == 'Y':
            main_loop(secret_word, 1, "", "", init_possibilities_map(), {}, CANDIDATE_SECRET_WORDS, True)
        else:
            main_loop(secret_word, 1)
    else:
        raise Exception("Invalid bot choice. Exiting progam.")


if __name__ == "__main__":
    play_game(True)