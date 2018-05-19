import operator
from util.FileManager import FileManager
from model.Activity import Activity
from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
from nltk.corpus import wordnet as wn


def activities_frequency():
    activityDao = ActivityDao()
    tagDao = TagDao()
    all_activities = activityDao.getAll()
    freq = dict()
    print(len(all_activities))

    for activity in all_activities:
        # similarities = list()
        # print("Activity: " + activity.name)
        for tag_id1 in activity.tags:
            tag = tagDao.getById(tag_id1)
            tagLabel = tag[0].label.replace(' ', '_')
            # print("Tag: " + tagLabel)
            if (tagLabel not in freq):
                freq[tagLabel] = 1
            else:
                freq[tagLabel] += 1

    print("similarities: " + str(freq))
    freq_sorted = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    similarities = freq_sorted
    print("--", len(similarities), "--", similarities)
    flag = 0
    summary1 = dict()
    for key, value in similarities:
        if (flag == 0):
            value1 = value
            c = 1
            flag = 1
        else:
            if (value1 == value):
                c += 1
            else:
                summary1[value1] = c
                value1 = value
                c = 1
    summary1[value1] = c
    for key1, value1 in summary1.items():
        print("Frequency of Use: " + str(key1) + " - Amount of Tags: " + str(value1))


if __name__ == "__main__":
    activities_frequency()
