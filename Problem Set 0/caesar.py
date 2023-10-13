from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def decipher_word(ciphered_word: str, shift: int) -> str:
    deciphered_word = ""
    for char in ciphered_word:
        deciphered_word = deciphered_word + chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
    return deciphered_word


def decipher_sentence(ciphered_list, shift, dictionary_set):
    number_of_mismatch = 0
    deciphered = ""
    for ciphered_word in ciphered_list:
        deciphered_word = decipher_word(ciphered_word, shift)
        if deciphered_word not in dictionary_set:
            number_of_mismatch += 1
        deciphered += deciphered_word + " "
    return (deciphered, number_of_mismatch)


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    dictionary_set = set(dictionary)
    ciphered_list = ciphered.split()
    min_mismatch = 20000
    result_shift = 0
    result_deciphered = ""
    for shift in range(26):
        deciphered, number_of_mismatch = decipher_sentence(ciphered_list, shift, dictionary_set)
        if number_of_mismatch < min_mismatch:
            result_shift = shift
            result_deciphered = deciphered
            min_mismatch = number_of_mismatch
    return result_deciphered[:-1], result_shift, min_mismatch
