from google.appengine.ext import ndb
from post import Post

class User(ndb.Model):
    lastname = ndb.StringProperty()
    firstname = ndb.StringProperty()
    username = ndb.StringProperty()
    image_label = ndb.StringProperty()
    email = ndb.StringProperty()
    posts = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
    followers = ndb.StringProperty(repeated = True)
