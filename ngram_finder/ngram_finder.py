import csv
import nltk

class NGramFinder:
    def __init__(self):
        pass

    def get_n_m_gram_count(self, texts, n, m, exclude_words=list()):
        counts = dict()
        for i in range(n, m+1):
            counts[i] = self.get_ngram_count(texts, i, exclude_words)
        return counts
            

    def get_ngram_count(self, texts, n, exclude_words):
        ngram_counts = dict()
        
        for text in texts:
            ngrams = self.get_ngrams_of_text(text, n, exclude_words)
            for ngram in ngrams:
                if ngram in ngram_counts:
                    ngram_counts[ngram] += 1
                else:
                    ngram_counts[ngram] = 1
        return ngram_counts

    def get_ngrams_of_text(self, text, n, exclude_words):
        # TODO: remove shit
        text = text.lower()
        # print(text)
        tokens = text.split(' ')
        # print(tokens)
        filtered_tokens = [word for word in tokens if not word in exclude_words]
        filtered_tokens = [word for word in filtered_tokens if not word in nltk.corpus.stopwords.words('german')]
        return set(nltk.ngrams(filtered_tokens, n))

ngf = NGramFinder()

with open('../data/2020-11-20 Stadteingang Elbbruecken_Kommentare.csv', 'r') as f:
    eb = list(csv.reader(f, delimiter=';'))
    eb_t = [text[3] for text in eb]
    count = ngf.get_ngram_count(eb_t, 2, [])
    print(max(count.values()))
    for text, count in count.items():
        if count >= 5:

            print(text)
