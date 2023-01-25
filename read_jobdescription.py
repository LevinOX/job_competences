"""
This code is expected to read textfiles of job descriptions and search for 
requested competences. The textfiles are expected to be structured with:
first line: URL
second line: job title
third line: job description

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
import functions2 as fu
import csv


with open("job_descriptions.txt", "r", encoding='utf-8') as f:
    jdescriptions = f.readlines()
    # .split(sep='\n')  # should result in lines tuple/list
    jdess = jdescriptions
with open("usual_words_de.csv", "r") as g:
    usual_words = sum(list(csv.reader(g, delimiter=',')), [])
    usual_words = [word.lower() for word in usual_words]
with open("competences.csv", "r") as h:
    competences = sum(list(csv.reader(h, delimiter=',')), [])


# define empty list of three lists for entries "job title, URL, competences"
# job_data-structure: [['URL', 'job_title', ['comp1', 'comp2', 'comp3']],
#                       ['URL2', 'job_title2', ['comp1', 'comp2', 'comp3']],
#                       ['URL3', ..., [...]]] and so forth.
ad_counts = 0
for line in jdess:
    if 'http' in line:
        ad_counts += 1
print("ad_counts: ", ad_counts)
job_data = [[None, None, set()]
            for i in range(ad_counts)]
print("job_data: ", job_data)
# TODO: Add company name in job_data
new_words = []
new_competences = []

ad_counter = -1
ad_start = False
for line in jdess:
    # print("line: ", line)
    if line.startswith('http'):
        ad_counter += 1
        job_data[ad_counter][0] = line
        ad_start = True
    elif ad_start:
        # the line after 'http' holds the job title
        job_data[ad_counter][1] = line
        ad_start = False
    else:
        # filter competences in job description
        text_input = fu.filter_string(line)
        word_list = tuple(filter(None, text_input.split(sep=' ')))
        # TODO: add replace of empty entries?
        print("word_list: ", word_list)
        ad_competences, new_words, new_competences = fu.sort_competences(
            word_list, usual_words, competences, new_words, new_competences)
        print("ad_competences:", ad_competences)
        job_data[ad_counter][2].update(ad_competences)

print("job_data: ", job_data)
print("new_competences: ", new_competences)
print("new_words: ", new_words)

fu.append_to_file("usual_words_de.csv", new_words)
fu.append_to_file("competences.csv", new_competences)
fu.append_to_file("job_data.csv", job_data)


"""
for line in text:
    if 'http' in string: continue*2 (jump to next line with job title)
    (and also jump over line with job title)
    
    list(string) and reduce to isalpha()-values (no other symbols): list(reduce(lambda str: isalpha(str),split(string)))
        for word in line:
            if word in usual: continue
            elif word in competences
            else append to weird_words    
"""


# if len(weird_words) > 0:
#   safe to weird_words.csv and quit.

"""
while not text_end:
    try to store URL in list (append)
    and store job title in list (append?)

    while URL not in string?
        read line/string
        (if 'http' in string: break)
        put string in list and reduce to isalpha()-values (no other symbols)
            for word in line:
                if word in usual: continue
                elif word in competences
                else append to weird_words    
"""
