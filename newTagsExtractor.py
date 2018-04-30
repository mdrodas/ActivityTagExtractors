"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import operator
import os

useless_words = ['its', 'an', 'of', 'in', 'the', 'and', 'on', 'for', 'with', 'to']


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
    all_tags = dict()
    for fileName in files:
        myFile = readFile(fileName)
        # print('File: ' + fileName)
        for line in myFile:

            activity_words = line.split('\t')
            # print(activity_words[0], "--")
            # similarities = set()
            freq = dict()
            activity = activity_words[0].lower()
            if (activity == '_id'):
                continue
            for i in range(3, 6):
                word = activity_words[i].lower().strip()
                freq[word] = 1;
            # similarities.add(word4);
            # print(freq,"--")
            if (activity not in activity_tags):
                activity_tags[activity] = freq
            else:
                freq2 = activity_tags[activity]
                for i in range(3, 6):
                    word = activity_words[i].lower().strip()
                    if (word in freq2):
                        freq2[word] = freq2[word] + 1
                    else:
                        freq2[word] = 1

                    if (word in all_tags):
                        all_tags[word] = all_tags[word] + 1
                    else:
                        all_tags[word] = 1
                activity_tags[activity] = freq2

    print("Results 01: Activities - Amount_Tags == Tags_List")
    i = 0
    size = 0
    for key, value in activity_tags.items():
        freq_sorted = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        i = i + 1
        size = size + len(freq_sorted)
        print(key, "-", len(freq_sorted), "== ", freq_sorted)

    print("Average tags per activity:", size / i)

    freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
    print("Amount of unique tags:", len(freq_sorted2))
    print("Results 02: Tag == frequency_used")
    for key, value in freq_sorted2:
        print(key, "==", value)
