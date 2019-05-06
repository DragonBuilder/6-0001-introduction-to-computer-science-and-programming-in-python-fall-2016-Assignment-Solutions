# Problem Set 4A
# Name: <aneesh anil>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    ## base case, one letter in sequence(or less), return same as a list
    if (len(sequence) <= 1):
        return [sequence]

    ## Not base case----------

    ## all the possible permutations of sequence will be stored
    all_permutations = []

    ## first letter in sequence is stored
    current_char = sequence[0]

    ## remaining character of the sequence
    rem_sequence = sequence[1:]

    ## get all possible permutations of remaining
    ## characters (other than first character in sequence) as list
    ## uses recursion
    permutations = get_permutations(rem_sequence)

    ## insert the first letter (of sequence) which was saved, into all possible places in each element in
    ## permutations list, to get all possible permuations for the given sequence
    for a_word in permutations:
        perm_with_cur_word = get_combo_with_letter(current_char, a_word)
        all_permutations += perm_with_cur_word

    ## return permutations
    return all_permutations


## helper function, not in original template of ps4a.py
## takes a letter and a word
## returns a list
## the returned list is such that it contains all different ways the letter can be inserted into the word
def get_combo_with_letter(letter, word):
    final_list = []
    ## start from ZERO, and end at length value of word
    for i in range(0, len(word) + 1):
        ## split the word into two parts
        pre = word[:i]
        post = word[i:]

        ## get one possible permutation
        one_perm = pre + letter + post

        ## save current permutation
        final_list.append(one_perm)

    ## return list of all possible ways the letter could be inserted into word
    return final_list


if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)
    example_input = 'cat'
    print('Input:', example_input)
    print('Expected Output:', ['cat', 'act', 'atc', 'cta', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_input))
