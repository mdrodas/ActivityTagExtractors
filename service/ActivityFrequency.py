import operator
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
from util.KnowledgeBase import KnowledgeBase


class ActivityFrequency:

    def __init__(self):
        self.kb = KnowledgeBase()

    def activities_frequency(self):
        activityDao = ActivityDao(self.kb)
        tagDao = TagDao(self.kb)
        all_activities = activityDao.getAll()
        freq = dict()
        total = 3000

        for activity in all_activities:
            # print("Activity: " + activity.name)
            for tag_id1 in activity.tags:
                # total += len(activity.tags)
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
        sum = 0
        print("total: " + str(total))

        for key1, value1 in summary1.items():
            value2 = value1 / total * 100
            sum += value2
            print("Frequency of Use: " + str(key1) + " - Amount of Tags: " + str(value1) + " (" + str(value2) + "%)")
        print("check 100%: " + str(sum))


if __name__ == "__main__":
    app = ActivityFrequency()
    app.activities_frequency()
