class Tenant:

    def __init__(self, name):
        self.rid = ""
        self.new(name, "", "")

    def new(self, name, lat, lon):
        self.name = name  # Mandatory, String
        self.lat = lat  # String
        self.lon = lon  # String

    def toDict(self):
        contact = dict(
            name=self.name,
            lat=self.lat,
            lon=self.lon,
        )
        return contact


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Tenant.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = Tenant("contactName")
            cmd = "INSERT INTO Tenant CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
