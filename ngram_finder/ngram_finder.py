import csv
import nltk

class NGramFinder:
    def __init__(self):
        nltk.download('stopwords')

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
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        # print(text)
        tokens = text.split(' ')
        # print(tokens)
        # TODO better filter for everything else than words
        filtered_tokens = [word for word in tokens if not word in ['', ' ', '.', ',', ':', ';', '!', '?']]
        filtered_tokens = [word for word in filtered_tokens if not word in exclude_words]
        filtered_tokens = [word for word in filtered_tokens if not word in nltk.corpus.stopwords.words('german')]
        return set(nltk.ngrams(filtered_tokens, n))

    """
    Returns a list of all indices for the position of a sublist in a list.
    """
    def indices_of_sublist(self, lst, sublst):
        indices = list()
        for index in range(len(lst) - len(sublst) + 1):
            if lst[index:index+len(sublst)] == sublst:
                indices.append(index)
        return indices

    """
    Finds the context for an ngram.
    Assumes the ngram to be a tuple with strings in lowercase.
    word_count_before and word_count_after can be set to limit the number of words before and after the ngram.
    Default behaviour or a high value like infinity indicate that all words should be included.
    """
    def get_contexts_for_ngram(self, texts, ngram, word_count_before=float('inf'), word_count_after=float('inf')):
        contexts = list()
        for text in texts:
            text_lower = text.lower()
            words = text.split(' ')
            words_lower = text_lower.split(' ')

            # we need all indices in case that two occurences of the ngram are in the same text
            # and we need lowercase text for list equality
            indices = self.indices_of_sublist(words_lower, list(ngram))
            for index in indices:
                startIndex = max(0, index - word_count_before)
                endIndex = min(len(words), index + len(ngram) + word_count_after)
                context = ' '.join(words[startIndex:endIndex])
                contexts.append(context)

        return contexts
