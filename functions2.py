import csv
import re


def filter_string(string):
    string = re.sub(
        r'[^a-zA-Z\säöüÄÖÜß/.-]|\.(?=(\s|$))', '', string)
    # |(?<=\s)\.
    # string = re.sub(r'\.(?=(\s|$))', '', string)
    # if string.endswith('.'):
    #     string = string[:-1]
    #     print('\ncut end stop\n')
    # string = re.sub(r'\.(?=\s)|(?<=\s)\.', '', string)
    # string = re.sub(r'(?<=\s)\.', '', string)
    # string = re.sub(r'\.(?=\s)', '', string)
    # string = re.sub(r'(?<=\S)\.(?=\s)', ' ', string)
    # string = re.sub(r'[^a-zA-Z\säöüÄÖÜß/-]|(?<=\S)\.(?=\s|$|\b)', ' ', string)
    # string = re.sub(
    #     r'(?i)(?<![a-zäöüß])[^a-z\säöüÄÖÜß/-]|\.(?=[\s\n])', '', string)
    # string = re.sub(r'(?<![a-zA-ZäöüÄÖÜß])\.(?=[\s\n])', '', string)
    # string = re.sub(
    #     r'(?<=[a-zA-ZäöüÄÖÜß])[^a-zA-Z\säöüÄÖÜß/](?=[a-zA-ZäöüÄÖÜß])', '', string)
    # string = re.sub(
    #     r'(?<=[a-zA-ZäöüÄÖÜß])[^a-zA-Z\säöüÄÖÜß/.](?=[a-zA-ZäöüÄÖÜß])|[^a-zA-Z\säöüÄÖÜß/.]+', '', string)

    # current "best" option, remaining full stops:
    # string = re.sub(r'[^a-zA-Z\säöüÄÖÜß/.-]', '', string)
    # string = re.sub(r'(?<=\S)\.(?=\S)', '', string)
    # string = string.replace('/', ' ')

    string = string.replace('--', '-')
    string = re.sub(r'[\n\t\xa0]+', ' ', string)
    # TODO: consider to allow stops (,) as well
    return string


def sort_competences(jdes, usual_words, competences, complex_competences, new_words, new_competences):
    """Two processes:
        1. sort known competences into a list to describe the job
        2. if word not known, ask if it is a competence or not, add it to list
        'usual_words' or 'competences' and, in latter case, add to list to
        describe the job.
    Input:
        jdes:           tuple of words in Job description
        usual_words:    tuple of usual used words
        competences:    tuple of known competences
        complex_competences: complex competence names
    Output:
        ad_competences: set of requested competences for that job/ad
        new_words, new_competences
        """
    # TODO: This function could run with a .. decorator(?) to ensure that the progress is
    # saved, even if it is interrupted.
    # TODO: allow '/'? What about 'vue.js' turning into 'vuejs'? Java/Kotlin
    # should be treated separate, while CI/CD shouldn't.
    # TODO: reduce words to stem
    ad_competences = set()
    print("jdes: ", jdes)
    for word in jdes:
        # print("word: ", word)
        # and len(word) > 1:
        # 'new_words' are not treated with lowercase, while usual_words are,
        # since we want to save them also with cap. letters in 'usual_words'.
        # workaround would be to save in two lists.
        if (word.lower() not in usual_words) and (word not in new_words):
            if word in competences or word in new_competences:
                # add to ad_competences set
                ad_competences.add(word)
                # print(f"'{word}' added to ad_competences.")

            else:
                # ask to either add to job competences
                # or to usual words.
                sortbool = False
                while not sortbool:
                    answer = input(f"is '{word}' a competence? [y/n]: ")
                    if answer == "y":
                        new_competences.add(word)
                        ad_competences.add(word)
                        print(f"'{word}' added to new_competences.")
                        print(f"'{word}' added to ad_competences.")
                        sortbool = True
                    elif answer == "n":
                        new_words.add(word)
                        print(f"'{word}' added to new_words.")
                        sortbool = True
                    else:
                        print("Please choose 'y' or 'n'.")
        else:
            pass
            # print(f"'{word}' in usual_words! (or new_words)")

    # current solution for double words
    matching_complex = {s for s in complex_competences if s in ' '.join(jdes)}
    ad_competences.update(matching_complex)

    # for comp in complex_competences:

    return ad_competences, new_words, new_competences


def append_to_file(filename, content):
    """function to append content to file"""
    with open(filename, "a", newline='') as g:
        # quoting=csv.QUOTE_NONE, escapechar=' '
        writer = csv.writer(g, dialect='excel')
        writer.writerows(content)
