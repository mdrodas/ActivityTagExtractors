"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import operator
from util.FileManager import FileManager


def all_tags_frequency(fileManager, all_tags):
    freq_sorted2 = sorted(all_tags.items(), key=operator.itemgetter(1), reverse=True)
    uniqueTagsLen = "Amount of unique tags:" + str(len(freq_sorted2))
    print(uniqueTagsLen)
    fileManager.writeFile(uniqueTagsLen)

    print("Results 02: Tag == frequency_used")
    for key, value in freq_sorted2:
        keyValue = key + "=" + str(value)
        # print(keyValue)
        fileManager.writeFile(keyValue)


def print_circles_tags(fileManager):
    print("Results 01: Circles. circle - tag_1 tag_2 tag_n")
    i = 0
    size = 0
    global circles_tags

    for key, value in circles_tags.items():
        freq_sorted = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        i += 1
        size += len(freq_sorted)
        toPrint = str(key) + "-" + str(len(freq_sorted)) + "== " + str(freq_sorted)
        print(toPrint)

        outLine = [str(key)]
        for value2 in freq_sorted:
            outLine.append(value2[0])

        toPrint2 = "\t".join(outLine)
        # print(toPrint2)
        fileManager.writeFile(toPrint2)

    average1 = "Average tags per circle:" + str(size / i)
    print(average1)
    fileManager.writeFile(average1)


def process_line(line):
    circle_tag = line.split(',\"')
    circle_name = circle_tag[4].lower().strip()
    circle_name = circle_name.replace('"', '')
    tag = circle_tag[2].lower().strip()
    tag = tag.replace('"','')
    tag = tag.replace('-', '_')
    tag = tag.replace(' ', '_')
    return (circle_name, tag)


def tag_count(tag):
    global all_tags
    if (tag in all_tags):
        all_tags[tag] += 1
    else:
        all_tags[tag] = 1


def process_circle_tags(circle_name, tag):
    global circles_tags
    freq = dict()
    freq[tag] = 1;
    if (circle_name not in circles_tags):
        circles_tags[circle_name] = freq
    else:
        freq2 = circles_tags[circle_name]
        if (tag in freq2):
            freq2[tag] += 1
        else:
            freq2[tag] = 1
        circles_tags[circle_name] = freq2


if __name__ == "__main__":
    circles_tags = dict()
    all_tags = dict()

    members_tags = "communities.tags.csv"
    clean_circles_tags = "all_circles_tags.txt"
    tags_frequency = "circle_tags_frequency.txt"
    in_directory = "../resources/dataset-meetup/"
    out_directory = "../resources/meetup/"

    fileManager = FileManager(in_directory)
    fileManager.new_in(in_directory, members_tags)
    fileManager.new_out(out_directory, clean_circles_tags)
    myFile = fileManager.readFile()

    for line in myFile:
        line2 = process_line(line)
        circle_name = line2[0]
        tag = line2[1]
        if (circle_name == 'community'):
            continue

        tag_count(tag)
        process_circle_tags(circle_name, tag)

    print_circles_tags(fileManager)

    fileManager.new_out(out_directory, tags_frequency)
    all_tags_frequency(fileManager, all_tags)
