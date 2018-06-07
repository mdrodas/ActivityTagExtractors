import os


class FileManager:

    def __init__(self, directory="../resources/"):
        filename = "my_file.txt"
        self.new_in(directory, filename)
        self.new_out(directory, filename + ".out")

    def new(self, directory, infilename, outfilename):
        self.new_in(directory, infilename)
        self.new_out(directory, outfilename)

    def new_in(self, directory, infilename):
        self.in_directory = directory
        self.in_filename = infilename
        self.path_in = self.in_directory + self.in_filename

    def new_out(self, directory, outfilename):
        self.out_directory = directory
        self.out_filename = outfilename
        self.path_out = self.out_directory + self.out_filename

    def set_infilename(self, infilename):
        self.in_filename = infilename
        self.path_in = self.in_directory + self.in_filename

    def set_outfilename(self, outfilename):
        self.out_filename = outfilename
        self.path_out = self.out_directory + self.out_filename

    def readFile(self, original = False):
        response = []
        with open(self.path_in, encoding="utf8") as fp:
            for line in fp:
                if (original):
                    response.append(line.strip('\n'))
                else:
                    response.append(line.lower().strip('\n'))
        return response

    def writeFile(self, value, mode="a+"):
        fp = open(self.path_out, mode)
        fp.write(value + "\n")
        fp.close()

    def unify_resources(self, directory):
        allTag_name = "allTags.txt"
        for root, dirs, files in os.walk(directory, topdown=False):
            for inFileName in files:
                FileManager.unify_resource(inFileName, allTag_name)

    def unify_resource(self, infilename, outfilename):
        fr = FileManager()
        fr.new_in(fr.directory, infilename)
        fr.new_out(fr.directory, outfilename)
        myFile = fr.readFile()
        toWrite = '\n'.join(myFile[1:]) + "\n"
        fr.writeFile(toWrite)
