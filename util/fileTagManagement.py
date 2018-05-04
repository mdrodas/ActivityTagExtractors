"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import operator
import os


def readFile(filename):
    response = []
    with open('../resources/tagsOnly/' + filename) as fp:
        for line in fp:
            response.append(line.lower().strip('\n'))
    return response

def writeFile(infilename, outfilename):
    fp = open('../resources/' + outfilename, "a+")
    myFile = readFile(infilename)
    toWrite = '\n'.join(myFile[1:]) + "\n"
    fp.write(toWrite)
    fp.close()

for root, dirs, files in os.walk("../resources/tagsOnly/", topdown=False):
    activity_tags = dict()
    all_tags = dict()
    for fileName in files:
        writeFile(fileName, "allTags.txt")
