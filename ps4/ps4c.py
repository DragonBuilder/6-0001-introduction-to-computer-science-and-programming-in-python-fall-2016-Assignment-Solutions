# Problem Set 4C
# Name: <Aneesh Anil>
# Collaborators:
# Time Spent: x:xx

import string, copy, random
from ps4a import get_permutations

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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text, wordlist=None):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        
        if wordlist != None:
            self.wordlist = wordlist
        else:
            self.wordlist = load_words(WORDLIST_FILENAME)
        
        self.valid_words = self.compute_valid_words(self.message_text)
        
    # helper, not in original code
    def compute_valid_words(self, text):
        # list to store the valid words in the given text
        valid_words_list = []
        text_split = text.split(' ')
        
        #
        for a_word in text_split:
            # in each word, strip the word of any special character
            stripped_word = a_word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
            
            # if the srtripped_word is a valid word, add it to the appropriate list
            if is_word(self.wordlist, stripped_word):
                valid_words_list.append(a_word)
                
                
        #return a deep copy
        return valid_words_list[:]
            
        
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
        return self.valid_words[:]
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
#        VOWELS_LOWER = 'aeiou'
#        VOWELS_UPPER = 'AEIOU'
#        CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
#        CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'
        
        # the dictionary to map a letter to another letter, used to encrypt data
        encrypt_mapping_dict = {}
        
        # covert the vowels_permutation to lowercase letters
        vowels_permutation = vowels_permutation.lower()
        
        # map every vowel to another vowel from vowels_permutation
        for i in range(len(VOWELS_LOWER)):
            # map lowercase vowel
            encrypt_mapping_dict[VOWELS_LOWER[i]] = vowels_permutation[i]
            # map ippercase vowel
            encrypt_mapping_dict[VOWELS_UPPER[i]] = vowels_permutation[i].upper()
            
        # map consonants, mapped to itself, ie B -> B, g -> g
        for i in range(len(CONSONANTS_LOWER)):
            encrypt_mapping_dict[CONSONANTS_LOWER[i]] = CONSONANTS_LOWER[i]
            encrypt_mapping_dict[CONSONANTS_UPPER[i]] = CONSONANTS_UPPER[i]
            
        return copy.deepcopy(encrypt_mapping_dict)
                    
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        
        encrypted_message_text = ''
        
        # using the mapped dictionary, encrypt the message_text and return that.
        for a_char in self.message_text:
            # if the character is a special character, it remainins as it is.
            encrypted_message_text += transpose_dict.get(a_char, a_char)
            
        return encrypted_message_text
        
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        
        # get list of all possible permutations on vowels
        all_permutaions_on_vowels = get_permutations(VOWELS_LOWER)
        
        # how many valid words in the best transpose done till now
        valid_words_in_best_transpose = len(self.get_valid_words())
        
        # the best transposed string till now
        best_transpose_string = self.message_text
        
        # find the best transposed string, by trring all the differenr permutations of vowels
        for a_permutation in all_permutaions_on_vowels:
            #print('\ncurrent perm: ',a_permutation)
            transpose_dict = self.build_transpose_dict(a_permutation)
            
            current_transposed_message = self.apply_transpose(transpose_dict)
            #print('current transposed string: ', current_transposed_message)
            
            total_valid_words_in_transposed_string = len(self.compute_valid_words(current_transposed_message))
            #print('valid words in current transposed string: ',total_valid_words_in_transposed_string,'\n')
           
            # if the current transposed string is the best till now, save it!
            if(total_valid_words_in_transposed_string > valid_words_in_best_transpose):
                best_transpose_string = current_transposed_message
                valid_words_in_best_transpose = total_valid_words_in_transposed_string
                
        return best_transpose_string
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    textMessage = 'Eminem is probably the greated ever! Don\'t even doubt it.'
    sb = SubMessage(textMessage)
    print('Original message: ', textMessage)
    one_permutation_vowel = 'eouia'
    enc_dict = sb.build_transpose_dict(one_permutation_vowel)
    enc_message = sb.apply_transpose(enc_dict)
    print('Expected encryption: ', "Omunom us pribebly tho groetod ovor! Din't ovon diabt ut.")
    print('Actual encryption: ', enc_message)
    
    
    textMessage = 'Fly blackbird over middle east, tell nobody, not even Israel.'
    sb = SubMessage(textMessage)
    print('Original message: ', textMessage)
    one_permutation_vowel = 'ieaou'
    enc_dict = sb.build_transpose_dict(one_permutation_vowel)
    enc_message = sb.apply_transpose(enc_dict)
    print('Expected encryption: ', "Fly blickbard over maddle eist, tell nobody, not even Asriel.")
    print('Actual encryption: ', enc_message)
    
    enc_textMessage = 'Fly blickbard over maddle eist, tell nobody, not even Asriel.'
    ecM = EncryptedSubMessage(enc_textMessage)
    print('Original message: ', enc_textMessage)
    print('Expected decryption: ', 'Fly blackbird over middle east, tell nobody, not even Israel.')
    print('Actual decryption: ', ecM.decrypt_message())
    
    enc_textMessage = "Omunom us pribebly tho groetod ovor! Din't ovon diabt ut."
    ecM = EncryptedSubMessage(enc_textMessage)
    print('Original message: ', enc_textMessage)
    print('Expected decryption: ', 'Eminem is probably the greated ever! Don\'t even doubt it.')
    print('Actual decryption: ', ecM.decrypt_message())
