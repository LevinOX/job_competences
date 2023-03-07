import csv
import spacy
nlp = spacy.load("de_core_news_lg") # de_core_news_lg and sm

with open("usual_words_de.csv", "r") as g:
    # the reader creates a list of lists, the sum makes a list of
    # entries/lines:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
    usual_words = [word.lower() for word in usual_words]
with open("competences.csv", "r") as h:
    competences = sum(list(csv.reader(h, delimiter=',')), [])

print("len(competences): ", len(competences))

false_words = []
for word in competences:
    if nlp(word).has_vector:
        false_words.append(word)

print(len(false_words))

with open('caught_competences_lg.txt', 'w') as file:
    for item in false_words:
        file.write(item + '\t')
