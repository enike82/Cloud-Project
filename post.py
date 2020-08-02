from google.appengine.ext import ndb
from comment import Comment

class Post(ndb.Model):
    image = ndb.StringProperty()
    caption = ndb.StringProperty()
    created_at = ndb.DateTimeProperty()
    owner_id = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comment, repeated=True)
