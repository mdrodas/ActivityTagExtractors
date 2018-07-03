from util.FileManager import FileManager
from model.Circle import Circle
from model.Tag import Tag
from DAO.CircleDao import CircleDao
from DAO.TagDao import TagDao
from DAO.TenantDao import TenantDao
from util.KnowledgeBase import KnowledgeBase


class CircleImporter:

    def __init__(self):
        self.kb = KnowledgeBase()

    def build_circle(self, name, tags):
        tenantdao = TenantDao(self.kb)
        tenancy = tenantdao.getByName("Trento")
        if (tenancy):
            circle = Circle(name, tenancy[0].rid)
            circle.add_tags(tags)
        else:
            raise ValueError('The Tenancy for Trento do not exist.')

        return circle

    def create_circle(self, id, name, tags):
        global write_on_db
        circle = Circle(name, "")

        if (not id):
            if (write_on_db):
                circle = self.build_circle(name, tags)
                myDao = CircleDao(self.kb)
                result = myDao.add(circle)
                print("CREATE:", str(result[0]))
            else:
                print("TO_CREATE: " + name + "- tags: " + str(list(tags)))
        else:
            circle.rid = id
            print("Circle Already Exist. Name:" + name + " ID:" + id)
        return circle

    def update_circle(self, name, tags):
        circle = self.build_circle(name, tags)
        myDao = CircleDao(self.kb)
        id = myDao.exist(name)
        circle.rid = id
        result = myDao.update(circle)
        print("Update: ", result[0])
        return circle

    def circle_hastag(self, circle_id, tag_id):
        myDao = CircleDao(self.kb)
        result = myDao.has_tag(circle_id, tag_id)
        return result

    def create_tag(self, taglabel):
        global write_on_db
        tagDao = TagDao(self.kb)
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

    def create_circles(self, post=".txt"):
        global create
        circle_tags = dict()
        all_tags = dict()
        in_directory = "../resources/meetup/"
        if (create):
            in_filename = "all_circles_tags" + post
        else:
            in_filename = "all_circles_tags" + post
        fileManager = FileManager()
        fileManager.new_in(in_directory, in_filename)

        myFile = fileManager.readFile(True, 'cp1250')
        for line in myFile[0:-2]:

            tags = list()
            # print(line)
            words = line.split('\t')
            name = ""
            name += words[0].lower().strip()

            myDao = CircleDao(self.kb)
            id = myDao.exist(name)
            if (id):
                continue

            length = len(words)
            for i in range(1, length):
                tag = words[i].lower().strip()
                id = self.create_tag(tag.replace('"', ''))
                if (id):
                    tags.append(id)
                else:
                    print("error creating tag: ", tag)
            if (create):
                circle = self.create_circle(id, name, tags)
            else:
                circle = self.update_circle(name, tags)


create = True
write_on_db = True

if __name__ == "__main__":
    ap = CircleImporter()
    ap.create_circles()
