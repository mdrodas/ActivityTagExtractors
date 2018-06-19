"""
Main function that process the meetup extracted data to Orientdb.

Process:
- New Circles (and Tags).
- New Users (and Tags).
- New Memberships (relation between Circles and Users)

Input:
- all_circles_tags+'post_id'
- all_users_tags+'post_id'
- all_is_member+'post_id'

Output:
- New Circle Vertex in OrientDB.
- New UserProfile Vertex in OrientDB.
- New IS_MEMBER Edge in OrientDB.
- New Tags Vertex in OrientDB.

"""
import datetime
from service.UserProfileImporter import UserProfileImporter
from service.CircleImporter import CircleImporter
from service.IsMemberImporter import IsMemberImporter

if __name__ == "__main__":
    post_id = "10.txt"
    t1 = datetime.datetime.now()
    print("Starting Procesing...")
    circles = CircleImporter()
    circles.create_circles(post_id)
    t2 = datetime.datetime.now()
    time1 = t2 - t1
    print("Time Circles: " + str(time1))
    print("Circles FINISHED.")
    users = UserProfileImporter()
    users.create_users(post_id)
    t3 = datetime.datetime.now()
    time2 = t3 - t2
    print("Time Users: " + str(time2))
    print("UserProfiles FINISHED.")
    members = IsMemberImporter()
    members.create_ismembers(post_id)
    t4 = datetime.datetime.now()
    time3 = t4 - t3
    print("Time Is_Member: " + str(time3))
    print("Is_Member FINISHED.")
