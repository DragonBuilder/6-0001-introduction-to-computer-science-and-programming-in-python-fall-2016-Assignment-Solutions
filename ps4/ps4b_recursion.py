# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 23:34:46 2019

@author: Anil Kumar
"""

# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import copy

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text, wordlist = None):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        # save the text message receieved
        self.message_text = text
        
        if wordlist != None:
            self.wordlist = wordlist
        else:
            self.wordlist = load_words(WORDLIST_FILENAME)
            

        # find all the valid words in the text message and save them too!
        #wordlist = load_words(WORDLIST_FILENAME)
        self.valid_words = self.compute_valid_words(self.message_text)

    #  helper, not in original template, added
    #  gives a list of valid words in message_text of current object
    def compute_valid_words(self, text_message):

        # split text_message into list
        words_in_text = text_message.split(' ')

        #list, to build and store all valid words in text_message
        valid_words_in_text = []

        # check each word in the words_in_text, and save into valid_words_in_text if the word is a valid word
        for aWord in words_in_text:
            if(is_word(self.wordlist, aWord)):
                valid_words_in_text.append(aWord)

        return copy.deepcopy(valid_words_in_text)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return copy.deepcopy(self.valid_words)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        cipher_dict = {}
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase

        for i in range(len(lowercase_letters)):
            #letter = lowercase_letters[i]

            # get the index of the letter to be mapped with the letter at index i
            cipherletter_index = (i + shift) % 26
            cipher_dict[lowercase_letters[i]] = lowercase_letters[cipherletter_index]
            cipher_dict[uppercase_letters[i]] = uppercase_letters[cipherletter_index]

        return cipher_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        cipher_text = ''
        cipher_dict = self.build_shift_dict(shift)

        for each_letter in self.message_text:
            # search if current character in cipher_dict
            # if the character is a alphabet, there will be a corresponding encrypt letters
            # if the character is a punctuation/space, keep it as it is
            cipher_text_letter = cipher_dict.get(each_letter, each_letter)
            cipher_text += cipher_text_letter

        return cipher_text

class PlaintextMessage(Message):
    def __init__(self, text, shift, wordlist=None):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super(PlaintextMessage, self).__init__(text, wordlist)

        ## calling method to set inital vaules for self.shift, self.encryption_dict and self.get_message_text_encrypted
        self.change_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text, wordlist=None):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super(CiphertextMessage, self).__init__(text, wordlist)

    def decrypt_message(self, shift_to_apply = 0):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        # do only this many total recursions only
        MAX_SHIFTS = 26 
        
        # how many more recusions has to be done
        remaining_shifts_to_do = MAX_SHIFTS - shift_to_apply
        
        ## -----------------------------------------------------------------------------------------------------
        ## ------------------------------------------- BASE CASE -------------------------------------------------------------
        ## -----------------------------------------------------------------------------------------------------
        
        # this shift doesn't matter, don't shift , return a dummy tuple
        if remaining_shifts_to_do < 1:
            return (0, '')
        
        ## -----------------------------------------------------------------------------------------------------
        ## -----------------------------------------------------------------------------------------------------
        
        
        
        ## -----------------------------------------------------------------------------------------------------
        ## ------------------------------------------- NOT BASE CASE -------------------------------------------------------------
        ## -----------------------------------------------------------------------------------------------------
        
        ## create a PlaintextMessage object, shift_to_apply is the shift value passed to constructor
        one_possible_shifted_object = PlaintextMessage(self.message_text, shift_to_apply, self.wordlist)
        # print('Shifted message: '+ one_possible_shifted_object.get_message_text_encrypted())
        
        ## get the value of string after shifting by shift_to_apply
        shifted_text = one_possible_shifted_object.get_message_text_encrypted()

        # how many valid words were found in the current
        MAX_VALID_WORDS_IN_CURRENT_SHIFT = len(self.compute_valid_words(shifted_text))
        #print('Valid words in shifted message: '+ str(MAX_VALID_WORDS_IN_CURRENT_SHIFT))

        # the tuple with current shift value and shifted text
        current_shift_with_shifted_text_tuple = (one_possible_shifted_object.get_shift(), shifted_text)
        
        # (best among the rest tuple) tuple with best shift value and shifted text after doing rest of the shifts
        best_shift_tuple_in_remaing_shifts = self.decrypt_message(shift_to_apply + 1)
        
        # get the number of valid words of the text in index 1 of best_shift_tuple_in_remaing_shifts tuple
        MAX_VALID_WORDS_IN_BEST_DECRYPT_IN_REMAINING_SHIFTS = len(self.compute_valid_words(best_shift_tuple_in_remaing_shifts[1]))
        
        # if the shift produced by best among the rest tuple is better than the current applied shift tuple, then 
        if MAX_VALID_WORDS_IN_BEST_DECRYPT_IN_REMAINING_SHIFTS > MAX_VALID_WORDS_IN_CURRENT_SHIFT:
            # return best among rest tuple
            return best_shift_tuple_in_remaing_shifts
        
        # return the tuple produced by the current shift value and it's shufted string
        # NOTE: this tuple is returned even if current applied shift value produced same number of valid words as best among the rest tuple ,
        # This is done to get rid of basecase tuple at the earliest recursion
        return current_shift_with_shifted_text_tuple
    



if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())
   
    #wordlist = load_words(WORDLIST_FILENAME)
    
    ## test case (PlaintextMessage)
    print('\n----------test case (PlaintextMessage)----------\n')

    text = 'deception is the skill to trick your enemy into submission, willingly'
    ptM1 = PlaintextMessage(text, 4)
    print('Input: '+ text)
    print('Excpected Output: higitxmsr mw xli wompp xs xvmgo csyv iriqc mrxs wyfqmwwmsr, amppmrkpc')
    print('Actutal Output: ' + ptM1.get_message_text_encrypted())
    
    text = 'Gudio Van Russo is a saint!'
    ptM1 = PlaintextMessage(text, 17)
    print('\nInput: '+ text)
    print('Excpected Output: Xluzf Mre Iljjf zj r jrzek!')
    print('Actual Output:' + ptM1.get_message_text_encrypted())
    
    # test case (CiphertextMessage)
    print('\n----------test case (CiphertextMessage)----------\n')
    
    text = 'Xluzf Mre Iljjf zj r jrzek!'
    ctM1 = CiphertextMessage(text)
    print('Input: '+ text)
    print('Excpected Output: (9, Gudio Van Russo is a saint!)')
    print('Actual Output:' + str(ctM1.decrypt_message()))
    
    text = 'higitxmsr mw xli wompp xs xvmgo csyv iriqc mrxs wyfqmwwmsr, amppmrkpc'
    ctM1 = CiphertextMessage(text)
    print('\nInput: '+ text)
    print('Excpected Output: (22, deception is the skill to trick your enemy into submission, willingly)')
    print('Actual Output:' + str(ctM1.decrypt_message()))
    
    # best shift value and unencrypted story
    # best shift value is 12
    # unencrypted story is ------> 
    
    # Jack Florey is a mythical character created on the spur of a moment to help
    # cover an insufficiently planned hack. He has been registered for classes at 
    # MIT twice before, but has reportedly never passed aclass. It has been the
    # tradition of the residents of East Campus to become Jack Florey for a few 
    # nights each year to educate incoming students in the ways, means, and ethics 
    # of hacking.

## inefficient solution for decrypt_message()
# class CiphertextMessage(Message):
#     def __init__(self, text):
#         '''
#         Initializes a CiphertextMessage object
#
#         text (string): the message's text
#
#         a CiphertextMessage object has two attributes:
#             self.message_text (string, determined by input text)
#             self.valid_words (list, determined using helper function load_words)
#         '''
#         super(CiphertextMessage, self).__init__(text)
#
#     def decrypt_message(self):
#         '''
#         Decrypt self.message_text by trying every possible shift value
#         and find the "best" one. We will define "best" as the shift that
#         creates the maximum number of real words when we use apply_shift(shift)
#         on the message text. If s is the original shift value used to encrypt
#         the message, then we would expect 26 - s to be the best shift value
#         for decrypting it.
#
#         Note: if multiple shifts are equally good such that they all create
#         the maximum number of valid words, you may choose any of those shifts
#         (and their corresponding decrypted messages) to return
#
#         Returns: a tuple of the best shift value used to decrypt the message
#         and the decrypted message text using that shift value
#         '''
#         # do a shift of message_text for 0 to MAX_SHIFTS
#         MAX_SHIFTS = 25
#
#         # how many valid words were found in the best shift done till now, initialized with current values
#         MAX_VALID_WORDS_IN_DECRYPT = len(self.valid_words)
#
#         # tuple, has the best shift value and the decrypted message for that shift value, initialized with current values
#         best_decrypt = (MAX_VALID_WORDS_IN_DECRYPT, self.message_text)
#
#         # do a shift for each possiblity
#         for current_shift in range(1, MAX_SHIFTS):
#             # get the shifted text
#             one_possible_decrypted_text = self.apply_shift(current_shift)
#
#             # Make a message Object, so that get_valid_words() method can be used
#             one_possible_decrypted_message = Message(one_possible_decrypted_text)
#
#             # for the text with current shift applied, get how many valid words are in that text
#             total_valid_words_in_current_shift = len(one_possible_decrypted_message.get_valid_words())
#
#             # is the number of valid words present in the current shifted text best till now?
#             if total_valid_words_in_current_shift > MAX_VALID_WORDS_IN_DECRYPT :
#                 # if so, update
#                 best_decrypt = (total_valid_words_in_current_shift, one_possible_decrypted_text)
#                 MAX_VALID_WORDS_IN_DECRYPT = total_valid_words_in_current_shift
#
#         return best_decrypt
#
