def search4vowels(word):
    """Display any vowels in an asked for word."""
    vowels=set('aeiou')
    found = vowels.intersection(set(word))
    return bool(found)

word= input("Provide a word to search for vowels: ")
print(search4vowels(word))
