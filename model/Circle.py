class Circle:

    def __init__(self, name, tenancy):
        self.rid = ""
        self.new(name, "recommended", list(""), tenancy)

    def new(self, name, status, tags, tenancy):
        self.name = name  # mandatory, String
        self.status = status  # String [recommended, rejected, accepted]
        self.tags = tags  # list of Tags(rids)
        self.tenancy = tenancy  # Mandatory, Tenancy(rid)

    def toDict(self):
        circle = dict(
            name=self.name,
            status=self.status,
            tags=list(self.tags),
            tenancy=self.tenancy,
        )
        return circle

    def toDictMandatory(self):
        circle = dict(
            name=self.name,
            tags=list(self.tags),
            tenancy=self.tenancy,
        )
        return circle

    def add_tags(self, new_tags):
        for tag_id in new_tags:
            self.tags.append(str(tag_id))


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Circle.osql', 'a', newline='') as outfile:
        for i in range(1):
            circle = Circle("Marcelo22", "#25:0")

            cmd = "INSERT INTO Circle CONTENT {0}".format(circle.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
