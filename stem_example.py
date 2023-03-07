from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
#print(" ".join(SnowballStemmer.languages))
stemmer = SnowballStemmer("english")
plurals = ['caresses', 'flies', 'dies', 'mules', 'denied',
           'died', 'agreed', 'owned', 'humbled', 'sized',
           'meeting', 'stating', 'siezing', 'itemization',
           'sensational', 'traditional', 'reference', 'colonizer',
           'plotted']
singles = [stemmer.stem(plural) for plural in plurals]
# print(' '.join(singles))
# import nltk
# nltk.download('punkt')
# print("Imported stem.")

import nltk
# nltk.download('punkt')
# nltk.download('words')
nltk.download('german')
from nltk.tokenize import word_tokenize

word = "Haus"
tokens = word_tokenize(word, language='german')
# nltk.tokenize.WordPunctTokenizer().tokenize(german)
if tokens[0] in nltk.corpus.words.words(language='german'):
    print("The word '{}' is in the nltk library.".format(word))
else:
    print("The word '{}' is not in the nltk library.".format(word))