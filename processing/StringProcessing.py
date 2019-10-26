def extend_int(input_int:int=0, input_length:int=0) -> str:
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