vowels = {'a','e','i','o','u'}
word= input("Enter your word: ")
i = vowels.intersection(set(word))
for ch in i:
    print(ch)
