"""a first try to filter the job competences out of a text"""
# nltk-library may help with stemming and more
# For stemming, check out: PorterStemmer, WordNetLemmatizer,
# SnowballStemmer (german & english) from nltk or Spacy
# For many words see "nltk words" (though maybe only english)
# from collect_words import filter_string
# NLTK seems to be the best, but do not have words for german.
# check out "GermaNLTK" implementation or PyGermanet:
# https://pypi.org/project/pygermanet/
import csv
# import os
import re


def filter_string(string):
    string = re.sub(r'[^a-zA-Z\säöüÄÖÜß-]', '', string)
    string = string.replace('--', '-')
    string = re.sub(r'[\n\t\xa0]+', ' ', string)
    string = string.lower()
    return string


with open("job_description.txt", "r", encoding='utf-8') as f:
    jdescription = filter_string(f.read(1000))
    jdes = tuple(jdescription.split(sep=' '))
with open("usual_words_de.csv", "r") as g:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
    # usual_words = g.read()  # <-- list
with open("competences.csv", "r") as h:
    # str_comp = h.read()
    competences = sum(list(csv.reader(h, delimiter=',')), [])

print(f"list of competences: \n{competences}")
print(f"job description: {jdescription}")
print(usual_words[:20])

# job_data-structure: [['URL', 'job_title', ['comp1', 'comp2', 'comp3']],
#                       ['URL2', 'job_title2', ['comp1', 'comp2', 'comp3']],
#                       ['URL3', ..., [...]]] and so forth.
print("count('http'): ", jdes.count('http'))
job_data = [[None, None, set()]
            for i in range(jdes.count('http'))]  # count number of URLs in 'jdes'
new_words = []
new_competences = []

# job_data[0][0] = 'URL'
# job_data[0][1] = 'job_title'


# all this could run with a .. decorator(?) to ensure that the progress is
# saved, even if it is interrupted.

# Two processes:
# 1. sort known competences into a list to describe the job
# 2. if word not known, ask if it is a competence or not, add it to list
#    'usual_words' or 'competences' and, in latter case, add to list to
#    describe the job.

for word in jdes:
    if word in usual_words:
        print(f"'{word}' in usual_words!")
    if (word not in usual_words) and (word not in new_words):  # and len(word) > 1:
        if word in competences or word in new_competences:
            # add to job_data set
            job_data[0][2].add(word)
            print(f"'{word}' added to job_data.")

        else:
            # ask to either add to job competences
            # or to usual words.
            sorted = False
            while not sorted:
                answer = input(f"is '{word}' a competence? [y/n]: ")
                if answer == "y":
                    new_competences.append(word)
                    job_data[0][2].add(word)
                    print(f"'{word}' added to new_competences.")
                    print(f"'{word}' added to job_data.")
                    sorted = True
                elif answer == "n":
                    new_words.append(word)
                    print(f"'{word}' added to new_words.")
                    sorted = True
                else:
                    print("Please choose 'y' or 'n'.")
    print("new_words: ", new_words)
    print("new_competences: ", new_competences)


with open("usual_words_de.csv", "a") as g:
    writer = csv.writer(g)
    writer.writerow(new_words)
    # usual_words = list(csv.writer(g, delimiter=','))
    # usual_words = g.read()  # <-- list
with open("competences.csv", "a") as h:
    writer = csv.writer(h)
    writer.writerow(new_competences)
    # str_comp = h.read()
    # competences = list(csv.reader(h, delimiter=','))

with open("job_data.csv", "a") as i:
    writer = csv.writer(i)
    writer.writerow(job_data)
