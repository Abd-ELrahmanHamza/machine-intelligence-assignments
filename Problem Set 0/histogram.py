from typing import Any, Dict, List
import utils


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the
    list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} 
    since 3 appears twice while 5 appears once 
    '''
    # TODO: ADD YOUR CODE HERE
    result_dict = {}
    for value in values:
        if value in result_dict:
            result_dict[value] += 1
        else:
            result_dict[value] = 1
    return result_dict


if __name__ == "__main__":
    print(histogram([1, 2, 3, 4, 1, 2, 3]))
