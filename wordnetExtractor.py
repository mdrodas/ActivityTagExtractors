"""
Implementation for wordnet extractor using directly the synsets of wordnet and calculating the path_similarity.
"""
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
    with open('resources/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


def clean_wordList(a, b):
    return list(set(a) - set(b))


activities = readFile('activities01.csv')
# print(activities)
print('Starting list...')
for activity in activities:
    activity_words = activity.split(' ')
    activity_words = clean_wordList(activity_words, useless_words)
    print(activity, " = ", activity_words)

    similarities = set()
    for word in activity_words:
        for my_syn in syn(word):
            my_syn2 = my_syn[0].lemma_names(lang='eng')
            my_syn3 = my_syn[1].lemma_names(lang='eng')
            similarities.update([x.lower() for x in my_syn2])
            similarities.update([x.lower() for x in my_syn3])

    print("--", len(similarities), "--", similarities)
