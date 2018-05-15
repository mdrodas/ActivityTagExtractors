from util.FileManager import FileManager
from model.Activity import Activity
from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
import json


def create_activity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    myDao = ActivityDao()
    id = myDao.exist(name)
    if (not id):
        result = myDao.add(activity.toDictMandatory())
        print("CREATE:", result[0])
    else:
        print("Activity Already Exist. Name:" + name + " ID:" + id)
    return activity


def update_activity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    myDao = ActivityDao()
    activity_id = myDao.exist(name)
    result = myDao.update(activity_id, activity.toDictMandatory())
    print("Create/Update:", result[0])
    return activity


def activity_hastag(activity_id, tag_id):
    myDao = ActivityDao()
    result = myDao.has_tag(activity_id, tag_id)
    return result


def create_tag(tag):
    tagDao = TagDao()
    id = tagDao.exist(tag)
    if (not id):
        tag = Tag(tag, "description_" + tag, "", "crowd", "en", list(), list())
        newTag = tagDao.add(tag.toDictMandatory())
        print(newTag)
        id = newTag[0]._rid
    return id


def create_activities():
    activity_tags = dict()
    all_tags = dict()
    cleanAllTagsName = "allTagsClean.txt"
    fileManager = FileManager()
    activityName = ""
    description = ""
    location = "#57:0"  # existing dummy location
    isEquiped = False  # assumption is False
    tenancy = "#25:0"  # existing dummy tenancy
    myFile = fileManager.readResource(cleanAllTagsName)
    for line in myFile[0:-2]:
        tags = list()
        print(line)
        words = line.split('\t')
        activityName = words[0].lower().strip()
        description = "-".join(words[1:4])
        length = len(words) - 1
        for i in range(1, length):
            tag = words[i].lower().strip()

            id = create_tag(tag.replace('"', ''))
            if (id):
                tags.append(id)
            else:
                print("error creating tag: ", tag)
        activity = create_activity(activityName, description, location, isEquiped, tenancy, tags)
        # print(activity.toDictMandatory())


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

    myFile = fileManager.readResource(cleanAllTagsName)
    for line in myFile[0:-2]:
        tags = list()
        print(line)
        words = line.split('\t')
        activityName = words[0].lower().strip()
        description = "-".join(words[1:4])
        length = len(words) - 1
        for i in range(1, length):
            tag = words[i].lower().strip()

            id = create_tag(tag.replace('"', ''))
            if (id):
                tags.append(id)
            else:
                print("error creating tag: ", tag)

        activity = update_activity(activityName, description, location, isEquiped, tenancy, tags)
        # print(activity.toDictMandatory())


if __name__ == "__main__":
    create = False
    if (create):
        create_activities()
    else:
        update_activities()
