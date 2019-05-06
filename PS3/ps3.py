# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Aneesh Anil
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    firstcomponent = 0; # first component of the score
    secondcomponent = 0 # second component of the score
    #word = word.trim();
    word = word.lower();
    
    #compute first component of the score
    for letter in word:
        firstcomponent += SCRABBLE_LETTER_VALUES.get(letter)
        
    # compute second component of the score
    wordlen = len(word)
    
    if(wordlen > 0):
        secondcomponent = 7*wordlen - 3*(n-wordlen)
        # should always be greater than or equal to one
        if secondcomponent < 1 :
            secondcomponent = 1
    
    #final score
    score = firstcomponent * secondcomponent;
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    # 1/3 rd  - 1 vowels
    num_vowels = int(math.ceil(n / 3)) - 1
    
    # one '*' in every hand
    hand['*'] = 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    
    # make words lowercase and get a copy of hand
    word_lower = word.lower();
    newHand = hand.copy()
    
    # for every letter in the word
    for letter in word_lower:
        inHand = newHand.get(letter, 0);
        # if that letter is in hand, reduce its count by one
        if(inHand > 0):
            inHand -= 1;
            newHand[letter] = inHand
            
    # return the updated hand
    return newHand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    lower_word = word.lower()
    updated_hand = hand
    
    ## check if any wildcard is present in the word, and if so then check if any valid words can be
    ## formed 
    if "*" in lower_word:
        wildcard_index = lower_word.find("*")
        if(not isWildcardWordValid(lower_word, wildcard_index, word_list)):
            return False
    
    ## no wildcards, check if it's a valid word
    elif lower_word not in word_list:
        return False
    
    ## check if the given word can be constructed from the given hand
    for letter in lower_word:
        try:
            if updated_hand[letter] > 0:
                updated_hand = update_hand(updated_hand, letter)
            else:
                return False
        except KeyError:
            return False
    
    return True

## helper, return True if a word with wildcard ('*') can 
## atleast form one word with '*' replaced by vowel
def isWildcardWordValid(word, wildcard_index, word_list):
    
    ## sub string of the given word till the * 
    till_wildcard = word[:wildcard_index]
    
    ## sub string of the given word after the *
    after_wildcard = word[wildcard_index+1:]
    
    ## a list of possible valid word(s) that can be formed by the given word with wildcard
    possible_words = []
    #possible_with_vowels = []
    
    # check if any valid word can be formed with any letter in alphabet substituted 
    # in place of wildcard('*')
    for a_word in word_list:
        ## a word is only a possiblity if the word with wildcard and word under consideration(a_word) have
        ## 1) same length
        ## 2) characters before wildcard matching exactly
        ## 3) characters after the wildcard matching exactly
        if len(a_word) == len(word) and (till_wildcard == a_word[0:wildcard_index]) and (after_wildcard == a_word[wildcard_index+1:]) :
            possible_words.append(a_word)
            
    # from the posssible words list from above, check if any word(s) in that list is such that,
    # a vowel can occupies the place of wildcard ('*')
    for a_word in possible_words:
        if a_word[wildcard_index] in VOWELS:
            return True
            #possible_with_vowels.append(a_word)
            
            # small optimization, since atleast one word is possible end
            #break
    
#    if len(possible_with_vowels) > 0:
#        return True
    return False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # get a list of keys of the hand dictionary
    hand_keys = hand.keys()
    
    # find the length of the hand
    len_hand = 0
    for a_key in hand_keys:
        len_hand += hand[a_key]
        
    # return hand's length
    return len_hand

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # Keep track of the total score
    total_score = 0
    
    current_hand = hand.copy()
    len_hand = calculate_handlen(current_hand)
    
    # As long as there are still letters left in the hand:
    while len_hand > 0:
    
        # Display the hand
        print("Current hand:" , end = " ")
        display_hand(current_hand)
        
        # Ask user for input
        user_word = input("Enter word, or \"!!\" to indicate that you are finished: ");
        # If the input is two exclamation points:
        if(user_word == "!!"):
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(user_word, current_hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                score = get_word_score(user_word, len_hand)
                total_score += score
                print(user_word + " earned " + str(score) + " points. Total: " + str(total_score))

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
            
            # update the user's hand by removing the letters of their inputted word
            current_hand = update_hand(current_hand, user_word)
            len_hand = calculate_handlen(current_hand)
            
    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if len_hand < 1:
        print("Ran out of letters.", end=" ")
    print("Total score for this hand: " + str(total_score))

    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # make a copy of hand
    cur_hand = hand.copy()
    
    # how many occurances of the letter to be substituted?
    num_letter = cur_hand.get(letter, 0)
    
    # if the letter given by user is not in hand, return the same hand
    if num_letter < 1:
        return hand
    
    ## get all letters in the english alphabet
    choose_from = list(string.ascii_letters[:26])
    already_in_hand = cur_hand.keys()
    
    # remove letters in the hand, so the new letter chosen would be a 
    # letter not already present in hand 
    for letter_in_hand in already_in_hand:
        try:
            choose_from.remove(letter_in_hand)
        except ValueError:
            continue
        
    # move the letter from the current hand
    del cur_hand[letter]
    
    # choose a new letter at random
    new_letter_for_hand = random.choice(choose_from)
    
    # add it to the hand
    cur_hand[new_letter_for_hand] = num_letter
    
    #return new hand
    return cur_hand
    
    
    
    
    
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    ## total number of hand the players wnats to play
    total_hands = int(input('Enter total number of hands: '))
    
    #total score over all hands
    total_score = 0
    
    #flags, for choice for substituting a letter in a hand and replaying a hand
    can_substitute_letter = True
    can_replay_hand = True
    
    # play as many hands as given by user, one at a time
    while(total_hands > 0):
        
        # get a random hand
        hand = deal_hand(HAND_SIZE)
        
        print("Current hand: ", end=' ')
        display_hand(hand)
        
        # if the player has not used up the uption to substitue a letter, 
        # ask whether the player would like to do so.
        if(can_substitute_letter):
            wants_to_substitue = input('Would you like to substitue a letter? ')
            # everything other than a "yes" is a "no"
            if(wants_to_substitue.lower() == 'yes'):
                #replace the desired letter
                letter_to_substitue = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, letter_to_substitue)
                # cannot replace any more letters
                can_substitute_letter = False
                
        
        # play a hand
        current_hand_score = play_hand(hand, word_list)
        total_hands -= 1
        
        print('-------')
        
        # if the player has not used up the option to rplay a hand
        # ask if the player would like to do so.
        if(can_replay_hand):
            wants_to_replay = input('Would you like to replay the hand? ')
            # everything other than a "yes" is a "no"
            if(wants_to_replay.lower() == "yes"):
                # play a hand, with same hand values as previous
                new_score = play_hand(hand, word_list)
                print('-------')
                
                # cannot replay a hand anymore
                can_replay_hand = False
                
                #the score for current hand would be the best among the 
                # two hands played i.e., original vs replayed
                if(new_score > current_hand_score):
                    current_hand_score = new_score
                    
        # add the score to the total game score
        total_score += current_hand_score
        
    ## game over, display total score across all hands
    print("Total score over all hands: " + str(total_score))


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
    #display_hand(update_hand({'j':2, 'o':1, 'l':1, 'w':1, 'n':2} , 'jolly'))
    #display_hand(update_hand({'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1} , 'quail'))
