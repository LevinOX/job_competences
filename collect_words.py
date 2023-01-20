"""
Fills words from text document into unique set, safed in csv-file.
"""
# declare set for usual words
# usual_words = set()

# open file
import re
f = open("random_text_de.txt", "r", encoding='utf-8')
text = f.read()
f.close()
# print(text)
# text = ''.join(e for e in text if (e.isalpha() or e.isspace()) else ' ')
# text = ''.join(c.lower() if c.isalpha() or c.isspace()
#              else ' ' for c in text).replace("\n", "")


def filter_string(string):
    string = re.sub(r'[^a-zA-Z\säöüÄÖÜß-]', '', string)
    string = string.replace('--', '-')
    string = re.sub(r'[\n\t\xa0]+', ' ', string)
    string = string.lower()
    return string


# def correct_char(char):
#    return char.isalpha()

text = filter_string(text)
# print(text)
usual_words = sorted(list(set(text.split(sep=' '))))

for i, word in enumerate(usual_words):
    if word.startswith('-'):
        usual_words[i] = word[1:]

print(len(usual_words))
# print(usual_words)
joinstring = ','.join(usual_words)
# print(joinstring[34755:34765])
f2 = open("usual_words_de.csv", "w")
f2.write(joinstring)
f2.close()
