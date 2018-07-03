from model.Tag import Tag


class TagDao:

    def __init__(self, baseConnection):
        kb = baseConnection
        self.connection = kb.getDB()

    def count(self):
        query = "SELECT count(*) FROM Tag"
        result = self.connection.query(query)
        return result

    def getAll(self, limit=-1):
        query = "SELECT * FROM Tag limit " + str(limit)
        # print("TagDao.getAll: " + query)
        result = self.connection.query(query)
        response = list()
        for tag_record in result:
            response.append(self.to_tag(tag_record))
        return response

    def exist(self, label):
        result = self.getByLabel(label.replace('"', ''))
        if (result):
            return result[0].rid
        return result

    def getByLabel(self, label):
        query = "SELECT * FROM Tag WHERE label = \"{0}\"".format(label.replace('"', ''))
        # print(query)
        result = self.connection.query(query)
        response = list()
        for tag_record in result:
            response.append(self.to_tag(tag_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM Tag WHERE @rid = {0}".format(id)
        # print(query)
        result = self.connection.query(query)
        response = list()
        for tag_record in result:
            response.append(self.to_tag(tag_record))
        return response

    def update(self, tag):
        cmd = "UPDATE Tag CONTENT {1} WHERE @rid= {0}".format(tag.rid, tag.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, tag):
        cmd = "INSERT INTO Tag CONTENT {0}".format(tag.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for tag_record in result:
            response.append(self.to_tag(tag_record))
        return response

    @staticmethod
    def to_tag(tag):
        label = tag.__getattr__('label')
        description_activity = tag.__getattr__('description_activity')
        description_prescription = tag.__getattr__('description_prescription')
        domain = tag.__getattr__('domain')
        lang = tag.__getattr__('lang')
        try:
            includes = tag.__getattr__('INCLUDES')
        except AttributeError:
            includes = list()
        try:
            synonyms = tag.__getattr__('synonyms')
        except AttributeError:
            synonyms = list()
        response = Tag(label, description_activity, description_prescription, domain, lang, includes, synonyms)
        response.rid = tag._rid
        return response


if __name__ == "__main__":
    myDao = TagDao()
    tag = Tag("label221", "description_Activity1", "description_prescription", "domain", "en", list(),
              list())

    result0 = myDao.getAll()
    rid0 = result0[0].rid

    if (rid0):
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].label))

    result2 = myDao.add(tag)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].label))

    tag.name = "newtagName22555"
    rid = result2[0].rid
    tag.rid = rid
    result3 = myDao.update(tag)
    print("UPDATE: Count:", result3[0])
