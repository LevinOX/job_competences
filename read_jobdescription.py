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

# load files: job_competences, usual_words, job_descriptions
f = open("job_descriptions.txt", "r")
# file = f.read()
# print(file)

# define empty list of three lists for entries "job title, URL, competences"
data = [[, , ]]
while not end of file:
    line = f.readline()
    if line.startswith('http'):
        data.append([[, , ]])
        data[-1][0] = str(line)
        data[-1][1] = str(f.readline())
    else:
        # step through job description and identify not usual words, i.e.
        # job competences.
        data[1][0] = str(line)

    if f.readline() == end of line:
        break


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
