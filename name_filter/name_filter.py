import yaml
import csv
import re

class NameFilter:
    def __init__(self, interactive=True, prints=True):
        self.interactive = interactive
        self.prints = prints
        with open('names/vornamen.txt', 'r') as f:
            self.first_names = [line[0] for line in csv.reader(f)]
        with open('names/nachnamen.txt', 'r') as f:
            self.surnames = [line[0] for line in csv.reader(f)]
        with open('include.txt', 'r') as f:
            self.include = [line[0] for line in csv.reader(f)]
        with open('exclude.txt', 'r') as f:
            self.exclude = [line[0] for line in csv.reader(f)]

    def add_to_include(self, word):
        if word not in self.include:
            self.include.append(word)
            with open('include.txt', 'a') as f:
                f.write(word + '\n')

    def add_to_exclude(self, word):
        if word not in self.exclude:
            self.exclude.append(word)
            with open('exclude.txt', 'a') as f:
                f.write(word + '\n')

    def classify(self, text: str) -> float:
        rating = 0
        first_name_finds = []
        surname_finds = []
        text = text.replace('\n', ' ')
        text = text.replace('-', ' ')
        # replace umlaute
        text = text.replace("Ä", "Ae").replace("ä", "ae")
        text = text.replace("Ü", "Ue").replace("ü", "ue")
        text = text.replace("Ö", "Oe").replace("ö", "oe")
        text = text.replace("ẞ", "Ss").replace("ß", "ss")

        words = text.split(' ')
        for i, word in enumerate(words):
            found = False
            if word in self.first_names:
                first_name_finds.append((i, word))
                found = True
                if self.prints:
                    print(f'found first name \"{word}\"')
            if word in self.surnames:
                surname_finds.append((i, word))
                found = True
                if self.prints:
                    print(f'found surname \"{word}\"')
            if found:
                rating += 0.2
        for first_name_find in first_name_finds:
            for first_name_find_b in first_name_finds:
                if first_name_find[0] + 1 == first_name_find_b[0]:
                    if self.prints:
                        print(f'found first name \"{first_name_find[1]}\" followed by first name \"{first_name_find_b[1]}\"')
                    rating += 0.2
            for surname_find in surname_finds:
                if first_name_find[0] + 1 == surname_find[0]:
                    if self.prints:
                        print(f'found first name \"{first_name_find[1]}\" followed by surname \"{first_name_find_b[1]}\"')
                    rating += 0.2
            if len(words) > first_name_find[0] + 1:
                if re.match('[A-Z]\.', words[first_name_find[0]+1]): # searching for Capital letter and dot (Jonas H.)
                    rating += 0.2
        for surname_find in surname_finds:

            if surname_find[0] > 0:
                if re.match('[A-Z]\.', words[surname_find[0]-1]): # searching for Capital letter and dot (J. Hagge)
                    rating += 0.2
        if self.interactive:
            name_finds = surname_finds + first_name_finds
            candidates = [words[name_find[0]-1] for name_find in name_finds if name_find[0] > 0]
            candidates += [words[name_find[0]+1] for name_find in name_finds if len(words) > name_find[0] +1]
            candidates = [candidate for candidate in candidates if candidate not in self.include and candidate not in self.exclude and candidate not in self.surnames and candidate not in self.first_names]
            candidates = [candidate for candidate in candidates if not re.match('[A-Z]\.', candidate)]
            for candidate in candidates: 
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

