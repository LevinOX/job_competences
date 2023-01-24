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
    # TODO: allow capitalized words in competences -> move this to the check
    # of allowed words.
    # string = string.lower()
    return string


def sort_competences(jdes, usual_words, competences, job_data):
    """Two processes:
    1. sort known competences into a list to describe the job
    2. if word not known, ask if it is a competence or not, add it to list
   'usual_words' or 'competences' and, in latter case, add to list to
   describe the job."""
    # TODO: This function could run with a .. decorator(?) to ensure that the progress is
    # saved, even if it is interrupted.
    # TODO: Find double words like 'Pair Programming','lineare Algebra', CI/CD, clean code, design patterns, Fullstack Developer
    # TODO: allow '/'? What about 'vue.js' turning into 'vuejs'?
    # TODO: reduce words to stem
    new_words = []
    new_competences = []
    for word in jdes:
        # and len(word) > 1:
        if (word.lower() not in usual_words) and (word.lower() not in new_words):
            if word in competences or word in new_competences:
                # add to job_data set
                job_data[0][2].add(word)
                print(f"'{word}' added to job_data.")

            else:
                # ask to either add to job competences
                # or to usual words.
                sortbool = False
                while not sortbool:
                    answer = input(f"is '{word}' a competence? [y/n]: ")
                    if answer == "y":
                        new_competences.append(word)
                        job_data[0][2].add(word)
                        print(f"'{word}' added to new_competences.")
                        print(f"'{word}' added to job_data.")
                        sortbool = True
                    elif answer == "n":
                        new_words.append(word.lower())
                        print(f"'{word}' added to new_words.")
                        sortbool = True
                    else:
                        print("Please choose 'y' or 'n'.")
        else:
            print(f"'{word}' in usual_words! (or new_words)")
        # print("new_words: ", new_words)
        # print("new_competences: ", new_competences)
    return job_data, new_words, new_competences


def append_to_file(filename, content):
    """function to append content to file"""
    with open(filename, "a", encoding='utf-8') as g:
        writer = csv.writer(g)
        writer.writerow(content)


with open("job_description.txt", "r", encoding='utf-8') as f:
    jdescription = filter_string(f.read(3000))
    jdes = tuple(filter(None, jdescription.split(sep=' ')))
with open("usual_words_de.csv", "r") as g:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
with open("competences.csv", "r") as h:
    competences = sum(list(csv.reader(h, delimiter=',')), [])

print(f"list of competences: \n{competences}")
print(f"job description: {jdescription}")
print(usual_words[:20])

# job_data-structure: [['URL', 'job_title', ['comp1', 'comp2', 'comp3']],
#                       ['URL2', 'job_title2', ['comp1', 'comp2', 'comp3']],
#                       ['URL3', ..., [...]]] and so forth.
job_data = [[None, None, set()]
            for i in range(jdes.count('http'))]  # count number of URLs in 'jdes'


job_data, new_words, new_competences = sort_competences(
    jdes, usual_words, competences, job_data)

print("job_data: ", job_data)
print("new_competences: ", new_competences)
print("new_words: ", new_words)

append_to_file("usual_words_de.csv", new_words)
append_to_file("competences.csv", new_competences)
append_to_file("job_data.csv", job_data)
# with open("competences.csv", "a", encoding='utf-8') as h:
#     writer = csv.writer(h)
#     writer.writerow(new_competences)

# with open("job_data.csv", "a", encoding='utf-8') as i:
#     writer = csv.writer(i)
#     writer.writerow(job_data)
