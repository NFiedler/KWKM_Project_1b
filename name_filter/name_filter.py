import yaml
import csv
import re

class NameFilter:
    def __init__(self):
        self.prints = True
        with open('names/vornamen.txt', 'r') as f:
            self.first_names = [line[0] for line in csv.reader(f)]
        with open('names/nachnamen.txt', 'r') as f:
            self.surnames = [line[0] for line in csv.reader(f)]

    def classify(self, text: str) -> float:
        rating = 0
        first_name_finds = []
        surname_finds = []
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
                print('a')
                if re.match('[A-Z]\.', words[first_name_find[0]+1]): # searching for Capital letter and dot (Jonas H.)
                    rating += 0.2
        for surname_find in surname_finds:

            if surname_find[0] > 0:
                if re.match('[A-Z]\.', words[surname_find[0]-1]): # searching for Capital letter and dot (J. Hagge)
                    rating += 0.2
        return rating



