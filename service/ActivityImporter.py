from util.FileManager import FileManager
from model.Activity import Activity
from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
import json


def createActivity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    return activity


def save(tag):
    tagDao = TagDao()
    id = tagDao.exist(tag)
    if (not id):
        tag = Tag(tag, "description_" + tag, "", "crowd", "en", list(), list())
        newTag = tagDao.add(tag.toDictMandatory())
        print(newTag)
        id = newTag[0]._rid
    return id


if __name__ == "__main__":
    activity_tags = dict()
    all_tags = dict()
    allTagsName = "allTags.txt"
    cleanAllTagsName = "allTagsClean.txt"
    tagsFrequencyName = "tagsFrequency.txt"
    fileManager = FileManager()

    activityName = ""
    description = ""
    location = "#57:0"  # existing dummy location
    isEquiped = False  # asumption is False
    tenancy = "#25:0"  # existing dummy tenancy
    tags = list()

    myFile = fileManager.readResource(cleanAllTagsName)
    for line in myFile[0:-2]:
        print(line)
        words = line.split('\t')
        activityName = words[0].lower().strip()
        description = "-".join(words[1:4])
        length = len(words) - 1
        for i in range(1, length):
            tag = words[i].lower().strip()

            id = save(tag.replace('"', ''))
            if (id):
                tags.append(id)
            else:
                print("errorTag: ", tag)

        activity = createActivity(activityName, description, location, isEquiped, tenancy, tags)
        # print(activity.toDictMandatory())

        myDao = ActivityDao()
        activity = False
        id = myDao.exist(activityName)
        if (not id):
            result = myDao.add(activity.toDictMandatory())
            print("CREATE:", result[0])
        else:
            print("Activity Already Exist. Name:"+activityName+" ID:"+id)
