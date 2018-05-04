"""
Implementation for wordnet extractor using directly the synsets of semcor.
"""
from nltk.corpus import semcor as wn

useless_words = ['a','an','of','in','the','and','on','for','with','to']

def syn(word, lch_threshold=1.0):
    net1 = wn.synsets(word)
    yield(net1)

def readFile(filename):
    response = []
    with open('../resources/'+filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response

def clean_wordList(a,b):
    return list(set(a)-set(b))

activities = readFile('activities01.csv')
# print(activities)
print ('Starting list...')
for activity in activities:
    activity_words = activity.split(' ')
    activity_words = clean_wordList(activity_words,useless_words)
    # for useless_word in useless_words:
    #     try:
    #         activity_words.remove(useless_word)
    #     except ValueError:
    #         pass

    print (activity," = ",activity_words)
    similarities = set()
    for word in activity_words:
        for my_syn in syn(word):
            if (len(my_syn)>0):
                similarities.update(my_syn[0].lemma_names())

    print("--",len(similarities),"--",similarities)