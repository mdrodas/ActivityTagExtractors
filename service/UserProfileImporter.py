from util.FileManager import FileManager
from model.UserProfile import UserProfile
from model.Address import Address
from model.ContactInfo import ContactInfo
from model.Person import Person
from model.Profession import Profession
from model.Tag import Tag
from DAO.UserProfileDao import UserProfileDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao


def build_user(screenname, tags):
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


def create_user(screenname, tags):
    global write_on_db
    user = build_user(screenname, tags)

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


def update_user(screenname, tags):
    user = build_user(screenname, tags)
    myDao = UserProfileDao()
    id = myDao.exist(screenname)
    user.rid = id
    result = myDao.update(user)
    print("Update: ", result[0])
    return user


def user_hastag(user_id, tag_id):
    myDao = UserProfileDao()
    result = myDao.has_tag(user_id, tag_id)
    return result


def create_tag(taglabel):
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

def check_user(name):
    groupname = "60+ happy hour"
    in_directory = "../resources/meetup/"
    in_filename = "all_users_tags.txt"
    print()

def create_users(create):
    user_tags = dict()
    all_tags = dict()
    in_directory = "../resources/meetup/"
    if (create):
        in_filename = "all_users_tags.txt"
    else:
        in_filename = "all_users_tags.txt"
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
            id = create_tag(tag)
            if (id):
                tags.append(id)
            else:
                print("error creating tag: ", tag)
        if (create):
            user = create_user(screenname, tags)
        else:
            user = update_user(screenname, tags)


if __name__ == "__main__":
    create = True
    write_on_db = True
    create_users(create)
