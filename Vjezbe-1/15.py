vowels = "aeiouAEIOU"
consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

def count_vowels_and_consonants(s):
    vowel_count = sum(1 for char in s if char in vowels)
    consonant_count = sum(1 for char in s if char in consonants)
    return {'vowels': vowel_count, 'consonants': consonant_count}


tekst = "Python je programski jezik koji je jednostavan za učenje i korištenje. Python jevrlo popularan."
print(count_vowels_and_consonants(tekst))