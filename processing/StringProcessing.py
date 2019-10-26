def extend_int(input_int:int=0, input_length:int=0) -> str:
    """
    Returns a string representation of a given int with a given length, using leading zeros if necessary.
    If values are invalid, the function returns "0" or a string of zeros of the specified length.
    
    Parameters:
        input_int (int): Int value to return as string.
        input_length (int): Lenth of the string to return.
        
    Returns:
        str: String value of input_int with the length of input_length
    """
    if input_length == None or input_length == 0:
        return "0"
    if input_int == None:
        return extend_int(0, input_length)
    
    return_str = str(input_int)
    if input_length < len(return_str):
        return extend_int(0, input_length)
     
    while len(return_str) < input_length:
        return_str = "0" + return_str
    
    return return_str