class ContactInfo:

    def __init__(self, name):
        self.rid = ""
        self.new(name, "")

    def new(self, name, phonenr):
        self.name = name  # String
        self.phonenr = phonenr  # String

    def toDict(self):
        contact = dict(
            name=self.name,
            phonenr=self.phonenr,
        )
        return contact


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'ContactInfo.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = ContactInfo("contactName")
            cmd = "INSERT INTO ContactInfo CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
