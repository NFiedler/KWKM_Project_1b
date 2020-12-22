import yaml
import csv
import re
from nltk.tokenize import RegexpTokenizer

class NameFilter:
    def __init__(self, interactive_add=True, prints=True):
        self.interactive_add = interactive_add
        self.prints = prints
        with open('names/namen.csv', 'r') as f:
            self.names = [line[0] for line in csv.reader(f)]
        with open('include.txt', 'r') as f:
            self.include = [line[0] for line in csv.reader(f)]
        with open('exclude.txt', 'r') as f:
            self.exclude = [line[0] for line in csv.reader(f)]
        self.tokenizer = RegexpTokenizer(r'\w+')

    def add_to_include(self, word):
        if word not in self.include and word != "":
            self.include.append(word)
            with open('include.txt', 'a') as f:
                f.write(word + '\n')

    def add_to_exclude(self, word):
        if word not in self.exclude and word != "":
            self.exclude.append(word)
            with open('exclude.txt', 'a') as f:
                f.write(word + '\n')

    def classify(self, text: str) -> float:
        rating = 0
        name_finds = []
        text = text.replace('\n', ' ')
        # replace umlaute
        text = text.replace("Ä", "Ae").replace("ä", "ae")
        text = text.replace("Ü", "Ue").replace("ü", "ue")
        text = text.replace("Ö", "Oe").replace("ö", "oe")
        text = text.replace("ẞ", "Ss").replace("ß", "ss")

        # Rule-based removal of street names
        text = re.sub(r"(([A-Z][a-z]+-)+|([A-Z][a-z]+ )){1,2}(Weg|Platz|Allee|Strasse|Park|Siedlung)", "", text)

        text = text.replace('-', ' ')

        words = self.tokenizer.tokenize(text)
        for i, word in enumerate(words):
            found = False
            if word in self.names:
                name_finds.append((i, word))
                found = True
                if self.prints:
                    print(f'found name \"{word}\"')
            if found:
                rating += 0.2
        for name_find in name_finds:
            for name_find_b in name_finds:
                if name_find[0] + 1 == name_find_b[0]:
                    if self.prints:
                        print(f'found name \"{name_find[1]}\" followed by name \"{name_find_b[1]}\"')
                    rating += 0.2
            if len(words) > name_find[0] + 1:
                if re.match('[A-Z]\.', words[name_find[0]+1]): # searching for Capital letter and dot (Jonas H.)
                    rating += 0.2
            if name_find[0] > 0:
                if re.match('[A-Z]\.', words[name_find[0]-1]): # searching for Capital letter and dot (J. Hagge)
                    rating += 0.2
        if self.interactive_add:
            candidates = [words[name_find[0]-1] for name_find in name_finds if name_find[0] > 0]
            candidates += [words[name_find[0]+1] for name_find in name_finds if len(words) > name_find[0] +1]
            candidates = [candidate for candidate in candidates if candidate not in self.names]
            candidates = [candidate for candidate in candidates if not re.match('[A-Z]\.', candidate) and candidate != ""]
            for candidate in candidates:
                if candidate not in self.include and candidate not in self.exclude:
                    result = yes_no(f'Is \"{candidate}\" a name?')
                    if result:
                        self.add_to_include(candidate)
                    else:
                        self.add_to_exclude(candidate)

        return rating

# Function for a Yes/No result based on the answer provided as an arguement
# Taken from https://overlaid.net/2016/02/09/simple-yes-no-function-in-python/
def yes_no(answer):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
     
    while True:
        choice = input(answer).lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print("Please respond with 'yes' or 'no'")

