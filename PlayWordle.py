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