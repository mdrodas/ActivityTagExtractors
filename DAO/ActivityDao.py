from util.KnowledgeBase import KnowledgeBase
from model.Activity import Activity


class ActivityDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def getActivityById(self, id):
        query = "SELECT * FROM Activity WHERE @rid = " + id
        print(query)
        result = self.connection.query(query)
        return result

    def updateActivity(self, rid, activity):
        cmd = "UPDATE Activity CONTENT {0} WHERE @rid= {1}".format(rid, activity)
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def setActivity(self, activity):
        cmd = "INSERT INTO Activity CONTENT {0}".format(activity)
        print(cmd)
        result = self.connection.command(cmd)
        return result


if __name__ == "__main__":
    myDao = ActivityDao()
    activity = Activity("activityName1", "descriptionActivity1", "", "#57:0", "2018-10-10", 0, list(), 0,
                        False, False, False, False, "#25:0")

    result = myDao.getActivityById("#66:2")
    print("READ:",result[0])

    result2 = myDao.setActivity(activity.toDict())
    print("CREATE:",result2[0])

    activity.name = "newActivityName5"
    rid = result2[0]._rid
    result3 = myDao.updateActivity(activity.toDict(), rid)
    print("UPDATE:",result3[0])
