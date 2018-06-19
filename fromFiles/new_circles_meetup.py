"""
Implementation for new tags extractor (meetup) using a list of files.
"""
import operator
from util.FileManager import FileManager


class new_circles_meetup:

    def all_tags_frequency(self, fileManager, all_tags):
        freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
        uniqueTagsLen = "Amount of unique tags:" + str(len(freq_sorted2))
        print(uniqueTagsLen)
        fileManager.writeFile(uniqueTagsLen)

        print("Results 02: Tag == frequency_used")
        for key, value in freq_sorted2:
            keyValue = key + "=" + str(value)
            # print(keyValue)
            fileManager.writeFile(keyValue)

    def print_circles_tags(self, fileManager):
        print("Results 01: Circles. circle - tag_1 tag_2 tag_n")
        i = 0
        size = 0
        global circles_tags
        global all_tags

        for circle_name, circle_tags in circles_tags.items():
            i += 1
            size += len(circle_tags)

            outLine = [str(circle_name)]
            outLine_freq = dict()
            for tag in circle_tags:
                outLine.append(tag)
                outLine_freq[tag] = all_tags[tag]

            freq_sorted = sorted(outLine_freq.items(), key=operator.itemgetter(1), reverse=True)
            toPrint = "C- " + str(circle_name) + "-" + str(len(circle_tags)) + "== " + str(freq_sorted)
            print(toPrint)

            toPrint2 = "\t".join(outLine)
            # print(toPrint2)
            fileManager.writeFile(toPrint2)

        average1 = "Average tags per circle:" + str(size / i)
        print(average1)
        fileManager.writeFile(average1)

    def process_line(self, line):
        circle_tag = line.split(',\"')
        circle_name = circle_tag[4].lower().strip()
        circle_name = circle_name.replace('"', '')
        tag = circle_tag[2].lower().strip()
        tag = tag.replace('"', '')
        tag = tag.replace('-', '_')
        tag = tag.replace(' ', '_')
        return (circle_name, tag)

    def tag_count(self, tag):
        global all_tags
        if (tag in all_tags):
            all_tags[tag] += 1
        else:
            all_tags[tag] = 1

    def process_circle_tags(self, circle_name, tag):
        global circles_tags
        # freq = dict()
        # freq[tag] = 1;
        if (circle_name not in circles_tags):
            circles_tags[circle_name] = [tag]
        else:
            if (tag not in circles_tags[circle_name]):
                circles_tags[circle_name].append(tag)

    def preprocessing_circles(self, post="2.txt"):

        members_tags = "communities.tags.csv"
        clean_circles_tags = "all_circles_tags" + post
        tags_frequency = "circles_tags_frequency" + post
        in_directory = "../resources/dataset-meetup/"
        out_directory = "../resources/meetup/"

        fileManager = FileManager(in_directory)
        fileManager.new_in(in_directory, members_tags)
        fileManager.new_out(out_directory, clean_circles_tags)
        myFile = fileManager.readFile('utf-8')

        for line in myFile:
            line2 = self.process_line(line)
            circle_name = line2[0]
            tag = line2[1]
            if (circle_name == 'community'):
                continue

            self.tag_count(tag)
            self.process_circle_tags(circle_name, tag)

        self.print_circles_tags(fileManager)

        fileManager.new_out(out_directory, tags_frequency)
        self.all_tags_frequency(fileManager, all_tags)


circles_tags = dict()
all_tags = dict()
if __name__ == "__main__":
    new_circles_meetup.preprocessing_circles()
