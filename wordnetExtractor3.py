import operator
from nltk.corpus import wordnet as wn

useless_words = ['a','an','of','in','the','and','on','for','with','to']

def readFile(filename):
    response = []
    with open('resources/'+filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response

def clean_wordList(a,b):
    return list(set(a)-set(b))

activities = readFile('activities01.csv')
# print(activities)
size = 5
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
    freq = dict()
    for word in activity_words:
        for my_syn in wn.synsets(word):
            my_syn2 = my_syn.lemmas(lang='eng')
            for syn in my_syn2:
                if (syn.count()> 0):
                    cadena = syn.name()
                    #print(cadena,'+',str(syn.count()))
                    if (cadena not in freq or freq[cadena] < syn.count()):
                        freq[cadena] = syn.count()

                    similarities.add(cadena)

    freq_sorted = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    similarities = freq_sorted[0:size]
    print("--",len(similarities),"--",similarities)