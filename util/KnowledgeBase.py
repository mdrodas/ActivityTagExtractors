import pyorient


class KnowledgeBase:

    def __init__(self, DBName="framework_test10"):
        self.server = "localhost"
        self.port = 2424
        self.user = "admin"
        self.password = "admin"
        self.DBName = DBName

        self.db = pyorient.OrientDB(self.server, self.port)
        self.kb = self.db.db_open(self.DBName, self.user, self.password)

    def set_server(self, server):
        self.server = server

    def set_user(self, user):
        self.user = user

    def set_pass(self, password):
        self.password = password

    def getDB(self):
        return self.db

    def getKB(self):
        return self.kb

    def open_connection(self):
        self.db = pyorient.OrientDB(self.server, self.port)
        self.kb = self.db.db_open(self.DBName, self.user, self.password)

    def close_connection(self):
        self.db.close()

    # returns list of cluster ids for UserProfile class
    def getClusterIds(db):
        clusterid_query = "SELECT name, clusterIds FROM (SELECT EXPAND(classes) FROM metadata:schema) WHERE name = 'UserProfile'"
        result = db.query(clusterid_query)

        return result[0].oRecordData['clusterIds']


if __name__ == "__main__":
    kb1 = KnowledgeBase()
    KnowledgeBase.getClusterIds(kb1.db)
