class Tag:

    def __init__(self, label, description_activity, description_prescription, domain, lang, Includes, synonyms):
        self.rid = "#0:0"
        self.label = label  # string,mandatory
        self.description_activity = description_activity  # string
        self.description_prescription = description_prescription  # string
        self.domain = domain  # string
        self.lang = lang  # string
        self.Includes = Includes  # Linkset(Tag)
        self.synonyms = synonyms  # EmbeddedSet(String)

    def toDict(self):
        tag = dict(
            label=self.label,  # string,mandatory
            description_activity=self.description_activity,
            description_prescription=self.description_prescription,
            domain=self.domain,
            lang=self.lang,
            Includes=self.Includes,  # Linkset(Tag)
            synonyms=self.synonyms,  # EmbeddedSet(String)
        )
        return tag

    def toDictMandatory(self):
        tag = dict(
            label=self.label,
        )
        return tag


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'tags.osql', 'a', newline='') as outfile:
        for i in range(10):
            activity = Tag.createRandomActivity()
            cmd = "INSERT INTO Tag CONTENT {0}".format(activity)
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
