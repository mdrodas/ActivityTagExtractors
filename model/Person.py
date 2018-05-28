
class Person:

    def __init__(self, firstName, familyName, birthDate):
        self.rid = ""
        self.new(firstName,familyName,birthDate,"","",0,"",list(""),"","User")

    def new(self, firstName, familyName, birthDate, civilStatus, completeName, education, gender, languages,
            phonenumber, role):
        self.firstName = firstName  # mandatory, String
        self.familyName = familyName  # mandatory, String
        self.birthDate = birthDate  # mandatory, Date
        self.civilStatus = civilStatus  # #String
        self.completeName = completeName  # String
        self.education = education  # Integer
        self.gender = gender  # String
        self.languages = languages  # List of Strings
        self.phonenumber = phonenumber  # String
        self.role = role  # String

    def toDict(self):
        person = dict(
            firstName = self.firstName,  # mandatory
            familyName = self.familyName,  # mandatory
            birthDate = self.birthDate,  # mandatory
            civilStatus = self.civilStatus, # #String
            completeName = self.completeName,  # String
            education = self.education,  # Integer
            gender = self.gender,  # String
            languages = self.languages,  # List of Strings
            phonenumber = self.phonenumber,  # String
            role = self.role,  # String
        )
        return person

    def toDictMandatory(self):
        person = dict(
            firstName = self.firstName,  # mandatory
            familyName = self.familyName,  # mandatory
            birthDate = self.birthDate,  # mandatory
        )
        return person


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Person.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = Person("name","lastname", "17/04/2018")
            cmd = "INSERT INTO Person CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
