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
        if output_list[count] == None or len(output_list[count]) == 0:
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