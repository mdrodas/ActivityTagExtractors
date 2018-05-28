from DAO.TenantDao import TenantDao
from model.Address import Address
from model.ContactInfo import ContactInfo
from model.Person import Person
from model.Profession import Profession


class UserProfile:

    def __init__(self, screenname, tenancy):
        self.rid = ""
        self.new(screenname, dict(), dict(""), dict(""), dict(""), list(""), list(""), dict(), tenancy)

    def new(self, screenname, address, contactinfo, mobilityrecords, person, preferences, prescriptions, profession,
            tenancy):
        self.screenname = screenname  # mandatory, String
        self.address = address  # Address(rid)
        self.contactinfo = contactinfo  # ContactInfo(rid)
        self.mobilityrecords = mobilityrecords  # list of MobilityRecords(rids)
        self.person = person  # Person (rid)
        self.preferences = preferences  # list of Tags (rids)
        self.prescriptions = prescriptions  # list of Tags (rids)
        self.profession = profession  # Profession(rid)
        self.tenancy = tenancy  # Mandatory Tenancy(rid)

    def toDict(self):
        activity = dict(
            screenname=self.screenname,
            address=self.address,
            contactinfo=self.contactinfo,
            mobilityrecords=self.mobilityrecords,
            person=self.person,
            preferences=list(self.preferences),
            prescriptions=list(self.prescriptions),
            profession=self.profession,
            tenancy=self.tenancy,
        )
        return activity

    def toDictMandatory(self):
        activity = dict(
            screenname=self.screenname,
            tenancy=self.tenancy,
            preferences=self.preferences,
        )
        return activity

    def createRandomUserProfile(self):

        tenantdao = TenantDao()
        tenancy = tenantdao.getByName("Trento")
        if (tenancy):
            userprofile = UserProfile("Marcelo22", tenancy[0].rid)

            profession = Profession("newJobTitle")
            userprofile.profession = profession.toDict()
            address = Address("MyStreetName")
            userprofile.address = address.toDict()
            person = Person("Marcelo", "Rodas", "2001-11-20")
            userprofile.person = person.toDict()
            contact = ContactInfo("Urgency")
            userprofile.contactinfo = contact.toDict()

        return userprofile

    def add_preferences(self, new_tags):
        for tag_id in new_tags:
            self.preferences.append(str(tag_id))


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'UserProfile.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = UserProfile("Marcelo22", "#25:0")

            userProfile = a.createRandomUserProfile()
            cmd = "INSERT INTO UserProfile CONTENT {0}".format(userProfile.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
