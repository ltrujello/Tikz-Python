def brackets(string):
    """A helper function for creating tikz code.
    Basically, if the string is empty, we don't obtain brackets [].
    """
    if len(string) != 0:
        return "[" + string + "]"
    else:
        return ""