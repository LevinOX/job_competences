"""
This code is expected to read textfiles of job descriptions and search for 
listed competences. The textfiles are expected to be structured with:
first line: URL
second line: job title
followed by lines with job description until next URL

Input files
job_competences.csv        register of unique job competences
usual words.csv
{job_descriptions}.txt      hm. containing several/all job descriptions?

Output
jobs_table   .csv   # comprises all job_titles, URLs and requested
                    competences
weird_words .csv    # to be checked and sorted

The script will sort the words accordingly and gather the information to fill
the jobs_table - which can be used to fill a database, showing which 
competences are requested for which positions.
"""
import csv
import datetime
# if you need paths, try pathlib.
# TODO: remove stop words and use nltk
# TODO: detect if english

import functions2 as fu

with open("job_descriptions_arbeitsagentur_api.txt", "r", encoding='utf-8') as f:
    jdescriptions = f.read().split(sep='\n')
    jdess = jdescriptions
with open("usual_words_de.csv", "r") as g:
    # the reader creates a list of lists, the sum makes a list of
    # entries/lines:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
    usual_words = [word.lower() for word in usual_words]
with open("competences.csv", "r") as h:
    competences = sum(list(csv.reader(h, delimiter=',')), [])
with open("complex_competences.csv", "r") as h:
    complex_competences = set(sum(list(csv.reader(h, delimiter=',')), []))

# define empty list of three lists for entries "job title, URL, competences"
# job_data-structure: [['URL', 'job_title', ['comp1', 'comp2', 'comp3']],
#                       ['URL2', 'job_title2', ['comp1', 'comp2', 'comp3']],
#                       ['URL3', ..., [...]]] and so forth.
ad_counts = 0
for line in jdess:
    if line.startswith('http'):
        ad_counts += 1
#            URL, jobtitle,company, refnr, date, place, todays_date, req. comp.
job_data = [[None, None,   None,    None,  None, None, str(datetime.date.today()), set()]
            for i in range(ad_counts)]

new_words = set()
# same like new_words just capital letters allowed.
new_competences = set()

ad_counter = -1
ad_start = 0

# https://www.smallcases.de/
# 10000-1193410325-S
# 2023-03-01
# Softwareentwickler (m/w/d) Python, Softwareentwickler/in 
# SmallCases GmbH Softwareberatung
# {'land': 'Deutschland', 'region': 'Baden-Württemberg', 'plz': '79106', 'ort': 'Freiburg im Breisgau', 'strasse': 'Wentzingerstr. 23'}
# Wir, die Smallcases

for line in jdess:
    if line.startswith('http'):
        # store URL
        ad_counter += 1
        job_data[ad_counter][0] = line
        ad_start += 1
    elif ad_start == 1:
        # the line after 'http' holds the job ad ref nr
        job_data[ad_counter][3] = line
        ad_start += 1
    elif ad_start == 2:
        # the line after 'http' holds the date
        job_data[ad_counter][4] = line
        ad_start += 1
    elif ad_start == 3:
        # the line after 'http' holds the job title
        job_data[ad_counter][1] = line
        ad_start += 1
    elif ad_start == 4:
        # name of company
        job_data[ad_counter][2] = line
        ad_start += 1
    elif ad_start == 5:
        # name of place
        job_data[ad_counter][5] = line
        ad_start = 0
    else:
        print("jdes line: ", line)
        # filter competences in job description
        text_input = fu.filter_string(line)
        word_list = tuple(filter(None, text_input.split(sep=' ')))
        ad_competences, newest_words, newest_competences = fu.sort_competences(
            word_list, usual_words, competences, complex_competences, new_words, new_competences)
        new_words.update(newest_words)
        new_competences.update(newest_competences)
        job_data[ad_counter][7].update(ad_competences)
        print("ad_competences:", ad_competences)
        print("newest_words: ", newest_words)

    # TODO: backup: if len new_words or new_competences > X: save to file.

print("job_data: ", job_data)
print("new_competences: ", new_competences)
print("new_words: ", new_words)


with open("usual_words_de.csv", "a", encoding='utf-8') as g:
    # TODO: use utf8?
    writer = csv.writer(g)
    writer.writerow(new_words)

with open("competences.csv", "a", encoding='utf-8') as g:
    # TODO: use utf8?
    writer = csv.writer(g)
    writer.writerow(new_competences)

with open("job_data.csv", "a", newline='', encoding='utf-8') as g:
    # TODO: use utf8
    writer = csv.writer(g, dialect='excel')
    writer.writerows(job_data)
