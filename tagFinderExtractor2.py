"""
Implementation for tagFinder extractor using the service api/search using chopped activity name.
"""
# http://tagfinder.herokuapp.com/api/search?query=eating%20out&format=json_pretty&lang=en
# http://tagfinder.herokuapp.com/api/terms?term=camping&format=json_pretty
import requests
import json

useless_words = ['a', 'an', 'of', 'in', 'the', 'and', 'on', 'for', 'with', 'to']
keys = ['leisure', 'amenity', 'tourism', 'sport', 'shop']


def clean_wordList(a, b):
    return list(set(a) - set(b))


def readTagFinder(word):
    response = requests.get('http://tagfinder.herokuapp.com/api/search?query=' + word + '&format=json_pretty&lang=en')
    assert response.status_code == 200

    similarities = set()
    for data in response.json():
        # print(data['combines'])
        for data2 in data['combines']:
            values = data2['label'].split('=')
            if (values[0] in keys and values[1] != '*'):
                # print (values[0],'=',values[1])
                similarities.add(values[1])

        # print ('------')
        for data3 in data['links']:
            values = data3['label'].split('=')
            if (values[0] in keys and values[1] != '*'):
                # print (values[0],'=',values[1])
                similarities.add(values[1])
        # print ('#####')
    return similarities


def readFile(filename):
    response = []
    with open('resources/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


activities = readFile('activities03.csv')
print('Starting list...')
for activity in activities:
    # activity_words = activity.replace(' ','_')
    activity_words = activity.split(' ')
    activity_words = clean_wordList(activity_words, useless_words)
    print(activity, " = ", activity_words)
    similarities = set()
    for word in activity_words:
        similarities.update(readTagFinder(word))
    print('--', len(similarities), '--', similarities)
