import yaml
import csv
import re
from nltk.tokenize import RegexpTokenizer
import spacy

class NameFilter:
    def __init__(self,
                 interactive_add=True,
                 interactive_adapt=True,
                 prints=True,
                 name_follow_name_rating=0.2,
                 name_follow_short_rating=0.2,
                 short_follow_name_rating=0.2,
                 learning_rate=0.2,
                 name_min_rating=0,
                 name_max_rating=2
                 ):
        self.interactive_add = interactive_add
        self.interactive_adapt = interactive_adapt
        self.prints = prints
        self.name_follow_name_rating = name_follow_name_rating
        self.name_follow_short_rating = name_follow_short_rating
        self.short_follow_name_rating = short_follow_name_rating
        self.name_min_rating = name_min_rating
        self.name_max_rating = name_max_rating
        self.learning_rate=learning_rate
        self.name_file = 'names/namen.csv'
        with open(self.name_file, 'r') as f:
            self.names = {line[0]: float(line[1]) for line in csv.reader(f)}
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
        # named entity recognition
        # this is commented out, because it did not work well
        # named_entity_recognition(text)


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
            if word in self.names.keys():
                name_finds.append((i, word, self.names[word]))
                found = True
                if self.prints or self.interactive_adapt:
                    print(f'found name \"{word}\"')
                if self.interactive_adapt:
                    formatted_text = text.replace(word, '\033[91m'+word+'\033[0m')
                    if yes_no('is the name find correct in the following context? \n' + formatted_text + '\n'):
                        self.change_name_rating(word, self.learning_rate)
                    else:
                        self.change_name_rating(word, -self.learning_rate)
            if found:
                rating += self.names[word]
        for name_find in name_finds:
            for name_find_b in name_finds:
                if name_find[0] + 1 == name_find_b[0]:
                    if self.prints:
                        print(f'found name \"{name_find[1]}\" followed by name \"{name_find_b[1]}\"')
                    rating += self.name_follow_name_rating
            if len(words) > name_find[0] + 1:
                if re.match('[A-Z]\.', words[name_find[0]+1]): # searching for Capital letter and dot (Jonas H.)
                    rating += self.short_follow_name_rating
            if name_find[0] > 0:
                if re.match('[A-Z]\.', words[name_find[0]-1]): # searching for Capital letter and dot (J. Hagge)
                    rating += self.name_follow_short_rating
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

    def change_name_rating(self, name, rating_change):
        with open(self.name_file, 'r') as f:
            text = ''.join([i for i in f]).replace(f'{name}, {self.names[name]}',
                                                   f'{name}, {min(self.name_max_rating, max(self.name_min_rating, self.names[name] + rating_change))}')
        with open(self.name_file, 'w') as f:
            f.writelines(text)


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

# We looked into Named Entity Recognition with spacy and used the dataset trained on wikipedia.
# However this led to a lot of false positives, so it seems like this is not a good approach for us.
# Especially because it is hard to parameterize
def named_entity_recognition(sentence):
    # https://spacy.io/api/annotation#ner-wikipedia-scheme
    # We use the wikipedia scheme, above is the documentation for it.
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(sentence)
    for ent in doc.ents:
        if ent.label_ == "PER":
            print(ent.text, ent.label_)