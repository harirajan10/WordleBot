from WordleBot import *
from WordlePlay import *
from WordleUtils import *

# Main Logic Helper Fucntions

def validate_game_choice_input(input):
    if input not in ['1', '2']:
        print_chars("Hmm, let's try again. Would you like to (1) play Wordle, (2) play Wordle with Hari's Wordle Bot, or (3) just use Hari's Wordle Bot?")  
        return validate_game_choice_input(input())
    return input

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
    print_chars("Would you like to (1) play Wordle or (2) just use Hari's Wordle Bot?\n")
    game_choice = validate_game_choice_input(input())
    if game_choice == '1':
        play_game(False)
    elif game_choice == '2':
        start_bot()
    else:
        raise Exception("Invalid game choice. Exiting progam.")

if __name__ == "__main__":
    main()