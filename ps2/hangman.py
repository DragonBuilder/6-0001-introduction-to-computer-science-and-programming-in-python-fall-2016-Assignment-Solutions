# Problem Set 2, hangman.py
# Name: DragonBuilder
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    
    for letter in secret_word:
        if (letter not in letters_guessed):
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess_string = ''
    for letter in secret_word:
        if letter in letters_guessed:
            guess_string += letter
        else:
            guess_string += '_ '
            
    return guess_string



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters_not_guessed = ''
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            letters_not_guessed += i
    return letters_not_guessed
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print("Welcome to the game Hangman!")
    sec_wrd_len = len(secret_word)
    print("I am thinking of a word that is " + str(sec_wrd_len) + " letters long.")
    
    warnings = 3;
    
    num_guesses = 6;
    letters_guessed = []
    
    won = False
    
    print('---------------')
    print('You have ' + str(warnings) + ' warnings left.')
    while(num_guesses > 0):        
        print('You have ' + str(num_guesses) + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))
        
        hint = get_guessed_word(secret_word, letters_guessed);
        guess = str.lower(input('Please guess a letter: '))
        if(not str.isalpha(guess)):
            if(warnings > 0):
                warnings -= 1;
                print('Oops! That is not a valid letter. You have ' + str(warnings) + ' warnings left: ' + hint)
            else:
                num_guesses -= 1;
                print('Oops! That is not a valid letter. You have no warnings left so you lose one guess:  ' + hint)
            print('---------------\n')
            continue
        if(guess in letters_guessed):
            if(warnings > 0):
                warnings -= 1;
                print('Oops! You\'ve already guessed that letter. You now have ' + str(warnings) + ' warnings: ' + hint)
            else:
                num_guesses -= 1;
                print('Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: ' + hint)
            print('---------------\n')
            continue
        letters_guessed.append(guess);
        hint = get_guessed_word(secret_word, letters_guessed);
        
        if(guess in secret_word):
            print('Good guess: ' + hint)
        else:
            num_guesses -= 1;
            print('Oops! That letter is not in my word: ' + hint)
        print('---------------\n')
        
        if(is_word_guessed(secret_word, letters_guessed)):
            won = True
            break
    
    if(won):
        total_score = num_guesses * len(unique_letters(secret_word))
        print('Congratulations, you won!')
        print('Your total score for this game is: ' + str(total_score))
    else:
        print('Sorry you ran out of guesses. The word was '+ secret_word)
        
def unique_letters(word):
    unique = []
    for letter in word:
        if letter not in unique:
            unique.append(letter)
    return unique


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def makeHintToList(hint):
    hintli = []
    for achr in hint:
        if(str.isalpha(achr) or achr == '_' ):
            hintli.append(achr)
    return hintli

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    hintList = makeHintToList(my_word)
    my_word_len = len(hintList)
    other_word_len = len(other_word)
    
    if my_word_len != other_word_len:
        return False
    #hintList = makeHintToList(my_word)
    
    for i in range(len(hintList)):
        if(hintList[i] != '_'):
            if(hintList[i] !=  other_word[i]):
                return False
        else:
            if(other_word[i] in hintList):
                return False
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    wordlist
    possibleGuess = makeHintToList(my_word)
    possible = True
    possiblesList = []
    
    for word in wordlist :
        possible = True
        if(len(word) == len(possibleGuess)):
            for i in range(len(word)):
                if(possibleGuess[i] != '_'):
                    if(possibleGuess[i] != word[i]):
                        possible = False;
                        break
            if(possible):
                possiblesList.append(word)
                
    if(len(possiblesList) < 1):
        print ('No matches found')
    else:
        for word in possiblesList:
            print (word, end=' ')
        print()
                
    



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print("Welcome to the game Hangman!")
    sec_wrd_len = len(secret_word)
    print("I am thinking of a word that is " + str(sec_wrd_len) + " letters long.")
    
    warnings = 3;
    
    num_guesses = 6;
    letters_guessed = []
    
    won = False
    
    print('---------------')
    print('You have ' + str(warnings) + ' warnings left.')
    while(num_guesses > 0):        
        print('You have ' + str(num_guesses) + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))
        
        hint = get_guessed_word(secret_word, letters_guessed);
        guess = str.lower(input('Please guess a letter: '))
        
        if(guess == '*'):
            print('Possible word matches are: ')
            show_possible_matches(hint)
            print('---------------\n')
            continue
        
        if(not str.isalpha(guess)):
            if(warnings > 0):
                warnings -= 1;
                print('Oops! That is not a valid letter. You have ' + str(warnings) + ' warnings left: ' + hint)
            else:
                num_guesses -= 1;
                print('Oops! That is not a valid letter. You have no warnings left so you lose one guess:  ' + hint)
            print('---------------\n')
            continue
        if(guess in letters_guessed):
            if(warnings > 0):
                warnings -= 1;
                print('Oops! You\'ve already guessed that letter. You now have ' + str(warnings) + ' warnings: ' + hint)
            else:
                num_guesses -= 1;
                print('Oops! You\'ve already guessed that letter. You now have no warnings left so you lose one guess: ' + hint)
            print('---------------\n')
            continue
        letters_guessed.append(guess);
        hint = get_guessed_word(secret_word, letters_guessed);
        
        if(guess in secret_word):
            print('Good guess: ' + hint)
        else:
            num_guesses -= 1;
            print('Oops! That letter is not in my word: ' + hint)
        print('---------------\n')
        
        if(is_word_guessed(secret_word, letters_guessed)):
            won = True
            break
    
    if(won):
        total_score = num_guesses * len(unique_letters(secret_word))
        print('Congratulations, you won!')
        print('Your total score for this game is: ' + str(total_score))
    else:
        print('Sorry you ran out of guesses. The word was '+ secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    
