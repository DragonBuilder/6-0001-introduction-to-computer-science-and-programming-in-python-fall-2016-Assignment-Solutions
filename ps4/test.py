from ps4b import Message, PlaintextMessage, CiphertextMessage, get_story_string, load_words, WORDLIST_FILENAME
from ps4c import SubMessage
from ps4a import get_permutations

import random

def testMessage():
    message = Message("Let's surround Dunkirk, end brits")
    print(message.get_message_text())
    print(message.get_valid_words())
    print(message.apply_shift(8))

def testPlaintextMessage():
    # ptM = PlaintextMessage("Let's surround Dunkirk, end brits", 8)
    # print(ptM.get_shift())
    # print(ptM.get_encryption_dict())
    # print(ptM.get_message_text_encrypted())
    # ptM.change_shift(10)
    # print(ptM.get_shift())
    # print(ptM.get_encryption_dict())
    # print(ptM.get_message_text_encrypted())

    ptM = PlaintextMessage("Let's surround Dunkirk, end brits", 0)
    print(ptM.get_shift())
    print(ptM.get_encryption_dict())
    print(ptM.get_message_text_encrypted())
    ptM.change_shift(10)
    print(ptM.get_shift())
    print(ptM.get_encryption_dict())
    print(ptM.get_message_text_encrypted())

def testCiphertextMessage():
    ctM = CiphertextMessage("Tmb'a aczzwcvl Lcvsqzs, mvl jzqba")
    print(ctM.decrypt_message())
    
def testSubMessage():
    VOWELS = 'aeiou'
    PERMUTATIONS_OF_VOWELS = get_permutations(VOWELS)
    
    sM = SubMessage('aeiou, are el vowelso')
    current_transpose_perm = sM.build_transpose_dict(PERMUTATIONS_OF_VOWELS[random.randrange(len(PERMUTATIONS_OF_VOWELS))])
    print('Mapping dict: ', current_transpose_perm)
    print('Encrypted string: ', sM.apply_transpose(current_transpose_perm))



if __name__ == '__main__':
    # testMessage()
    # print('-----------------------')
    # testPlaintextMessage()
    #testCiphertextMessage()
    #wordlist = load_words(WORDLIST_FILENAME)
    
    #encrypted_story = get_story_string()
    #print(encrypted_story)
    #story = CiphertextMessage(encrypted_story)
    #decrypted_story = story.decrypt_message()
    #print(decrypted_story)
    
    testSubMessage()
