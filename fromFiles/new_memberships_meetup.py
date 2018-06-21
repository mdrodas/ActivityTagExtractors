"""
Implementation for new tags extractor (meetup) using a list of files.
"""
import operator
import datetime
from util.FileManager import FileManager
from DAO.CircleDao import CircleDao
from DAO.UserProfileDao import UserProfileDao
from DAO.TenantDao import TenantDao
from model.UserProfile import UserProfile
from model.Address import Address
from model.ContactInfo import ContactInfo
from model.Person import Person
from model.Profession import Profession


class new_memberships_meetup:

    def build_user(self, screenname, tags):
        tenantdao = TenantDao()
        tenancy = tenantdao.getByName("Trento")
        if (tenancy):
            userprofile = UserProfile(screenname, tenancy[0].rid)
            profession = Profession("")
            userprofile.profession = profession.toDict()
            address = Address("")
            userprofile.address = address.toDict()
            person = Person(screenname, screenname + "_family", "2000-01-01")
            userprofile.person = person.toDict()
            contact = ContactInfo("")
            userprofile.contactinfo = contact.toDict()
            userprofile.add_preferences(tags)
        else:
            raise ValueError('The Tenancy for Trento do not exist.')

        return userprofile

    def all_users_frequency(self, fileManager, all_tags):
        freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
        uniqueTagsLen = "Amount of unique Circles:" + str(len(freq_sorted2))
        print(uniqueTagsLen)
        fileManager.writeFile(uniqueTagsLen)

        # print("Results 02: Tag == frequency_used")
        for key, value in freq_sorted2:
            keyValue = key + "=" + str(value)
            # print(keyValue)
            fileManager.writeFile(keyValue)

    def print_circle_members(self, fileManager):
        # print("Results 01: Members. circle_id - user_id_1 user_id_2 user_id_n")
        i = 0
        size = 0
        global circle_members
        global all_users

        for circle_id, members in circle_members.items():
            i += 1
            size += len(members)

            outLine = [str(circle_id)]
            outLine_freq = dict()
            for user_id in members:
                outLine.append(user_id)
                # outLine_freq[user_id] = all_users[user_id]

            # freq_sorted = sorted(outLine_freq.items(), key=operator.itemgetter(1), reverse=True)
            if (i % 1) == 0:
                toPrint = "IM-" + str(i) + "=" + str(circle_id) + "-" + str(len(members))
                print(toPrint)

            toPrint2 = "\t".join(outLine)
            # print(toPrint2)
            fileManager.writeFile(toPrint2)

        if (i > 0):
            average1 = "Average users per circle:" + str(size / i)
            print(average1)
            fileManager.writeFile(average1)
        else:
            print("PROBLEMS: " + size)

    # "","gmemid","member","chapterId","membershipURL","memid","name","role","url"
    def process_line(self, line):
        fields = line.split(',\"')
        circle_name = fields[6].lower().strip().replace('"', '').replace('\\', '\\\\')
        user_id = fields[5].lower().strip().replace('"', '')
        user_name = fields[2].lower().strip().replace('"', '')
        return (user_id, user_name, circle_name)

    def user_count(self, user_id):
        global all_users
        if (user_id in all_users):
            all_users[user_id] += 1
        else:
            all_users[user_id] = 1

    def is_member(self, user_name, circle_name):
        userdao = UserProfileDao()
        circledao = CircleDao()
        user = userdao.getByScreenname(user_name)
        circle = circledao.getByName(circle_name)
        response = ("", "")
        if (user and circle):
            user_rid = user[0].rid
            circle_rid = circle[0].rid
            if (user_rid and circle_rid):
                response = (user_rid, circle_rid)
        return response

    def process_is_member(self, user_name, circle_name):
        global circle_members
        ismember = self.is_member(user_name, circle_name)
        if (ismember[0] and ismember[1]):
            user_id = ismember[0]
            circle_id = ismember[1]
            print("great! circle:" + circle_id + "- user:" + user_id)
            if (circle_id not in circle_members):
                circle_members[circle_id] = [user_id]
            else:
                if (user_id not in circle_members[circle_id]):
                    circle_members[circle_id].append(user_id)
        # else:
        # print("Something is wrong: " + str(ismember))

    def save_new(self, user_id, circle_name):
        out_directory = "../resources/meetup/"
        new_members_tags = "new_members.communities4.txt"
        fileManager = FileManager()
        fileManager.new_out(out_directory, new_members_tags)
        fileManager.writeFile("\t".join([user_id, circle_name]))

    def preprocessing_is_member(self, post="2.txt"):

        # new_members_tags = "new_members.communities" + post
        members_tags = "members.communities.csv"
        clean_circles_tags = "all_is_member" + post
        is_member_frequency = "is_member_frequency" + post
        in_directory = "../resources/dataset-meetup/"
        out_directory = "../resources/meetup/"

        fileManager = FileManager(in_directory)
        fileManager.new_in(in_directory, members_tags)
        fileManager.new_out(out_directory, clean_circles_tags)
        myFile = fileManager.readFile(True, "utf-8")
        i = 0
        for line in myFile:
            line2 = self.process_line(line)
            user_id = line2[0]
            user_name = line2[1]
            circle_name = line2[2]

            if (user_id == 'memid' or not user_id or not circle_name):
                # save_new(user_id, circle_name)
                continue

            self.user_count("mup_" + user_id)
            self.process_is_member("mup_" + user_id, circle_name)

        self.print_circle_members(fileManager)

        fileManager.new_out(out_directory, is_member_frequency)
        self.all_users_frequency(fileManager, all_users)


circle_members = dict()
all_users = dict()

if __name__ == "__main__":
    post_id = "10.txt"
    t1 = datetime.datetime.now()
    print("Is_Member BEGIN.")
    members = new_memberships_meetup()
    members.preprocessing_is_member(post_id)
    t2 = datetime.datetime.now()
    print("Is_Member FINISHED.")
    time1 = t2 - t1
    print("Time Is_Member: " + str(time1))
