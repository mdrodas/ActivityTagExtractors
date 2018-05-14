from util.KnowledgeBase import KnowledgeBase
from model.Activity import Activity


class ActivityDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def getAll(self):
        query = "SELECT * FROM Activity"
        print(query)
        result = self.connection.query(query)
        return result

    def exist(self, name):
        result = self.getByName(name)
        if (result):
            return result[0]._rid
        return result

    def getByName(self, name):
        query = "SELECT * FROM Activity WHERE name = \"{0}\"".format(name.replace('"', ''))
        print(query)
        result = self.connection.query(query)
        print("getByLabel:" + str(result))
        return result

    def getById(self, id):
        query = "SELECT * FROM Activity WHERE @rid = {0}".format(id)
        print(query)
        result = self.connection.query(query)
        return result

    def update(self, rid, activity):
        cmd = "UPDATE Activity CONTENT {0} WHERE @rid= {1}".format(rid, activity)
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, activity):
        cmd = "INSERT INTO Activity CONTENT {0}".format(activity)
        print(cmd)
        result = self.connection.command(cmd)
        return result


if __name__ == "__main__":
    myDao = ActivityDao()
    activity = Activity("activityName1", "descriptionActivity1", "", "#57:0", "2018-10-10", 0, list(), 0,
                        False, False, False, False, "#25:0")

    result0 = myDao.getAll()
    rid0 = result0[0]._rid

    if (rid0):
        result = myDao.getById(rid0)
        print("READ:", result[0])

    result2 = myDao.add(activity.toDict())
    print("CREATE:", result2[0])

    activity.name = "newActivityName5"
    rid = result2[0]._rid
    result3 = myDao.update(activity.toDict(), rid)
    print("UPDATE:", result3[0])
