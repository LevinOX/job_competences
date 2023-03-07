"""
Fills words from text document into unique set and saves in csv-file.
"""

# open file
import re
# with open(....) as myfile:
#   string = readlines()
input("warning: if you continue, you overwrite the manual sorting progress")
f = open("random_text_de.txt", "r", encoding='utf-8')
text = f.read()
f.close()


def filter_string(string):
    string = re.sub(r'[^a-zA-Z\säöüÄÖÜß-]', '', string)
    string = string.replace('--', '-')
    string = re.sub(r'[\n\t\xa0]+', ' ', string)
    string = string.lower()
    return string


# preparing string and store in list
text = filter_string(text)
usual_words = sorted(list(set(text.split(sep=' '))))

for i, word in enumerate(usual_words):
    if word.startswith('-'):
        usual_words[i] = word[1:]
usual_words = sorted(usual_words)

print(len(usual_words))
joinstring = ','.join(usual_words)

f2 = open("usual_words_de.csv", "w", encoding='utf-8')
f2.write(joinstring)
f2.close()
