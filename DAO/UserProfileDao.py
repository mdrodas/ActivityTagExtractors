from util.KnowledgeBase import KnowledgeBase
from model.UserProfile import UserProfile


class UserProfileDao:

    def __init__(self, baseConnection):
        kb = baseConnection
        self.connection = kb.getDB()

    def has_tag(self, user_id, tag_id):
        query = "select * from UserProfile where @rid = {0} and preferences contains (@rid = {1})".format(user_id,
                                                                                                          tag_id)
        # print(query)
        result = self.connection.query(query)
        response = False
        if (result):
            response = True
        return response

    def getAll(self, limit=-1):
        query = "SELECT * FROM UserProfile limit " + str(limit)
        print(query)
        result = self.connection.query(query)
        response = list()
        for user_record in result:
            response.append(self.to_UserProfile(user_record))
        return response

    def exist(self, name):
        result = self.getByScreenname(name)
        if (result):
            return result[0].rid
        return result

    def getByScreenname(self, name):
        query = "SELECT * FROM UserProfile WHERE screenname = \"{0}\"".format(name.replace('"', ''))
        # print(query)
        result = self.connection.query(query)
        response = list()
        for user_record in result:
            response.append(self.to_UserProfile(user_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM UserProfile WHERE @rid = {0}".format(id)
        print(query)
        result = self.connection.query(query)
        response = list()
        for user_record in result:
            response.append(self.to_UserProfile(user_record))
        return response

    def update(self, user):
        cmd = "UPDATE UserProfile MERGE {1} WHERE @rid= {0} ".format(user.rid, user.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, user):
        cmd = "INSERT INTO UserProfile CONTENT {0}".format(user.toDict())
        print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for user_record in result:
            response.append(self.to_UserProfile(user_record))
        return response

    @staticmethod
    def to_UserProfile(user):
        screenname = user.__getattr__('screenname')  # mandatory, string
        try:
            tenancy0 = user.__getattr__('tenancy')
            tenancy = "#" + tenancy0.get()  # Mandatory, Tenant
        except AttributeError:
            tenancy = ""
        new_user = UserProfile(screenname, tenancy)
        new_user.rid = user._rid  # string

        try:
            address = user.__getattr__('address')  # string
        except AttributeError:
            address = ""
        try:
            contactinfo = user.__getattr__('contactinfo')  # string
        except AttributeError:
            contactinfo = ""
        try:
            mobilityrecords = user.__getattr__('mobilityrecords')  # string
        except AttributeError:
            mobilityrecords = dict()
        try:
            person = user.__getattr__('person')  # Person
        except AttributeError:
            person = ""
        try:
            preferences = user.__getattr__('preferences')  # list of Tags
        except AttributeError:
            print("Opss...")
            preferences = list("")
        try:
            prescriptions = user.__getattr__('prescriptions')  # list of Tags
        except AttributeError:
            prescriptions = ""
        try:
            profession = user.__getattr__('profession')  # Profession(rid)
        except AttributeError:
            profession = ""

        new_user.address = address
        new_user.contactinfo = contactinfo
        new_user.mobilityrecords = mobilityrecords
        new_user.person = person
        new_user.preferences = preferences
        new_user.prescriptions = prescriptions
        new_user.profession = profession

        return new_user


if __name__ == "__main__":
    myDao = UserProfileDao()
    user1 = UserProfile("Marcelo", "#25:0")  # tenancy #25:0
    user = user1.createRandomUserProfile()  # tenancy #25:0

    result0 = myDao.getAll()

    if (result0):
        rid0 = result0[100].rid
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].tenancy))
        print("++: {0} - {1} - {2} - {3} ".format(result[0].rid, result[0].screenname, str(result[0].preferences),
                                                  result[0].tenancy))
        print("UserProfile: " + str(result[0]))
        for tag in result[0].preferences:
            print("preferences: " + str(tag))
        user.add_preferences(result[0].preferences)

    result2 = myDao.add(user)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].screenname))

    user.screenname = "newMarcelo23"
    rid = result2[0].rid
    user.rid = rid
    result3 = myDao.update(user)
    print("UPDATE: Count:", result3[0])
