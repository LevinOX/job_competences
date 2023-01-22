"""a first try to filter the job competences out of a text"""
from collect_words import filter_string
import csv

with open("job_descriptions.txt", "r") as f:
    jdescription = filter_string(f.read())
    jdes = tuple(jdescription.split(sep=' '))
with open("usual_words_de.csv", "r") as g:
    usual_words = list(csv.reader(g, delimiter=','))
    # usual_words = g.read()  # <-- list
with open("competences.csv", "r") as h:
    # str_comp = h.read()
    competences = list(csv.reader(h, delimiter=','))

# all this could run with a .. decorator(?) to ensure that the progress is
# saved, even if it is interrupted.

# Two processes:
# 1. sort known competences into a list to describe the job
# 2. if word not known, ask if it is a competence or not, add it to list
#    'usual_words' or 'competences' and, in latter case, add to list to
#    describe the job.
for word in jdes:
    if word not in usual_words and len(word) > 1:
        if word in competences:
            # add to competence list

        else:
            # ask to either add to job competences
            # or to usual words.
            sorted = False
            while not sorted:
                answer = input(f"is {word} a competence? [y/n]: ")
                if answer = "y":
                    competences.append(word)
                    sorted = True
                elif answer = "n":
                    usual_words.append(word)
                    sorted = True
                else:
                    print("Please choose 'y' or 'n'.")
