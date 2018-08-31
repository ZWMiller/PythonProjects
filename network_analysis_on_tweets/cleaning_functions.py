import string
import numpy as np

available_chars = string.printable

def clean_user_name(raw_user_name):
    assert type(raw_user_name) == str, "Not a valid user_name type, must be string"
    usable_chars = [x for x in  raw_user_name if x in available_chars]
    user_name =  ''.join(usable_chars).strip()
    if not user_name:
        return "NAN"
    return user_name