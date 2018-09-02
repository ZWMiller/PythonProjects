import string


def clean_user_name(raw_user_name):
    """
    Removes all unprintable characters from username and strips
    any extra spaces from beginning and end of string. If the
    username is then an empty string, returns a special case name
    for removal at a later time ("NAN")

    raw_user_name: The string to clean
    return: Cleaned username
    """
    assert type(raw_user_name) == str, "Not a valid user_name type, must be string"

    available_chars = string.printable
    usable_chars = [x for x in  raw_user_name if x in available_chars]
    user_name =  ''.join(usable_chars).strip()
    if not user_name:
        return "NAN"
    return user_name