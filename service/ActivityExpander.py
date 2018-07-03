from model.Tag import Tag
from DAO.ActivityDao import ActivityDao
from DAO.TagDao import TagDao
from nltk.corpus import wordnet as wn

from util.KnowledgeBase import KnowledgeBase


class ActivityExpander:

    def __init__(self):
        self.kb = KnowledgeBase()

    def create_tag(self, taglabel):
        tagDao = TagDao(self.kb)
        id = tagDao.exist(taglabel)
        if (not id):
            new_tag = Tag(taglabel, "description_" + taglabel, "", "wordnet", "en", list(), list())
            created_tag = tagDao.add(new_tag)
            print(created_tag[0])
            id = created_tag[0].rid
        return id


    def check_synonyms_wordnet(self, activity, word2, threshold=0.0):
        activityDao = ActivityDao(self.kb)
        word1 = activity.name
        # syns1 = wn.synsets(word1)
        syns2 = wn.synsets(word2)
        tags_id = list()
        for syn2 in syns2:  # different meanings of the tag
            for synonym in syn2.lemmas(lang='eng'):  # synonyms of a meaning of a tag
                for syn3 in wn.synsets(synonym.name()):  # different meanings of a synonym
                    distance = syn2.path_similarity(syn3)
                    if distance and distance > threshold:
                        print("word1: " + word1 + "; word2: " + word2 + " (" + synonym.name() + ") -- syn3: " + str(
                            syn3) + "; syn2: " + str(syn2) + "; dist: " + str(distance))

                        tag_id2 = self.create_tag(str(syn3.lemmas()[0].name()))
                        result = activityDao.has_tag(activity.rid, tag_id2)
                        if (not result and tag_id2 not in tags_id):
                            tags_id.append(tag_id2)
        return tags_id


    def update_activities(self):
        activityDao = ActivityDao(self.kb)
        tagDao = TagDao(self.kb)
        all_activities = activityDao.getAll()
        threshold = 0.75

        for activity in all_activities:
            tags_ids = list()
            for tag_id1 in activity.tags:
                tag = tagDao.getById(tag_id1)
                tagLabel = tag[0].label.replace(' ', '_')
                tags_ids = tags_ids + self.check_synonyms_wordnet(activity, tagLabel, threshold)

            print("new Tags Ids: " + str(tags_ids))
            for new_tagid in tags_ids:
                activity.tags.append(new_tagid)
            activityDao.update(activity)


    def update_activities_old(self):
        activityDao = ActivityDao(self.kb)
        tagDao = TagDao(self.kb)
        all_activities = activityDao.getAll()
        print("len: " + str(len(all_activities)))
        for activity in all_activities:
            similarities = list()
            for tag_id1 in activity.tags:
                # similarities.append(tag_id1)
                tag = tagDao.getById(tag_id1)
                tagLabel = tag[0].label.replace(' ', '_')
                print("Tag: " + tagLabel)
                for my_syn in wn.synsets(tagLabel):
                    for syn in my_syn.lemmas(lang='eng'):
                        if (syn.count() > 0):
                            cadena = syn.name()
                            if (tagLabel != cadena):
                                # print(cadena,'+',str(syn.count()))
                                tag_id2 = self.create_tag(cadena)
                                result = activityDao.has_tag(activity.rid, tag_id2)
                                if (not result and tag_id2 not in similarities):
                                    similarities.append(tag_id2)
            print("similarities: " + str(similarities))
            for new_tagid in similarities:
                activity.tags.append(new_tagid)
            activityDao.update(activity)


if __name__ == "__main__":
    app = ActivityExpander()
    app.update_activities()
