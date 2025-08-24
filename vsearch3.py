def search4vowels(word:str) -> set:
    """Return any vowels found in a supplied word."""
    vowels=set('aeiou')
    return vowels.intersection(set(word))
    

word= input("Provide a word to search for vowels: ")
print(search4vowels(word))
