from util.FileManager import FileManager
from model.Is_Member import Is_Member
from DAO.CircleDao import CircleDao


class IsMemberImporter:

    def create_ismember(self, circle_rid, users):
        global write_on_db
        myDao = CircleDao()

        for user_rid in users:
            ismember = myDao.get_is_member(circle_rid, user_rid)
            if (not ismember):
                ismember = Is_Member(circle_rid, user_rid)
                if (write_on_db):
                    result = myDao.set_member(ismember)
                    print("CREATE:", str(result[0]))
                else:
                    print("TO_CREATE: " + ismember.inV + "- users: " + ismember.outV)
            else:
                print("is_member Already Exist. Circle:" + circle_rid + " User: " + user_rid + " id:" + id)
        return ismember

    def create_ismembers(self, post=".txt"):
        global create
        ismember_tags = dict()
        all_tags = dict()
        in_directory = "../resources/meetup/"
        in_filename = "all_is_member" + post
        fileManager = FileManager()
        fileManager.new_in(in_directory, in_filename)

        myFile = fileManager.readFile()
        for line in myFile[0:-2]:
            users = list()
            # print(line)
            words = line.split('\t')
            circle_rid = ""
            circle_rid += words[0].lower().strip()
            length = len(words)
            for i in range(1, length):
                user_rid = words[i].lower().strip().replace('"', '')
                users.append(user_rid)
                # print("error adding user_rid to circle: ", user_rid)
            if (create):
                ismember = self.create_ismember(circle_rid, users)


create = True
write_on_db = True

if __name__ == "__main__":
    app = IsMemberImporter()
    app.create_ismembers()
