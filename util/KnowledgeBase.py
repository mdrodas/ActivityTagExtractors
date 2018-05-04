import pyorient


class KnowledgeBase:

    def __init__(self):
        self.db = pyorient.OrientDB("localhost", 2424)
        self.kb = self.db.db_open("KB_Trento", "admin", "admin")

    # returns list of cluster ids for UserProfile class
    def getClusterIds(db):
        clusterid_query = "SELECT name, clusterIds FROM (SELECT EXPAND(classes) FROM metadata:schema) WHERE name = 'UserProfile'"
        result = db.query(clusterid_query)
        return result[0].oRecordData['clusterIds']


if __name__ == "__main__":
    kb1 = KnowledgeBase()
    KnowledgeBase.getClusterIds(kb1.db)
