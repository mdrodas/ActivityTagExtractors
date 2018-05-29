from util.KnowledgeBase import KnowledgeBase
from model.Circle import Circle
from DAO.TagDao import TagDao

class CircleDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def has_tag(self, user_id, tag_id):
        query = "select * from Circle where @rid = {0} and tags contains (@rid = {1})".format(user_id, tag_id)
        # print(query)
        result = self.connection.query(query)
        response = False
        if (result):
            response = True
        return response

    def getAll(self, limit=-1):
        query = "SELECT * FROM Circle limit " + str(limit)
        print(query)
        result = self.connection.query(query)
        response = list()
        for circle_record in result:
            response.append(self.to_Circle(circle_record))
        return response

    def exist(self, name):
        result = self.getByName(name)
        if (result):
            return result[0].rid
        return result

    def getByName(self, name):
        query = "SELECT * FROM Circle WHERE name = \"{0}\"".format(name.replace('"', ''))
        # print(query)
        result = self.connection.query(query)
        response = list()
        for circle_record in result:
            response.append(self.to_Circle(circle_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM Circle WHERE @rid = {0}".format(id)
        print(query)
        result = self.connection.query(query)
        response = list()
        for circle_record in result:
            response.append(self.to_Circle(circle_record))
        return response

    def update(self, user):
        cmd = "UPDATE Circle MERGE {1} WHERE @rid= {0} ".format(user.rid, user.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, user):
        cmd = "INSERT INTO Circle CONTENT {0}".format(user.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for circle_record in result:
            response.append(self.to_Circle(circle_record))
        return response

    def to_Circle(self, circle):
        name = circle.__getattr__('name')  # mandatory, string
        try:
            tenancy0 = circle.__getattr__('tenancy')
            tenancy = "#" + tenancy0.get()  # Mandatory, Tenant
        except AttributeError:
            tenancy = ""

        new_circle = Circle(name, tenancy)
        new_circle.rid = circle._rid  # string
        status = circle.__getattr__('status')  # string
        try:
            tags = circle.__getattr__('tags')  # list of Tags(rids)
        except AttributeError:
            tags = list("")

        new_circle.status = status
        new_circle.tags = tags

        return new_circle


if __name__ == "__main__":
    myDao = CircleDao()
    tagDao = TagDao()
    circle = Circle("CircleNew", "#113:0")  # tenancy #25:0

    result0 = myDao.getAll()

    if (result0):
        rid0 = result0[0].rid
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].tenancy))
        print("+: {0} - {1} - {2} - {3}".format(result[0].rid, result[0].name, str(result[0].tags), result[0].tenancy))
        print("Circle: " + str(result[0]))
        for tag in result[0].tags:
            print("Circle tags: " + str(tag))
        circle.add_tags(result[0].tags)
    else:
        tags = tagDao.getAll(2)
        tags2 = list()
        for tag in tags:
            tags2.append(tag.rid)
        print("tags: "+str(tags2))
        circle.add_tags(tags2)


    result2 = myDao.add(circle)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].name))

    circle.name = "newCircle23"
    rid = result2[0].rid
    circle.rid = rid
    result3 = myDao.update(circle)
    print("UPDATE: Count:", result3[0])
