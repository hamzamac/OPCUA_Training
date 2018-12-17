

string = "[1,3,4]"

def str_2_array(string, func):
    if len(string)>2:
        return [func(x) for x in string.strip('[').strip(']').split(',')] 
    else:
        return []

print(str_2_array(string, bool))