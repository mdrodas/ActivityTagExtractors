import operator
import datetime
from util.FileManager import FileManager
from util.KnowledgeBase import KnowledgeBase
from model.Tag import Tag
from DAO.TagDao import TagDao


class TagsImporter:

    def __init__(self, DBName = "framework_test10"):
        self.kb = KnowledgeBase(DBName)

    def create_tag(self, taglabel):
        t0 = datetime.datetime.now()
        global write_on_db
        tagDao = TagDao(self.kb)
        t1 = datetime.datetime.now()
        #print("time (init) create tag: " + (str(t1 - t0)))
        id = tagDao.exist(taglabel)
        t2 = datetime.datetime.now()
        #print("time (exist) create tag: " + (str(t2 - t1)))
        if (not id and taglabel):
            tag = Tag(taglabel, "description_" + taglabel, "", "meetup_1", "en", list(), list())
            if (write_on_db):
                new_tag = tagDao.add(tag)
                id = new_tag[0].rid
            else:
                id = taglabel
        t3 = datetime.datetime.now()
        #print("time (add) create tag: " + (str(t3 - t2)))
        return id

    def create_tags(self, post="10.txt"):
        user_tags = dict()
        all_tags = dict()

        in_directory = "../resources/meetup/"
        in_filename = "users_tags_frequency" + post
        fileManager = FileManager()
        fileManager.new_in(in_directory, in_filename)

        myFile = fileManager.readFile()
        for line in myFile[1:-1]:
            tags = list()
            # print(line)
            words = line.split('=')
            label = words[0].lower().strip()

            t1 = datetime.datetime.now()
            id = self.create_tag(label)
            t2 = datetime.datetime.now()
            print("3. time create tag: (label:" + label + ") " + (str(t2 - t1)))


write_on_db = True

if __name__ == "__main__":
    post = "10.txt"

    app = TagsImporter()
    app.create_tags(post)
