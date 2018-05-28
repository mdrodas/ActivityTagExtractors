class MobilityRecord:

    def __init__(self, date):
        self.rid = ""
        if (not date):
            date = "1900-01-01"
        self.date = date # Date

    def toDict(self):
        mobility = dict(
            date=self.date,
        )
        return mobility


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'MobilityRecord.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = MobilityRecord("2018-04-11")
            cmd = "INSERT INTO MobilityRecord CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
