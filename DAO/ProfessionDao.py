from util.KnowledgeBase import KnowledgeBase
from model.Profession import Profession


class ProfessionDao:

    def __init__(self):
        kb = KnowledgeBase()
        self.connection = kb.getDB()

    def count(self):
        query = "SELECT count(*) FROM Profession"
        result = self.connection.query(query)
        return result

    def getAll(self, limit=-1):
        query = "SELECT * FROM Profession limit " + str(limit)
        # print("ProfessionDao.getAll: " + query)
        result = self.connection.query(query)
        response = list()
        for profession_record in result:
            response.append(self.to_profession(profession_record))
        return response

    def exist(self, jobTitle):
        result = self.getByJobTitle(jobTitle.replace('"', ''))
        if (result):
            return result[0].rid
        return result

    def getByJobTitle(self, jobTitle):
        query = "SELECT * FROM Profession WHERE jobtitle = \"{0}\"".format(jobTitle.replace('"', ''))
        # print(query)
        result = self.connection.query(query)
        response = list()
        for profession_record in result:
            response.append(self.to_profession(profession_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM Profession WHERE @rid = {0}".format(id)
        # print(query)
        result = self.connection.query(query)
        response = list()
        for profession_record in result:
            response.append(self.to_profession(profession_record))
        return response

    def update(self, profession):
        cmd = "UPDATE Profession CONTENT {1} WHERE @rid= {0}".format(profession.rid, profession.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, profession):
        cmd = "INSERT INTO Profession CONTENT {0}".format(profession.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for profession_record in result:
            response.append(self.to_profession(profession_record))
        return response

    def to_profession(self, profession):
        rid = profession._rid
        jobtitle = profession.__getattr__('jobtitle')
        description = profession.__getattr__('description')
        try:
            categories = profession.__getattr__('categories')
        except AttributeError:
            categories = list()

        response = Profession(jobtitle)
        response.rid = rid
        response.description = description
        response.categories = categories

        return response


if __name__ == "__main__":
    myDao = ProfessionDao()
    profession = Profession("newProfession1")

    result0 = myDao.getAll()

    if (result0):
        rid0 = result0[0].rid
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].jobtitle))

    result2 = myDao.add(profession)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].jobtitle))

    profession.jobtitle = "newtagName22555"
    rid = result2[0].rid
    profession.rid = rid
    result3 = myDao.update(profession)
    print("UPDATE: Count:", result3[0])
