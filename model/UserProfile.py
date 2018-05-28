
class UserProfile:

    def __init__(self, screenname, tenancy):
        self.rid = ""
        self.screenname = screenname  # mandatory
        self.tenancy = tenancy  # mandatory
        self.preferences = list()  # needed

    def new(self, screenname, address, contactinfo, mobilityrecords, person, preferences, prescriptions, profession,
            tenancy):
        self.screenname = screenname  # mandatory, String
        self.address = address  # Address
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
            preferences=list(self.preferences),
        )
        return activity

    def createRandomUserProfile(self):
        userprofile = UserProfile("name", "tenancy")
        return userprofile

    def add_tags(self, new_tags):
        for tag_id in new_tags:
            self.tags.add(tag_id)


if __name__ == "__main__":

    with open('UserProfile.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = UserProfile("")
            activity = a.createRandomUserProfile()
            cmd = "INSERT INTO UserProfile CONTENT {0}".format(activity)
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
