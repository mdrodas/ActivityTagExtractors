import operator
import datetime
from util.FileManager import FileManager
from model.UserProfile import UserProfile
from model.Address import Address
from model.ContactInfo import ContactInfo
from model.Person import Person
from model.Profession import Profession
from model.Tag import Tag
from DAO.UserProfileDao import UserProfileDao
from DAO.CircleDao import CircleDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao


class UserProfileImporter:

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

    def create_user(self, screenname, tags):
        global write_on_db
        user = self.build_user(screenname, tags)

        myDao = UserProfileDao()
        id = myDao.exist(screenname)
        if (not id):
            if (write_on_db):
                result = myDao.add(user)
                print("CREATE: ", str(result[0].screenname + "- tags: " + str(list(result[0].preferences))))
            else:
                print("TO_CREATE: " + user.screenname + "- tags: " + str(list(user.preferences)))
        else:
            user.rid = id
            print("UserProfile Already Exist. Name:" + screenname + " ID:" + id)
        return user

    def update_user(self, screenname, tags):
        user = self.build_user(screenname, tags)
        myDao = UserProfileDao()
        id = myDao.exist(screenname)
        user.rid = id
        result = myDao.update(user)
        print("Update: ", result[0])
        return user

    def user_hastag(self, user_id, tag_id):
        myDao = UserProfileDao()
        result = myDao.has_tag(user_id, tag_id)
        return result

    def create_tag(self, taglabel):
        global write_on_db
        tagDao = TagDao()
        id = tagDao.exist(taglabel)
        if (not id and taglabel):
            tag = Tag(taglabel, "description_" + taglabel, "", "meetup_1", "en", list(), list())
            if (write_on_db):
                new_tag = tagDao.add(tag)
                # print(newTag)
                id = new_tag[0].rid
            else:
                id = taglabel
        return id

    def check_user(self):
        groupname = "60+ happy hour"
        in_directory = "../resources/meetup/"
        in_filename = "all_users_tags.txt"
        myDao = UserProfileDao()
        tagDao = TagDao()
        all_users = myDao.getAll()
        tags = dict()
        for user in all_users:
            for tag in user.preferences:
                real_tag = tagDao.getById(tag)[0].label
                if real_tag in tags:
                    tags[real_tag] += 1;
                else:
                    tags[real_tag] = 1
        return tags

    def check_circle(self):
        groupname = "60+ happy hour"
        in_directory = "../resources/meetup/"
        in_filename = "all_users_tags.txt"
        myDao = CircleDao()
        tagDao = TagDao()
        all_circles = myDao.getAll()
        tags = dict()
        for circle in all_circles:
            for tag in circle.tags:
                real_tag = tagDao.getById(tag)[0].label
                if real_tag in tags:
                    tags[real_tag] += 1;
                else:
                    tags[real_tag] = 1
        return tags

    def check_all(self):
        tags_users = self.check_user()
        tags_circles = self.check_circle()
        print("USERS TAGS " + str(len(tags_users)))
        tags_users2 = sorted(tags_users.items(), key=operator.itemgetter(1), reverse=True)
        tags_circles2 = sorted(tags_circles.items(), key=operator.itemgetter(1), reverse=True)
        for key, value in tags_users2:
            print("K: " + key + " V: " + str(value))

        print("CIRCLES TAGS " + str(len(tags_circles)))
        for key, value in tags_circles2:
            print("K: " + key + " V: " + str(value))

    def check_circle_users(self):
        myDao = CircleDao()
        tagDao = TagDao()
        all_circles = myDao.getAll()

        for circle in all_circles:
            circle_rid = circle.rid
            is_members = dict()
            for circle_tag in circle.tags:
                users = myDao.get_members(circle_rid)
                c = 0
                # print(str(len(users)))
                for user in users:
                    user_rid = user.rid
                    user_tags = user.preferences
                    # print(str(len(user_tags)))
                    # print (str(circle_tag)+"=="+str(user_tags))
                    for user_tag in user_tags:
                        if str(circle_tag) == str(user_tag):
                            # real_tag = tagDao.getById(tag)[0].label
                            print("circle: " + circle_rid + " user: " + user_rid)
                            ismember = myDao.get_is_member(circle_rid, user_rid)
                            ismember[0].rank += 1.0
                            myDao.update_is_member(ismember[0])
                            break

    def print_circle_users_membership(self):
        myDao = CircleDao()
        tagDao = TagDao()
        all_circles = myDao.getAll()
        cicles_len = len(all_circles)
        base = 0
        all_percentage = 0
        all_circle_size = 0
        min_circle = ""
        min_percentage = 0
        max_circle = ""
        max_percentage = 0

        for circle in all_circles:
            circle_rid = circle.rid
            circle_tags_len = len(circle.tags)
            users = myDao.get_members(circle_rid)
            users_len = len(users)
            base = circle_tags_len * users_len
            all_circle_size += users_len
            rank = 0.0
            for user in users:
                user_rid = user.rid
                # real_tag = tagDao.getById(tag)[0].label
                ismember = myDao.get_is_member(circle_rid, user_rid)
                rank += ismember[0].rank
            if (base == 0.0):
                percentage = 0
            else:
                percentage = rank / base * 100

            if not min_circle:
                min_circle = circle.name
                min_percentage = percentage

            if min_percentage > percentage:
                min_percentage = percentage
                min_circle = circle.name

            if not max_circle:
                max_circle = circle.name
                max_percentage = percentage

            if max_percentage < percentage:
                max_percentage = percentage
                max_circle = circle.name

            print("rid, circle_size, percentage_overlap_tags")
            print("circle: " + circle.rid + "(" + str(users_len) + ") percentage: " + str(percentage))
            all_percentage += percentage
        print("Average User-Circle-Tags Overlapping : " + str(all_percentage / cicles_len))
        print("Min Circle Percentage: " + str(min_percentage) + " Circle:" + min_circle)
        print("Max Circle Percentage: " + str(max_percentage) + " Circle:" + max_circle)
        print("Average circle size: " + str(all_circle_size / cicles_len))

    def create_users(self, post=".txt"):
        global create
        user_tags = dict()
        all_tags = dict()
        in_directory = "../resources/meetup/"
        if (create):
            in_filename = "all_users_tags" + post
        else:
            in_filename = "all_users_tags" + post
        fileManager = FileManager()
        fileManager.new_in(in_directory, in_filename)

        myFile = fileManager.readFile()
        for line in myFile[0:-2]:

            tags = list()
            # print(line)
            words = line.split('\t')
            screenname = "mup_"
            name = words[0].lower().strip()
            screenname += name
            length = len(words)
            for i in range(1, length):
                tag = words[i].lower().strip().replace('"', '')
                id = self.create_tag(tag)
                if (id):
                    tags.append(id)
                else:
                    print("error creating tag: ", tag)
            if (create):
                user = self.create_user(screenname, tags)
            else:
                user = self.update_user(screenname, tags)


create = True
write_on_db = True

if __name__ == "__main__":
    app = UserProfileImporter()
    # app.create_users()
    # app.check_all()
    # app.check_circle_users()
    app.print_circle_users_membership()
