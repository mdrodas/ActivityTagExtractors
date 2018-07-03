from util.FileManager import FileManager
from model.Activity import Activity
from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao
from util.KnowledgeBase import KnowledgeBase


class ActivityImporter:

    def __init__(self):
        self.kb = KnowledgeBase()

    def create_activity(self, name, description, isEquiped, tags):
        tenantdao = TenantDao(self.kb)
        tenant = tenantdao.getByName("Trento")
        location = tenantdao.get_one_placeRid()
        activity = Activity(name)
        if (tenant and location):
            tenancy = tenant[0].rid
            activity.new(name, description, "", location, "2000-01-01", 0, tags, 0.0,
                         False, False, False, isEquiped, tenancy)
            myDao = ActivityDao(self.kb)
            id = myDao.exist(name)
            activity.rid = id
            if (not id):
                result = myDao.add(activity)
                # print("CREATE:", result[0])
            else:
                print("Activity Already Exist. Name:" + name + " ID:" + id)
        return activity


    def update_activity(self, name, description, location, isEquiped, tags):
        tenantdao = TenantDao(self.kb)
        tenant = tenantdao.getByName("Trento")
        location = tenantdao.get_one_placeRid()
        activity = Activity(name)
        if (tenant and location):
            tenancy = tenant[0].rid
            activity.new(name, description, "", location, "2000-01-01", 0, tags, 0,
                         False, False, False, isEquiped, tenancy)
            myDao = ActivityDao(self.kb)
            activity_id = myDao.exist(name)
            activity.rid = activity_id
            result = myDao.update(activity)
            print("Create/Update:", result[0])
        return activity


    def activity_hastag(self, activity_id, tag_id):
        myDao = ActivityDao(self.kb)
        result = myDao.has_tag(activity_id, tag_id)
        return result


    def create_tag(self, tag):
        tagDao = TagDao(self.kb)
        id = tagDao.exist(tag)
        if (not id):
            tag = Tag(tag, "description_" + tag, "", "crowd", "en", list(), list())
            newTag = tagDao.add(tag)
            print(newTag)
            id = newTag[0].rid
        return id


    def create_activities(self, create):
        activity_tags = dict()
        all_tags = dict()
        cleanAllTagsName = "allTagsClean.txt"
        directory = "../resources/crowd/"
        fileManager = FileManager()
        fileManager.new(directory, cleanAllTagsName, "")
        activityName = ""
        description = ""
        isEquiped = False  # assumption is False
        myFile = fileManager.readFile()
        for line in myFile[0:-2]:
            tags = list()
            print(line)
            words = line.split('\t')
            activityName = words[0].lower().strip().replace('"', '')
            description = "-".join(words[1:4])
            length = len(words) - 1
            for i in range(1, length):
                tag = words[i].lower().strip()

                id = self.create_tag(tag.replace('"', ''))
                if (id):
                    tags.append(id)
                else:
                    print("error creating tag: ", tag)
            if (create):
                activity = self.create_activity(activityName, description, isEquiped, tags)
            else:
                activity = self.update_activity(activityName, description, isEquiped, tags)
            # print(activity.toDictMandatory())


if __name__ == "__main__":
    create = True
    app = ActivityImporter()
    if (create):
        app.create_activities(create)
