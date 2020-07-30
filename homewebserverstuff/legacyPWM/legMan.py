from hashlib import sha256


def createPW(input_Str, flags, result_len):
    alphaNumStuff = ["abcdefghijklm",
                     "nopqrstuvwxyz",
                     "ABCDEFGHIJKLM",
                     "NOPQRSTUVWXYZ",
                     "0123456789",
                     "()= !\\$%&/",
                     "@#°?\"{[]}*+'~"]
    increment = int(64 / result_len)
    output = ""

    for i in range(0, len(input_Str), increment):
        subStr = input_Str[i:i + increment]
        str_index = getStrIndex(subStr)
        list_index = getListIndex(subStr, str_index, flags)
        while str_index >= len(alphaNumStuff[list_index]):
            str_index -= len(alphaNumStuff[list_index])
        output += alphaNumStuff[list_index][str_index]
    return output


def getStrIndex(input_Str):
    output = 0
    switch = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
              "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    for i in range(len(input_Str)):
        output += switch[input_Str[i]]
    return output


def getListIndex(input_Str, str_index, flags):
    output = 0
    max_output = 0
    switch = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
              "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    flag_switch = {8: 2, 12: 4, 13: 5, 15: 7}

    output += switch[input_Str[1]]
    output += str_index
    try:
        max_output = flag_switch[flags]
    except KeyError:
        max_output = 2

    while (output - max_output) >= 0:
        output -= max_output
    return output


def getPW(username, password, website, pw_len, numbers, specials):
    """arguments:
            username, password, website: strings
            pw_len: int (has to be a power of 2, min 2^0, max 2^6)
            numbers, specials: bools

    returns:
            password: string/None
            errorMsg: None/string
    """
    flags = 12
    allowed_lengths = [1, 2, 4, 8, 16, 32]

    if numbers:
        flags += 1
    if specials:
        flags += 2

    if username == "" or password == "" or website == "":
        return None, "username, password and website all have to be filled in."

    if pw_len not in allowed_lengths:
        return None, "pw_len not allowed."

    concatInfo = username + password + website
    shaResult = sha256(concatInfo.encode()).hexdigest()
    return createPW(shaResult, flags, pw_len), None