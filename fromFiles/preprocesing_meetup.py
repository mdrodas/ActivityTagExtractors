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
from fromFiles.new_users_meetup import new_users_meetup
from fromFiles.new_circles_meetup import new_circles_meetup
from fromFiles.new_memberships_meetup import new_memberships_meetup

if __name__ == "__main__":
    post_id = "10.txt"
    print("Starting Preprocesing...")
    circles = new_circles_meetup()
    circles.preprocessing_circles(post_id)
    print("Circles FINISHED.")
    users = new_users_meetup()
    users.preprocessing_UserProfile(post_id)
    print("UserProfiles FINISHED.")
    members = new_memberships_meetup()
    members.preprocessing_is_member(post_id)
    print("Is_Member FINISHED.")
