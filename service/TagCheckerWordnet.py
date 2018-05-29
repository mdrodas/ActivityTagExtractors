from nltk.corpus import wordnet as wn
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao


def check_synonyms_wordnet(activity, word2, threshold=0.0):
    activityDao = ActivityDao()
    word1 = activity.name
    syns1 = wn.synsets(word1)
    syns2 = wn.synsets(word2)
    if not syns1 or not syns2:
        return

    syn1 = syns1[0].lemmas()[0].name()
    syn2 = syns2[0].lemmas()[0].name()
    # for syn1 in syns1:  # different meanings of the tag
    #    for syn2 in syns2:  # synonyms of a meaning of a tag
    distance = wn.path_similarity(syns1[0], syns2[0])
    if not distance:
        distance = wn.path_similarity(syns2[0], syns1[0])

    if distance and distance > threshold:
        print("word1: " + word1 + "; word2: " + word2 + " -- syn1: " + str(syn1) + "; syn2: " + str(
            syn2) + "; dist: " + str(distance))


def compare1(word1, word2, threshold=0.0):
    syns1 = wn.synsets(word1)
    syns2 = wn.synsets(word2)
    for syn2 in syns2:  # different meanings of the tag
        for synonym in syn2.lemmas(lang='eng'):  # synonyms of a meaning of a tag
            for syn1 in syns1:  # different meaning of the Activity name
                for syn3 in wn.synsets(synonym.name()):  # different meanings of a synonym
                    distance = syn1.path_similarity(syn3)
                    if distance and distance > threshold:
                        print("word1: " + word1 + "; word2: " + word2 + " (" + synonym.name() + ") -- syn1: " + str(
                            syn1) + "; syn2: " + str(syn2) + "; dist: " + str(distance))


def check():
    activity_dao = ActivityDao()
    tag_dao = TagDao()
    all_activities = activity_dao.getAll(-1)
    freq = dict()
    threshold = 0.0

    for activity in all_activities:
        print("Activity: " + activity.name)
        for tag_id1 in activity.tags:
            tag = tag_dao.getById(tag_id1)
            tagLabel = tag[0].label.replace(' ', '_')
            # print("Tag: " + tagLabel)
            check_synonyms_wordnet(activity, tagLabel, threshold)


if __name__ == "__main__":
    check()
