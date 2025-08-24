def search4letters(phrase:str, letters:str = 'aeiou')-> set:
    """Return the set of letters in the phrase."""
    return set(letters).intersection(set(phrase))
#keyword assignment
print ( search4letters(letters='xye',phrase='Helllloooo'))
        
