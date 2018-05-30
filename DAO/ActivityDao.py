from util.KnowledgeBase import KnowledgeBase
from model.Activity import Activity


class ActivityDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def has_tag(self, activity_id, tag_id):
        query = "select * from activity where @rid = {0} and tags contains (@rid = {1})".format(activity_id, tag_id)
        #print(query)
        result = self.connection.query(query)
        response = False
        if (result):
            response = True
        return response

    def getAll(self,limit=-1):
        query = "SELECT * FROM activity limit "+str(limit)
        print(query)
        result = self.connection.query(query)
        response = list()
        for activity_record in result:
            response.append(self.to_activity(activity_record))
        return response

    def exist(self, name):
        result = self.getByName(name)
        if (result):
            return result[0].rid
        return result

    def getByName(self, name):
        query = "SELECT * FROM Activity WHERE name = \"{0}\"".format(name)
        print(query)
        result = self.connection.query(query)
        response = list()
        for activity_record in result:
            response.append(self.to_activity(activity_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM Activity WHERE @rid = {0}".format(id)
        print(query)
        result = self.connection.query(query)
        response = list()
        for activity_record in result:
            response.append(self.to_activity(activity_record))
        return response

    def update(self, activity):
        cmd = "UPDATE Activity MERGE {1} WHERE @rid= {0} ".format(activity.rid, activity.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, activity):

        cmd = "INSERT INTO Activity CONTENT {0}".format(activity.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for activity_record in result:
            response.append(self.to_activity(activity_record))
        return response

    def to_activity(self, activity):
        new_activity = Activity(activity.__getattr__('name'))
        new_activity.rid = activity._rid  # string
        new_activity.name = activity.__getattr__('name')  # mandatory, string
        new_activity.description = activity.__getattr__('description')  # mandatory, string
        new_activity.longdescription = activity.__getattr__('longdescription')  # string
        new_activity.location = "#"+activity.__getattr__('location').get()  # mandatory, Place
        new_activity.starts = str(activity.__getattr__('starts'))  # date
        new_activity.duration = activity.__getattr__('duration')  # integer
        for internal_tag in activity.__getattr__('tags'): # list of rids
            new_activity.tags.append("#"+internal_tag.get())
        new_activity.admissioncostperperson = float(activity.__getattr__('admissioncostperperson')) # float
        new_activity.friwalkprovided = activity.__getattr__('friwalkprovided')  # boolean
        new_activity.groupsuitable = activity.__getattr__('groupsuitable')  # boolean
        new_activity.bringfriends = activity.__getattr__('bringfriends')  # boolean
        new_activity.isequipped = activity.__getattr__('isequipped')  # Mandatory, boolean
        new_activity.tenancy = "#"+activity.__getattr__('tenancy').get()  # Mandatory, Tenant
        return new_activity


if __name__ == "__main__":
    myDao = ActivityDao()
    activity = Activity("activityName1")
    activity.new("activityName122", "descriptionActivity1", "", "#57:0", "2018-10-10", 0, list(), 0,
                 False, False, False, False, "#25:0")

    result0 = myDao.getAll()
    rid0 = result0[0].rid

    if (rid0):
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].tenancy))
        print("++: {0} - {1} - {2} - {3} - {4} - {5}".format(result[0].rid, result[0].name, result[0].location,
              result[0].tags, result[0].starts, result[0].tenancy))
        print("ACTIVITY: " + str(result[0]))
        for tag in result[0].tags:
            print("TAG: " + tag)

    result2 = myDao.add(activity)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].name))

    activity.name = "newActivityName55"
    rid = result2[0].rid
    activity.rid = rid
    result3 = myDao.update(activity)
    print("UPDATE: Count:", result3[0])
