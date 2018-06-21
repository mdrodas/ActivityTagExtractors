from util.KnowledgeBase import KnowledgeBase
from model.Tenant import Tenant


class TenantDao:

    def __init__(self, DBName="framework_test10"):
        kb = KnowledgeBase(DBName)
        self.connection = kb.getDB()

    def count(self):
        query = "SELECT count(*) FROM Tenant"
        result = self.connection.query(query)
        return result

    def getAll(self, limit=-1):
        query = "SELECT * FROM Tenant limit " + str(limit)
        # print("TenantDao.getAll: " + query)
        result = self.connection.query(query)
        response = list()
        for tenant_record in result:
            response.append(self.to_tenant(tenant_record))
        return response

    def get_one_placeRid(self, limit=1):
        query = "SELECT * FROM Place limit " + str(limit)
        # print("TenantDao.getAll: " + query)
        result = self.connection.query(query)
        response = ""
        if result:
            response = result[0]._rid
        return response

    def exist(self, name):
        result = self.getByName(name.replace('"', ''))
        if (result):
            return result[0].rid
        return result

    def getByName(self, name):
        query = "SELECT * FROM Tenant WHERE name = \"{0}\"".format(name)
        # print(query)
        result = self.connection.query(query)
        response = list()
        for tenant_record in result:
            response.append(self.to_tenant(tenant_record))
        return response

    def getById(self, id):
        query = "SELECT * FROM Tenant WHERE @rid = {0}".format(id)
        # print(query)
        result = self.connection.query(query)
        response = list()
        for tenant_record in result:
            response.append(self.to_tenant(tenant_record))
        return response

    def update(self, tenant):
        cmd = "UPDATE Tenant CONTENT {1} WHERE @rid= {0}".format(tenant.rid, tenant.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        return result

    def add(self, tenant):
        cmd = "INSERT INTO Tenant CONTENT {0}".format(tenant.toDict())
        # print(cmd)
        result = self.connection.command(cmd)
        response = list()
        for tenant_record in result:
            response.append(self.to_tenant(tenant_record))
        return response

    def to_tenant(self, tenant):
        label = tenant.__getattr__('name')
        lon = tenant.__getattr__('lon')
        lat = tenant.__getattr__('lat')

        response = Tenant(label)
        response.new(label, lat, lon)
        response.rid = tenant._rid
        return response


if __name__ == "__main__":
    myDao = TenantDao()
    tenant = Tenant("tenantX")

    result0 = myDao.getAll()

    if (result0):
        rid0 = result0[0].rid
        result = myDao.getById(rid0)
        print("READ: {0} - {1}".format(result[0].rid, result[0].name))

    result2 = myDao.add(tenant)
    print("CREATE: {0} - {1}".format(result2[0].rid, result2[0].name))

    tenant.name = "newtenantName22555"
    rid = result2[0].rid
    tenant.rid = rid
    result3 = myDao.update(tenant)
    print("UPDATE: Count:", result3[0])
