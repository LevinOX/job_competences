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
import functions as fu


with open("job_description.txt", "r", encoding='utf-8') as f:
    jdescription = fu.filter_string(f.read(3000))
    jdes = tuple(filter(None, jdescription.split(sep=' ')))
with open("usual_words_de.csv", "r") as g:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
with open("competences.csv", "r") as h:
    competences = sum(list(csv.reader(h, delimiter=',')), [])

print(f"list of competences: \n{competences}")
print(f"job description: {jdescription}")
print(usual_words[:20])

# job_data-structure: [['URL', 'job_title', {'comp1', 'comp2', 'comp3'}],
#                       ['URL2', 'job_title2', {'comp1', 'comp2', 'comp3'}],
#                       ['URL3', ..., {...}]] and so forth.
job_data = [[None, None, set()]
            for i in range(jdes.count('http'))]  # count number of URLs in 'jdes'


job_data, new_words, new_competences = fu.sort_competences(
    jdes, usual_words, competences, job_data)

print("job_data: ", job_data)
print("new_competences: ", new_competences)
print("new_words: ", new_words)

fu.append_to_file("usual_words_de.csv", new_words)
fu.append_to_file("competences.csv", new_competences)
fu.append_to_file("job_data.csv", job_data)
# with open("competences.csv", "a", encoding='utf-8') as h:
#     writer = csv.writer(h)
#     writer.writerow(new_competences)

# with open("job_data.csv", "a", encoding='utf-8') as i:
#     writer = csv.writer(i)
#     writer.writerow(job_data)
