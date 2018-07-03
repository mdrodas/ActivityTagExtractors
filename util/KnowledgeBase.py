import pyorient


class KnowledgeBase:

    def __init__(self):
        self.read_knowledge_base()

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

    def read_knowledge_base(self):
        encoding = 'utf8'
        path_in = "../resources/knowledgeBase.properties"
        with open(path_in, encoding=encoding) as fp:
            self.port = 2424
            for line in fp:
                new_line = line.strip('\n').split('=')
                if (new_line[0] == "knowledgebase.server"):
                    self.server = new_line[1]
                if (new_line[0] == "knowledgebase.db"):
                    self.DBName = new_line[1]
                if (new_line[0] == "knowledgebase.user"):
                    self.user = new_line[1]
                if (new_line[0] == "knowledgebase.pass"):
                    self.password = new_line[1]
                if (new_line[0] == "knowledgebase.maxconnectionattempts"):
                    self.max_connections = new_line[1]


if __name__ == "__main__":
    kb1 = KnowledgeBase()
    KnowledgeBase.getClusterIds(kb1.db)
