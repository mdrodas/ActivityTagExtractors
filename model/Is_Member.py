import datetime


class Is_Member:

    def __init__(self, inV, outV):
        self.rid = ""
        rank = 0.0
        status = "accepted"
        timestamp = datetime.datetime.now()
        self.new(inV, outV, rank, status, timestamp)

    def new(self, inV, outV, rank, status, timestamp):
        self.inV = inV  # mandatory, String(Circle.rid)
        self.outV = outV  # mandatory, String (UserProfile.rid)
        self.rank = rank  # double
        self.status = status  # String (recommended, accepted, rejected)
        self.timestamp = timestamp  # datetime

    def toDict(self):
        is_member = dict(
            rank=self.rank,
            status=self.status,
            timestamp=str(self.timestamp),
        )
        return is_member

    def add_edges(self, inV, outV):
        self.inV = inV
        self.outV = outV

if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Is_Member.osql', 'a', newline='') as outfile:
        for i in range(1):
            ismember = Is_Member("#1:0", "#25:0")
            user_rid = "#25:0"
            circle_rid = "#26:0"

            cmd = "Create Edge IS_MEMBER FROM {0} TO {1} CONTENT {2}".format(user_rid, circle_rid, ismember.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
