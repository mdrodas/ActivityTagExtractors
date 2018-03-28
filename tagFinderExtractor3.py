# http://tagfinder.herokuapp.com/api/search?query=eating%20out&format=json_pretty&lang=en
#http://tagfinder.herokuapp.com/api/terms?term=camping&format=json_pretty
import requests
import json

useless_words = ['a','an','of','in','the','and','on','for','with','to']
keys = ['leisure','amenity','tourism','sport','shop']

def clean_wordList(a,b):
    return list(set(a)-set(b))

def readTagFinder(word):
    response = requests.get('http://tagfinder.herokuapp.com/api/terms?term=' + word + '&format=json_pretty')
    assert response.status_code == 200

    similarities = set()
    data = response.json()
    termBroader = data['termBroader']['en']
    if (len(termBroader)>0):
        similarities.update(termBroader)
    termNarrower = data['termNarrower']['en']
    if (len(termNarrower) > 0):
        similarities.update(termNarrower)
    termRelated = data['termRelated']['en']
    if (len(termRelated) > 0):
        similarities.update(termRelated)
    return similarities


def readFile(filename):
    response = []
    with open('resources/'+filename) as fp:
        for line in fp:
            response.append(line.strip('\n'))
    return response


activities = readFile('activities03.csv')
print ('Starting list...')
for activity in activities:
    #activity_words = activity.replace(' ','_')
    activity_words = activity.split(' ')
    activity_words = clean_wordList(activity_words, useless_words)
    print(activity, " = ", activity_words)
    similarities = set()
    for word in activity_words:
        similarities.update(readTagFinder(word))
    print ('--',len(similarities),'--',similarities)