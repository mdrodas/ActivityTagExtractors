"""
Main function that preprocess the meetup extracted data to some more appropriated files for Orientdb.

Process:
- New Circles (and Tags).
- New Users (and Tags).
- New Memberships (relation between Circles and Users)

Output:
- all_circles_tags+'post_id'
- all_users_tags+'post_id'
- all_is_member+'post_id'
- circles_tags_frequency+'post_id'
- users_tags_frequency+'post_id'
- is_member_frequency+'post_id'

"""
import datetime
from fromFiles.new_users_meetup import new_users_meetup
from fromFiles.new_circles_meetup import new_circles_meetup
from fromFiles.new_memberships_meetup import new_memberships_meetup

if __name__ == "__main__":
    post_id = "10.txt"
    t1 = datetime.datetime.now()
    print("Starting Preprocesing...")
    circles = new_circles_meetup()
    circles.preprocessing_circles(post_id)
    t2 = datetime.datetime.now()
    time1 = t2 - t1
    print("Time Circles: " + str(time1))
    print("Circles FINISHED.")
    users = new_users_meetup()
    users.preprocessing_UserProfile(post_id)
    t3 = datetime.datetime.now()
    time2 = t3 - t2
    print("Time Users: " + str(time2))
    print("UserProfiles FINISHED.")
    members = new_memberships_meetup()
    members.preprocessing_is_member(post_id)
    t4 = datetime.datetime.now()
    print("Is_Member FINISHED.")
    time3 = t4 - t3
    print("Time Is_Member: " + str(time3))
