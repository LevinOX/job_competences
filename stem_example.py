from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
print(" ".join(SnowballStemmer.languages))
stemmer = SnowballStemmer("english")
plurals = ['caresses', 'flies', 'dies', 'mules', 'denied',
           'died', 'agreed', 'owned', 'humbled', 'sized',
           'meeting', 'stating', 'siezing', 'itemization',
           'sensational', 'traditional', 'reference', 'colonizer',
           'plotted']
singles = [stemmer.stem(plural) for plural in plurals]
print(' '.join(singles))
# import nltk
# nltk.download('punkt')
# print("Imported stem.")
