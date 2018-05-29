class Profession:

    def __init__(self, jobtitle):
        self.rid = ""
        self.new(jobtitle, "", list(""))

    def new(self, jobtitle, description, categories):
        self.jobtitle = jobtitle  # mandatory, String
        self.description = description  # String
        self.categories = categories  # list of Tags

    def toDict(self):
        profession = dict(
            jobtitle=self.jobtitle,
            description=self.description,
            categories=self.categories,
        )
        return profession

    def toDictMandatory(self):
        profession = dict(
            jobtitle=self.jobtitle,
            categories=list(self.categories),
        )
        return profession

    def add_categories(self, new_tags):
        for tag_id in new_tags:
            self.categories.add(tag_id)


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Profession.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = Profession("jobtitle2")
            cmd = "INSERT INTO Profession CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
