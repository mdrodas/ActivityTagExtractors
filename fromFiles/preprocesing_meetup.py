from fromFiles.new_users_meetup import new_users_meetup
from fromFiles.new_circles_meetup import new_circles_meetup
from fromFiles.new_memberships_meetup import new_memberships_meetup

if __name__ == "__main__":
    post_id = "3.txt"
    print("Starting Preprocesing...")
    new_circles_meetup.preprocessing_circles(post_id)
    print("Circles FINISHED.")
    new_users_meetup.preprocessing_UserProfile(post_id)
    print("UserProfiles FINISHED.")
    new_memberships_meetup.preprocessing_is_member(post_id)
    print("Is_Member FINISHED.")
