from util.FileManager import FileManager
from model.Circle import Circle
from model.Is_Member import Is_Member
from model.Tag import Tag
from DAO.CircleDao import CircleDao
from DAO.UserProfileDao import UserProfileDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao


def build_ismember(name, tags):
    tenantdao = TenantDao()
    tenancy = tenantdao.getByName("Trento")
    if (tenancy):
        ismember = Circle(name, tenancy[0].rid)
        ismember.add_tags(tags)
    else:
        raise ValueError('The Tenancy for Trento do not exist.')

    return ismember


def create_ismember(name, tags):
    global write_on_db
    ismember = build_ismember(name, tags)

    myDao = CircleDao()
    id = myDao.exist(name)
    if (not id):
        if (write_on_db):
            result = myDao.add(ismember)
            print("CREATE:", str(result[0]))
        else:
            print("TO_CREATE: " + ismember.name + "- tags: " + str(list(ismember.tags)))
    else:
        ismember.rid = id
        print("Circle Already Exist. Name:" + name + " ID:" + id)
    return ismember


def update_ismember(name, tags):
    ismember = build_ismember(name, tags)
    myDao = CircleDao()
    id = myDao.exist(name)
    ismember.rid = id
    result = myDao.update(ismember)
    print("Update: ", result[0])
    return ismember


def ismember_hastag(ismember_id, tag_id):
    myDao = CircleDao()
    result = myDao.has_tag(ismember_id, tag_id)
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


def create_ismembers(create):
    ismember_tags = dict()
    all_tags = dict()
    in_directory = "../resources/meetup/"
    if (create):
        in_filename = "all_ismembers_tags.txt"
    else:
        in_filename = "all_ismembers_tags.txt"
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
            ismember = create_ismember(name, tags)
        else:
            ismember = update_ismember(name, tags)


if __name__ == "__main__":
    create = True
    write_on_db = True
    create_ismembers(create)
