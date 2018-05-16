import datetime
import random
import radar
import loremipsum


class Activity:

    def __init__(self, name):
        self.name = name  # mandatory
        self.tags = list()

    def new(self, name, description, longdescription, location, starts, duration, tags, admissioncostperperson,
                 friwalkprovided, groupsuitable, bringfriends, isequipped, tenancy):
        self.name = name  # mandatory
        self.description = description  # mandatory
        self.longdescription = longdescription
        self.location = location  # mandatory
        self.starts = starts
        self.duration = duration
        self.tags = tags
        self.admissioncostperperson = admissioncostperperson
        self.friwalkprovided = friwalkprovided
        self.groupsuitable = groupsuitable
        self.bringfriends = bringfriends
        self.isequipped = isequipped  # Mandatory
        self.tenancy = tenancy  # Mandatory

    def toDict(self):
        activity = dict(
            name=self.name,
            description=self.description,
            longdescription=self.longdescription,
            location=self.location,
            starts=self.starts,
            duration=self.duration,
            tags=list(self.tags),
            admissioncostperperson=self.admissioncostperperson,
            friwalkprovided=self.friwalkprovided,
            groupsuitable=self.groupsuitable,
            bringfriends=self.bringfriends,
            isequipped=self.isequipped,
            tenancy=self.tenancy,
        )
        return activity

    def toDictMandatory(self):
        activity = dict(
            name=self.name,
            description=self.description,
            location=self.location,
            isequipped=self.isequipped,
            tenancy=self.tenancy,
            tags=list(self.tags),
        )
        return activity

    def createRandomActivity(self):
        soon = datetime.datetime.today() + datetime.timedelta(days=random.randint(14, 32))
        tags = dict()
        activity = dict(
            name=" ".join(tags.keys()),
            description=loremipsum.get_sentence(start_with_lorem=False).replace("'", "`"),
            longdescription=' '.join(
                [t.replace("'", "`") for t in loremipsum.get_sentences(3, start_with_lorem=False)]),
            location=dict(),
            starts=radar.random_date(start=soon,
                                     stop=datetime.datetime(year=2019, month=12, day=31)).strftime('%Y-%m-%d %H:%M:%S'),
            duration=random.randint(1, 12) * 15,
            tags=list(tags.values()),
            admissioncostperperson=random.randint(0, 35),
            friwalkprovided=random.choice((True, False)),
            groupsuitable=random.choice((True, False)),
            bringfriends=random.choice((True, False)),
            isequipped=random.choice((True, False)),
        )
        return activity


    def add_tags(self,new_tags):
        for tag_id in new_tags:
            self.tags.add(tag_id)

if __name__ == "__main__":

    with open('activities.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = Activity("")
            activity = a.createRandomActivity()
            cmd = "INSERT INTO Activity CONTENT {0}".format(activity)
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
