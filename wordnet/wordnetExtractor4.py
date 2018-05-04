"""
Implementation for wordnet extractor using directly the synsets of wordnet and calculating the path_similarity and the frequency number to order and limiting the amount of tags.
"""
import operator
from nltk.corpus import wordnet as wn

useless_words = ['a', 'an', 'of', 'in', 'the', 'and', 'on', 'for', 'with', 'to']


def syn(word, lch_threshold=0.8):
    for net1 in wn.synsets(word):
        for net2 in wn.all_synsets():
            try:
                lch = net1.path_similarity(net2)
            except:
                continue
            # The value to compare the LCH to was found empirically.
            if lch is not None and lch >= lch_threshold:
                yield (net1, net2, lch)


def readFile(filename):
    response = []
    with open('../resources/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


def clean_wordList(a, b):
    return list(set(a) - set(b))


activities = readFile('activities03.csv')
# print(activities)
size = 5
print('Starting list...')
for activity in activities:
    activity_words = activity.split(' ')
    activity_words = clean_wordList(activity_words, useless_words)
    print(activity, " = ", activity_words)
    freq = dict()
    similarities = set()
    for word in activity_words:
        for my_syn in syn(word):
            my_syn2 = my_syn[0].lemmas(lang='eng')
            my_syn3 = my_syn[1].lemmas(lang='eng')
            for x in my_syn2:
                name = x.name().lower()
                if (name not in freq or freq[name] < x.count()):
                    freq[name] = x.count()
                similarities.add(name)

            for y in my_syn3:
                name = y.name().lower()
                if (name not in freq or freq[name] < y.count()):
                    freq[name] = y.count()
                similarities.add(name)

    freq_sorted = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    similarities = freq_sorted[0:size]
    print("--", len(similarities), "--", similarities)
