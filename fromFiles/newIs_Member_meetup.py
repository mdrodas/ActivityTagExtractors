"""
Implementation for new tags extractor (meetup) using a list of files.
"""
import operator
from util.FileManager import FileManager
from DAO.CircleDao import CircleDao
from DAO.UserProfileDao import UserProfileDao


def all_users_frequency(fileManager, all_tags):
    freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
    uniqueTagsLen = "Amount of unique tags:" + str(len(freq_sorted2))
    print(uniqueTagsLen)
    fileManager.writeFile(uniqueTagsLen)

    print("Results 02: Tag == frequency_used")
    for key, value in freq_sorted2:
        keyValue = key + "=" + str(value)
        # print(keyValue)
        fileManager.writeFile(keyValue)


def print_circle_members(fileManager):
    print("Results 01: Members. circle_id - user_id_1 user_id_2 user_id_n")
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
            outLine_freq[user_id] = all_users[user_id]

        freq_sorted = sorted(outLine_freq.items(), key=operator.itemgetter(1), reverse=True)
        toPrint = str(circle_id) + "-" + str(len(members)) + "== " + str(freq_sorted)
        print(toPrint)

        toPrint2 = "\t".join(outLine)
        # print(toPrint2)
        fileManager.writeFile(toPrint2)

    average1 = "Average tags per circle:" + str(size / i)
    print(average1)
    fileManager.writeFile(average1)


# "","gmemid","member","chapterId","membershipURL","memid","name","role","url"
def process_line(line):
    fields = line.split(',\"')
    circle_name = fields[6].lower().strip().replace('"', '')
    user_id = fields[5].lower().strip().replace('"', '')
    user_name = fields[2].lower().strip().replace('"', '')
    return (user_id, user_name, circle_name)


def user_count(user_id):
    global all_users
    if (user_id in all_users):
        all_users[user_id] += 1
    else:
        all_users[user_id] = 1


def is_member(user_name, circle_name):
    userdao = UserProfileDao()
    circledao = CircleDao()
    user = userdao.getByScreenname(user_name)
    circle = circledao.getByName(circle_name)
    #print("what? "+str(user_name)+"--"+str(circle_name))
    response = ("", "")
    if (user):
        user_rid = user[0].rid
        if (circle):
            circle_rid = circle[0].rid
            if (user_rid and circle_rid):
                members = circledao.get_members(circle_rid)
                for member in members:
                    if (user_rid == member.rid):
                        response = (user_rid, circle_rid)
                        break
    return response


def process_is_member(user_name, circle_name):
    global circle_members
    ismember = is_member(user_name, circle_name)
    if (ismember[0]):
        user_id = ismember[0]
        circle_id = ismember[1]
        if (circle_id not in circle_members):
            circle_members[circle_id] = [user_id]
        else:
            if (user_id not in circle_members[circle_id]):
                circle_members[circle_id].append(user_id)
    #else:
        # print("Something is wrong: " + str(ismember))


if __name__ == "__main__":
    circle_members = list()
    all_users = dict()

    members_tags = "members.communities.csv"
    clean_circles_tags = "all_is_member_tags.txt"
    is_member_frequency = "is_member_frequency.txt"
    in_directory = "../resources/dataset-meetup/"
    out_directory = "../resources/meetup/"

    fileManager = FileManager(in_directory)
    fileManager.new_in(in_directory, members_tags)
    fileManager.new_out(out_directory, clean_circles_tags)
    myFile = fileManager.readFile()
    i =0
    for line in myFile:
        line2 = process_line(line)
        user_id = line2[0]
        user_name = line2[1]
        circle_name = line2[2]

        if (user_id == 'memid' or not user_id or not circle_name):
            continue

        user_count(user_id)
        process_is_member(user_id, circle_name)

    print_circle_members(fileManager)

    fileManager.new_out(out_directory, is_member_frequency)
    all_users_frequency(fileManager, all_users)
