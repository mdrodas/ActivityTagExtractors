"""
Implementation for tagFinder extractor using the service api/search using full activity name.
"""
# http://tagfinder.herokuapp.com/api/search?query=eating%20out&format=json_pretty&lang=en
import requests
import json

word = 'eating_out'
word2 = 'running'
keys = ['leisure', 'amenity', 'tourism', 'sport', 'shop']


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
    with open('../resources/' + filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


activities = readFile('activities01.csv')
print('Starting list...')
for activity in activities:
    activity_words = activity.replace(' ', '_')
    print(activity_words);
    similarities = readTagFinder(activity)
    print(similarities)
