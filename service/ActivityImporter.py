from util.FileManager import FileManager
from model.Activity import Activity
from DAO.ActivityDao import ActivityDao


def createActivity(name, description, location, isEquiped, tenancy, tags):
    activity = Activity(name, description, "", location, "2018-01-01", 0, tags, 0,
                        False, False, False, isEquiped, tenancy)
    return activity


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
        length = len(words)-1
        for i in range(1, length):
            tag = words[i].lower().strip()
            tags.append(tag)

        activity = createActivity(activityName, description, location, isEquiped, tenancy, tags)
        #print(activity.toDictMandatory())

        myDao = ActivityDao()
        result = myDao.add(activity.toDictMandatory())
        print("CREATE:", result[0])
