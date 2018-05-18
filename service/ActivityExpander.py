from util.FileManager import FileManager
from model.Activity import Activity
from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
from nltk.corpus import wordnet as wn


def create_activity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    myDao = ActivityDao()
    id = myDao.exist(name)
    if (not id):
        result = myDao.add(activity.toDict())
        print("CREATE:", result[0])
    else:
        print("Activity Already Exist. Name:" + name + " ID:" + id)
    return activity


def update_activity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    myDao = ActivityDao()
    activity_id = myDao.exist(name)
    result = myDao.update(activity_id, activity.toDict())
    print("Create/Update:", result[0])
    return activity


def activity_hastag(activity_id, tag_id):
    myDao = ActivityDao()
    result = myDao.has_tag(activity_id, tag_id)
    return result


def create_tag(taglabel):
    tagDao = TagDao()
    id = tagDao.exist(taglabel)
    if (not id):
        new_tag = Tag(taglabel, "description_" + taglabel, "", "wordnet", "en", list(), list())
        created_tag = tagDao.add(new_tag)
        print(created_tag[0])
        id = created_tag[0].rid
    return id


def update_activities():
    activity_tags = dict()
    all_tags = dict()
    cleanAllTagsName = "allTagsClean.txt"
    fileManager = FileManager()
    activityName = ""
    description = ""
    location = "#57:0"  # existing dummy location
    isEquiped = False  # assumption is False
    tenancy = "#25:0"  # existing dummy tenancy

    activityDao = ActivityDao()
    tagDao = TagDao()
    all_activities = activityDao.getAll()
    print("len: "+str(len(all_activities)))
    for activity in all_activities:
        similarities = list()
        for tag_id1 in activity.tags:
            # similarities.append(tag_id1)
            tag = tagDao.getById(tag_id1)
            tagLabel = tag[0].label.replace(' ', '_')
            print("Tag: " + tagLabel)
            for my_syn in wn.synsets(tagLabel):
                for syn in my_syn.lemmas(lang='eng'):
                    if (syn.count() > 0):
                        cadena = syn.name()
                        if (tagLabel != cadena):
                            # print(cadena,'+',str(syn.count()))
                            tag_id2 = create_tag(cadena)
                            result = activityDao.has_tag(activity.rid, tag_id2)
                            if (not result and tag_id2 not in similarities):
                                similarities.append(tag_id2)
        print("similarities: " + str(similarities))
        for new_tagid in similarities:
            activity.tags.append(new_tagid)
        activityDao.update(activity)


if __name__ == "__main__":
    update_activities()
