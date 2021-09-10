#!/usr/bin/env python3

from dvk_archive.main.processing.string_processing import remove_whitespace
from typing import List

def separate_into_chunks(search:str=None) -> List[str]:
    """
    Separates boolean search string into parsable chunks.

    :param search: String using boolean search logic, defaults to None
    :type search: str, optional
    :return: List of chunks for boolean logic
    :rtype: list[str]
    """
    # Remove whitespace from start and end of string
    string = remove_whitespace(search)
    # Run through string, separating components
    chunks = []
    while len(string) > 0:
        if string[0] == "!" or string[0] == "-":
            # Separate not operator
            chunks.append("!")
            string = string[1:]
        elif string[0] == "&" or string[0] == "+":
            # Separate and operator
            chunks.append("&")
            string = string[1:]
        elif string[0] == "|" or string[0] == "~":
            # Separate or operator
            chunks.append("|")
            string = string[1:]
        elif string[0] == "(" or string[0] == "[":
            # Separate left paren operator
            chunks.append("(")
            string = string[1:]
        elif string[0] == ")" or string[0] == "]":
            # Separate right paren operator
            chunks.append(")")
            string = string[1:]
        elif string[0] == "'" or string[0] == "\"" or string[0] == "=":
            # Separate string in quotation marks
            char = string[0]
            end = string.find(char, 1)
            if end == -1:
                end = len(string)
            chunks.append(string[1:end])
            string = string[end:]
            if string.startswith(char):
                string = string[1:]
        else:
            # Separates standard strings
            end = 0
            while (end < len(string)
                        and not string[end] == " "
                        and not string[end] == ")"
                        and not string[end] == "]"):
                end += 1
            word = string[:end]
            string = string[end:]
            # Check if separated string is an operator
            if word.lower() == "and":
                # Replace AND with "&" operator
                word = "&"
            elif word.lower() == "or":
                # Replace OR with "|" operator
                word = "|"
            elif word.lower() == "not":
                # Replace NOT with "!" operator
                word = "!"
            chunks.append(word)
        # Remove whitespace from the start of the string
        string = remove_whitespace(string)
    return chunks

def is_string(chunk:str=None) -> bool:
    """
    Returns whether given boolean chunk is a string.
    Returns False if chunk is an operator symbol.

    :param chunk: Boolean chunk, defaults to None
    :type chunk: str, optional
    :return: Whether given chunk is a string
    :rtype: bool
    """
    # Return False if parameter is invalid
    if chunk is None:
        return False
    # Check if given chunk is an operator symbol
    if (chunk == "&"
            or chunk == "|"
            or chunk == "!"
            or chunk == "("
            or chunk == ")"):
        return False
    return True

def fix_logic(chunks:List[str]=None) -> List[str]:
    """
    Fixes any logic errors in a boolean search expression.
    Uses boolean search chunks from separate_into_chunks function.

    :param chunks: Boolean search chunks, defaults to None
    :type chunks: list[str], optional
    :return: Fixed list of boolean search chunks
    :rtype: list[str]
    """
    # Return empty list if parameters are invalid
    if chunks is None:
        return []
    # Remove leading operators
    fixed = chunks
    while len(fixed) > 0 and (fixed[0] == "&" or fixed[0] == "|"):
        del fixed[0]
    # Remove trailing operators
    while len(fixed) > 0 and (fixed[-1] == "&" or fixed[-1] == "|" or fixed[-1] == "!"):
        del fixed[len(fixed)-1]
    if len(fixed) == 0:
        return []
    # Complete left parens
    if "(" in fixed:
        index = fixed.index("(") + 1
        # Count parens after the first left paren
        left = 1
        right = 0
        while index < len(fixed):
            if fixed[index] == "(":
                left += 1
            elif fixed[index] == ")":
                right += 1
            index += 1
        # Add right parens if necessary
        if left > right:
            for i in range(0, left-right):
                fixed.append(")")
    # Complete right parens
    if ")" in fixed:
        # Get last index of right paren
        index = len(fixed) - 1
        while not fixed[index] == ")":
            index -= 1
        # Count parens before the last right paren
        left = 0
        right = 1
        index -= 1
        while index > -1:
            if fixed[index] == "(":
                left += 1
            elif fixed[index] == ")":
                right += 1
            index -= 1
        # Add left parens if necessary
        if right > left:
            for i in range(0, right-left):
                fixed.insert(0, "(")
    # Add AND operator to unlinked logic
    index = 1
    while index < len(fixed):
        if is_string(fixed[index]) and (is_string(fixed[index-1]) or fixed[index-1] == ")"):
            fixed.insert(index, "&")
        elif fixed[index] == "(" and (fixed[index-1] == ")" or is_string(fixed[index-1])):
            fixed.insert(index, "&")
        elif fixed[index] == "!" and (fixed[index-1] == ")" or is_string(fixed[index-1])):
            fixed.insert(index, "&")
        index += 1
    # Add empty strings to hanging operators
    index = 0
    while index < len(fixed) - 1:
        if ((fixed[index] == "&" or fixed[index] == "|" or fixed[index] == "!")
                and (fixed[index+1] == "&" or fixed[index+1] == "|")):
            fixed.insert(index+1, "")
        if fixed[index] == "!" and fixed[index+1] == "!":
            fixed.insert(index+1, "")
        index += 1
    return fixed

def get_logic(chunks:List[str]=None) -> List:
    """
    Returns list with logic parameters from boolean logic chunks.
    [0] - Argument 1, string or nested logic
    [1] - Whether Argument 1 logic should be inverted
    [2] - Argument 2, string or nested logic
    [3] - Whether Argument 2 logic should be inverted
    [4] - Operator for comparing Arguments 1 and 2 (AND or OR)

    :param chunks: Valid boolean search chunks, defaults to None
    :type chunks: List[str]
    :return: Logic list
    :rtype: List
    """
    logic = [None, False, None, False, None]
    mod_chunks = []
    try:
        mod_chunks.extend(chunks)
        # Add first inversion if necessary
        if mod_chunks[0] == "!":
            logic[1] = True
            del mod_chunks[0]
        if mod_chunks[0] == "(":
            # Get nested statement, if necessary
            del mod_chunks[0]
            section = []
            left = 1
            right = 0
            while not left == right:
                if mod_chunks[0] == "(":
                    left += 1
                elif mod_chunks[0] == ")":
                    right += 1
                section.append(mod_chunks[0])
                del mod_chunks[0]
            del section[len(section) - 1]
            logic[0] = get_logic(section)
        else:
            # Get first search string
            logic[0] = mod_chunks[0]
            del mod_chunks[0]
        if len(mod_chunks) > 0:
            # Get operator
            logic[4] = mod_chunks[0]
            del mod_chunks[0]
            # Add second inversion if necessary
            if len(mod_chunks) == 2 and mod_chunks[0] == "!":
                logic[3] = True
                del mod_chunks[0]
            if len(mod_chunks) > 1:
                # Get nested statement if necessary.
                logic[2] = get_logic(mod_chunks)
            else:
                # Get second search string
                logic[2] = mod_chunks[0]
                del mod_chunks[0]
        # Simplify logic
        if not logic[1] and type(logic[0]) is list and logic[2] is None:
            return logic[0]
        return logic
    except:
        return []

def get_logic_from_string(search:str=None) -> List:
    """
    Returns list with logic parameters from boolean search string.

    :param search: Boolean search string, defaults to None
    :type search: str, optional
    :return: Logic list
    :rtype: List
    """
    chunks = separate_into_chunks(search)
    chunks = fix_logic(chunks)
    logic = get_logic(chunks)
    return logic

def logic_to_lower(logic:List=None) -> List:
    """
    Converts all string arguments in a given logic list to lowercase.

    :param logic: Logic list, defaults to None
    :type logic: List, optional
    :return: Logic list with arguments converted to lowercase
    :rtype: List
    """
    try:
        # Convert arg1 to lowercase
        if type(logic[0]) is list:
            # Recurse if arg1 is a logic list
            logic[0] = logic_to_lower(logic[0])
        else:
            logic[0] = logic[0].lower()
        # Convert arg2 to lowercase
        if type(logic[2]) is list:
            # Recurse if arg2 is a logic list
            logic[2] = logic_to_lower(logic[2])
        else:
            logic[2] = logic[2].lower()
        # Return logic
        return logic
    except:
        return []

def get_arg_value(search=None,
            invert:bool=False,
            string:str=None,
            exact_match:bool=False) -> bool:
    """
    Returns whether given string matches the search string.
    Used for getting argument values in a greater search logic list.

    :param search: String to search for, defaults to None
    :type search: str, optional
    :param invert: Whether to invert the return bool, defaults to None
    :type invert: bool, optional
    :param string: String to search within, defaults to None
    :type string: str, optional
    :param exact_match: Whether strings have to match exactly or just contain value, defaults to False
    :type exact_match: bool, optional
    :return: Whether the given string matches the search
    :rtype: bool
    """
    value = False
    if type(search) is not list:
        # Compare strings if search is a string
        if exact_match:
            value = (search == string)
        else:
            value = search in string
    else:
        # get search_string result if search is a logic list
        value = search_string(search, string, exact_match)
    # Invert result if necessary
    if invert:
        return not value
    return value

def search_string(logic:List=None,
            string:str=None,
            exact_match:bool=False) -> bool:
    """
    Searches a given string for values specified in logic list.

    :param logic: Logic list to search string with, defaults to None
    :type logic: str, optional
    :param string: String to search for values within, defaults to None
    :type string: str, optional
    :param exact_match: Whether strings have to match exactly or just contain value, defaults to False
    :type exact_match:bool, optional
    :return: Whether given string matches the given logic
    :rtype: bool
    """
    try:
        if logic[4] == "&":
            # Compares argument values with AND operator
            return (get_arg_value(logic[0], logic[1], string, exact_match)
                        and get_arg_value(logic[2], logic[3], string, exact_match))
        elif logic[4] == "|":
            # Compares argument values with OR operator
            return (get_arg_value(logic[0], logic[1], string, exact_match)
                        or get_arg_value(logic[2], logic[3], string, exact_match))
        else:
            # Returns value of argument 1 if argument 2 doesn't exist
            return get_arg_value(logic[0], logic[1], string, exact_match)
    except:
        # Return False if comparing arguments fails
        return False
