"""
Implementation for new tags extractor (meetup) using a list of files
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


def print_users_tags(fileManager):
    print("Results 01: UserProfiles. user - tag_1 tag_2 tag_n")
    i = 0
    size = 0
    global users_tags
    global all_tags

    for key, value in users_tags.items():
        # new_value = dict()
        # for key2, value2 in value.items():
        #    new_value[key2] = all_tags[key2]
        # freq_sorted0 = sorted(new_value.items(), key=operator.itemgetter(1), reverse=True)
        # toPrint0 = str(key) + "-" + str(len(freq_sorted0)) + "=2= " + str(freq_sorted0)
        # print(toPrint0)

        freq_sorted = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        i += 1
        size += len(freq_sorted)
        toPrint1 = str(key) + "-" + str(len(freq_sorted)) + "== " + str(freq_sorted)
        print(toPrint1)

        outLine = [str(key)]
        for value2 in freq_sorted:
            outLine.append(value2[0])

        toPrint2 = "\t".join(outLine)
        # print(toPrint2)
        fileManager.writeFile(toPrint2)

    average1 = "Average tags per activity:" + str(size / i)
    print(average1)
    fileManager.writeFile(average1)


def process_line(line):
    member_tag = line.split(',\"')
    user_id = member_tag[2].lower().strip()
    user_id = user_id.replace('"', '')
    tag = member_tag[4].lower().strip()
    tag = tag.replace('"', '')
    tag = tag.replace('-', '_')
    tag = tag.replace(' ', '_')
    return (user_id, tag)


def tag_count(tag):
    global all_tags
    if (tag in all_tags):
        all_tags[tag] += 1
    else:
        all_tags[tag] = 1


def process_user_tags(user_id, tag):
    global users_tags
    freq = dict()
    freq[tag] = 1;
    if (user_id not in users_tags):
        users_tags[user_id] = freq
    else:
        freq2 = users_tags[user_id]
        if (tag in freq2):
            freq2[tag] += 1
        else:
            freq2[tag] = 1
        users_tags[user_id] = freq2


if __name__ == "__main__":
    users_tags = dict()
    all_tags = dict()

    members_tags = "members.tags.csv"
    clean_users_tags = "all_users_tags.txt"
    tags_frequency = "users_tags_frequency.txt"
    in_directory = "../resources/dataset-meetup/"
    out_directory = "../resources/meetup/"
    fileManager = FileManager(in_directory)
    fileManager.new_in(in_directory, members_tags)
    fileManager.new_out(out_directory, clean_users_tags)
    myFile = fileManager.readFile()

    for line in myFile:
        line2 = process_line(line)
        user_id = line2[0]
        tag = line2[1]
        if (user_id == 'memberid'):
            continue

        tag_count(tag)
        process_user_tags(user_id, tag)

    print_users_tags(fileManager)

    fileManager.new_out(out_directory, tags_frequency)
    all_tags_frequency(fileManager, all_tags)
