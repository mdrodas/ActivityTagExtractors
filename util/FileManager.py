import os


class FileManager:
    resources = "../resources/"
    tagsOnly = resources + "tagsOnly/"

    def readTagsOnly(self, filename):
        response = []
        with open(FileManager.tagsOnly + filename) as fp:
            for line in fp:
                response.append(line.lower().strip('\n'))
        return response

    def readResource(self, filename):
        response = []
        with open(FileManager.resources + filename) as fp:
            for line in fp:
                response.append(line.lower().strip('\n'))
        return response

    def writeProcessResources(self, outfilename, value):
        fp = open(FileManager.resources + outfilename, "a+")
        fp.write(value + "\n")
        fp.close()

    def writeResources(self):
        for root, dirs, files in os.walk(FileManager.tagsOnly, topdown=False):
            for inFileName in files:
                FileManager.unifyResources(inFileName, "allTags.txt")

    def unifyResources(infilename, outfilename):
        fp = open(FileManager.resources + outfilename, "a+")
        myFile = FileManager.readResource(infilename)
        toWrite = '\n'.join(myFile[1:]) + "\n"
        fp.write(toWrite)
        fp.close()
