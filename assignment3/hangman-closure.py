def make_hangman(secret_word):
    """
    Creates a closure for a game of hangman.
    stores the guesses in a list local to this function scope.
    """
    guesses = []

    def hangman_closure(letter):
        
        guesses.append(letter)

        # Build word
        output_string = ""
        all_guessed = True

        for char in secret_word:
            if char in guesses:
                output_string += char
            else:
                output_string += "_"
                all_guessed = False
        
        print(output_string)
        return all_guessed

    return hangman_closure


if __name__ == "__main__":
    # 1. Prompt for secret word
    secret_word = input("Enter the secret word to start the game: ")
    
    
    play_turn = make_hangman(secret_word)

    print("\n--- Game Start! ---")
    
    
    finished = False
    while not finished:
        guess = input("Guess a letter: ")
        
        # i assuned user enters single character
        if not guess:
            continue
            
        
        finished = play_turn(guess)

    print(f"Congratulations! You guessed the word: {secret_word}")