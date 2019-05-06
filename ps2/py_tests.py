# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 15:28:59 2018

@author: White Dragon
"""
import string
# =============================================================================
# def get_guessed_word(secret_word, letters_guessed):
#     '''
#     secret_word: string, the word the user is guessing
#     letters_guessed: list (of letters), which letters have been guessed so far
#     returns: string, comprised of letters, underscores (_), and spaces that represents
#       which letters in secret_word have been guessed so far.
#     '''
#     guess_string = ''
#     for letter in secret_word:
#         if letter in letters_guessed:
#             guess_string += letter
#         else:
#             guess_string += '_ '
#             
#     return guess_string
# 
# secret_word= 'apple'
# letters_guessed = ['k','s','z','f','r','s']
# 
# print(get_guessed_word(secret_word, letters_guessed))
# =============================================================================
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
    
print(get_available_letters(['e','i','k','p','r','s']))