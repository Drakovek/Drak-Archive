def clean_list(input_list:list=None) -> list:
    """
    Cleans a given list to contain no duplicates or entries with no value.
    
    Parameters:
        input_list (list): List to clean
    
    Returns:
        list: Cleaned version of the input_list
    """
    if input_list == None:
        return []
    output_list = input_list
    #REMOVE EMPTY ENTRIES
    count = 0
    while count < len(output_list):
        if output_list[count] == None or output_list[count] == "":
            del output_list[count]
        else:
            count = count + 1
    
    #REMOVE DUPLICATE ENTRIES
    count = 0
    while count < len(output_list):
        comp = count + 1
        while comp < len(output_list):
            if output_list[count] == output_list[comp]:
                del output_list[comp]
            else:
                comp = comp + 1
        count = count + 1
    return output_list

def list_to_string(input_list:list=None) -> str:
    """
    Converts a list to a string with entries separated by commas.
    
    Parameters:
        input_list (list): List to convert to string
    
    Returns:
        str: Converted string
    """
    if input_list == None:
        return ""
    result = ""
    for next_string in input_list:
        if not next_string == None and not next_string == "":
            if result == "":
                result = next_string
            else:
                result = result + "," + next_string
    return result
    
    