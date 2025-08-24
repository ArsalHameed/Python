def search4letters(phrase:str, letters:str)-> set:
    """Return the set of letters in the phrase."""
    return set(letters).intersection(set(phrase))
