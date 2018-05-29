from util.FileManager import FileManager
from model.Circle import Circle
from model.Address import Address
from model.ContactInfo import ContactInfo
from model.Person import Person
from model.Profession import Profession
from model.Tag import Tag
from DAO.CircleDao import CircleDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao


def build_circle(name, tags):
    tenantdao = TenantDao()
    tenancy = tenantdao.getByName("Trento")
    if (tenancy):
        circle = Circle(name, tenancy[0].rid)
        profession = Profession("")
        circle.profession = profession.toDict()
        address = Address("")
        circle.address = address.toDict()
        person = Person(name, name + "_family", "1900-01-01")
        circle.person = person.toDict()
        contact = ContactInfo("")
        circle.contactinfo = contact.toDict()
        circle.add_preferences(tags)
    else:
        raise ValueError('The Tenancy for Trento do not exist.')

    return circle


def create_circle(name, tags):
    global write_on_db
    circle = build_circle(name, tags)

    myDao = CircleDao()
    id = myDao.exist(name)
    if (not id):
        if (write_on_db):
            result = myDao.add(circle)
            print("CREATE:", str(result[0]))
        else:
            print("TO_CREATE: " + circle.name + "- tags: " + str(list(circle.preferences)))
    else:
        circle.rid = id
        print("Circle Already Exist. Name:" + name + " ID:" + id)
    return circle


def update_circle(name, tags):
    circle = build_circle(name, tags)
    myDao = CircleDao()
    id = myDao.exist(name)
    circle.rid = id
    result = myDao.update(circle)
    print("Update: ", result[0])
    return circle


def circle_hastag(circle_id, tag_id):
    myDao = CircleDao()
    result = myDao.has_tag(circle_id, tag_id)
    return result


def create_tag(taglabel):
    global write_on_db
    tagDao = TagDao()
    id = tagDao.exist(taglabel)
    if (not id):
        tag = Tag(taglabel, "description_" + taglabel, "", "meetup_2", "en", list(), list())
        if (write_on_db):
            new_tag = tagDao.add(tag)
            # print(newTag)
            id = new_tag[0].rid
        else:
            id = taglabel
    return id


def create_circles(create):
    circle_tags = dict()
    all_tags = dict()
    in_directory = "../resources/meetup/"
    if (create):
        in_filename = "all_circles_tags.txt"
    else:
        in_filename = "all_circles_tags.txt"
    fileManager = FileManager()
    fileManager.new_in(in_directory, in_filename)

    myFile = fileManager.readFile()
    for line in myFile[0:-2]:

        tags = list()
        # print(line)
        words = line.split('\t')
        name = ""
        name += words[0].lower().strip()
        length = len(words)
        for i in range(1, length):
            tag = words[i].lower().strip()
            id = create_tag(tag.replace('"', ''))
            if (id):
                tags.append(id)
            else:
                print("error creating tag: ", tag)
        if (create):
            circle = create_circle(name, tags)
        else:
            circle = update_circle(name, tags)


if __name__ == "__main__":
    create = True
    write_on_db = False
    create_circles(create)
