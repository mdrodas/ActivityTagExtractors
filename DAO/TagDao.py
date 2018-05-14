from util.KnowledgeBase import KnowledgeBase
from model.Tag import Tag


class TagDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def getAll(self):
        query = "SELECT * FROM Tag"
        print("TagDao.getAll: " + query)
        result = self.connection.query(query)
        return result

    def exist(self, label):
        result = self.getByLabel(label.replace('"', ''))
        if (result):
            return result[0]._rid
        return result

    def getByLabel(self, label):
        query = "SELECT * FROM Tag WHERE label = \"{0}\"".format(label.replace('"', ''))
        # print(query)
        result = self.connection.query(query)
        # print("getByLabel:"+ str(result))
        return result

    def getById(self, id):
        query = "SELECT * FROM Tag WHERE @rid = {0}".format(id)
        print(query)
        result = self.connection.query(query)
        return result

    def update(self, rid, tag):
        cmd = "UPDATE Tag CONTENT {0} WHERE @rid= {1}".format(rid, tag)
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, tag):
        cmd = "INSERT INTO Tag CONTENT {0}".format(tag)
        print(cmd)
        result = self.connection.command(cmd)
        return result


if __name__ == "__main__":
    myDao = TagDao()
    tag = Tag("label1", "description_Activity1", "description_prescription", "domain", "en", list(),
              list())

    result0 = myDao.getAll()
    rid0 = result0[0]._rid

    if (rid0):
        result = myDao.getById(rid0)
        print("READ:", result[0])

    result2 = myDao.add(tag.toDict())
    print("CREATE:", result2[0])

    tag.name = "newActivityName5"
    rid = result2[0]._rid
    result3 = myDao.update(tag.toDict(), rid)
    print("UPDATE:", result3[0])
