from google.appengine.ext import ndb

class Comment(ndb.Model):
    comment = ndb.StringProperty()
    comment_by = ndb.StringProperty()
    comment_by_id = ndb.StringProperty()
