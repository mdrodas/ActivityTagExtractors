"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import operator
import os

# useless_words = ['a', 'an', 'of', 'in', 'the', 'and', 'on', 'for', 'with', 'to']


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
    with open('resources/tagsOnly/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


def clean_wordList(a, b):
    return list(set(a) - set(b))


for root, dirs, files in os.walk("resources/tagsOnly/", topdown=False):
    activity_tags = dict()
    for fileName in files:
        myFile = readFile(fileName)
        print('File: '+fileName)
        for line in myFile:

            activity_words = line.split('\t')
            #print(activity_words[0], "--")
            # similarities = set()
            freq = dict()
            activity = activity_words[0].lower()
            if (activity == '_id'):
                continue
            for i in range (3,6):
                word = activity_words[i].lower().strip()
                freq[word]= 1;
            # similarities.add(word4);
            #print(freq,"--")
            if (activity not in activity_tags):
                activity_tags[activity]=freq
            else:
                freq2 = activity_tags[activity]
                for i in range(3, 6):
                    word = activity_words[i].lower().strip()
                    if (word in freq2):
                        freq2[word] = freq2[word] + 1
                    else:
                        freq2[word] = 1
                activity_tags[activity] = freq2

    print("Results: ")
    for key, value in activity_tags.items():
        freq_sorted = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        print (key,"==",freq_sorted)

    # freq_sorted = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    # similarities = freq_sorted[0:size]
    # print("--", len(similarities), "--", similarities)
