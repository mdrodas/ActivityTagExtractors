"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import operator
import os

useless_words = ['its', 'an', 'of', 'in', 'the', 'and', 'on', 'for', 'with', 'to']


def readFile(filename):
    response = []
    with open('resources/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


def writeFile(value, outfilename):
    fp = open('resources/' + outfilename, "a+")
    fp.write(value + "\n")
    fp.close()


def clean_wordList(a, b):
    return list(set(a) - set(b))


activity_tags = dict()
all_tags = dict()
allTagsName = "allTags.txt"
cleanAllTagsName = "allTagsClean.txt"
tagsFrequencyName = "tagsFrequency.txt"
myFile = readFile(allTagsName)
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
        if (len(activity_words) > i):
            word = activity_words[i].lower().strip()
            freq[word] = 1;
    # similarities.add(word4);
    # print(freq,"--")
    if (activity not in activity_tags):
        activity_tags[activity] = freq
    else:
        freq2 = activity_tags[activity]
        for i in range(3, 6):
            if (len(activity_words) > i):
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
    # toPrint = str(key) + "-" + str(len(freq_sorted)) + "== " + str(freq_sorted)
    # print(toPrint)

    outLine = [str(key)]
    for value2 in freq_sorted:
        outLine.append(value2[0])

    toPrint2 = "\t".join(outLine)
    # print(toPrint2)
    writeFile(toPrint2, cleanAllTagsName)

average1 = "Average tags per activity:"+ str(size / i)
#print(average1)
writeFile(average1, cleanAllTagsName)

freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
uniqueTagsLen = "Amount of unique tags:"+ str(len(freq_sorted2))
# print(uniqueTagsLen)
writeFile(uniqueTagsLen, cleanAllTagsName)

print("Results 02: Tag == frequency_used")
for key, value in freq_sorted2:
    keyValue=key+ "=="+ str(value)
    #print(keyValue)
    writeFile(keyValue,tagsFrequencyName)
