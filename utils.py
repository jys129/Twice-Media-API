def compare_in_nocase(str1 = "", str2 = ""):
    """Compares if str1 is in str 2, ignoring case
    
    Arguments:
        str1 {string} -- The string to find
        str2 {string} -- The string to search in
    """    
    # Important to note that this won't work in some edge cases e.g. greek letters
    # However, since this will mostly be dealing with ASCII and sometimes korean hangul characters,
    # this shouldn't be a problem.
    if str1.upper().lower() in str2.upper().lower():
        return True
    else:
        return False