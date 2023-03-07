# import nltk

# if 'german' in nltk.corpus.words.fileids():
#     german_words = nltk.corpus.words.words('german')
#     print(len(german_words))
# else:
#     print("German word list not found in NLTK.")

import spacy

nlp = spacy.load("de_core_news_lg") # de_core_news_lg

word = "Stromboot"
doc = nlp(word)

if doc.has_vector:
# if word in nlp.vocab:
    print(f"{word} is in the vocabulary.")
else:
    print(f"{word} is not in the vocabulary.")
