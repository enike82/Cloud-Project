import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

from user import User

from helpers import getImage, getPosts, getCurrentUserTimelinePost, sortPostByDateInDesendingOrder, getFirstFiftyPostWithImages

from view_all_comments import ViewAllCommentsInAPost
from create_comment import CreateCommentPost
from profile import UserProfile
from follow import UpdateFollowStatus
from search import SearchUserAccount
from profile_user import OtherUserProfile
from edit_profile import EditUserProfile
from create_post import CreatePost
from profile_uploader import EditProfileUploadHandler
from post_upload import PostUploadHandler
from redirect_to import RedirectToFeeds
from blob_collection import BlobCollection
from api import APIRequest
from follower_following import FollowersFollowingPage


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):

        url = ''
        my_user = None
        user = users.get_current_user()
        fullname = ""
        username = ""

        collection_key = ndb.Key( 'BlobCollection', 1 )
        collection = collection_key.get()

        if collection == None:
            collection = BlobCollection( id = 1)
            collection.put()

        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            url = users.create_logout_url( self.request.uri )
            my_user_key = ndb.Key('User', user.user_id())
            my_user = my_user_key.get()

            if my_user == None:
                my_user = User(id=user.user_id())
                my_user.put()
                self.redirect('/update-profile')
                return
            else:
                if my_user.lastname and my_user.lastname:
                    fullname = str(my_user.firstname).capitalize() + " " + str(my_user.lastname).capitalize()
                    username = str(my_user.username).lower()
                else:
                    self.redirect('/update-profile')
                    return


        posts = getCurrentUserTimelinePost(my_user)
        posts = sortPostByDateInDesendingOrder(posts)
        posts = getFirstFiftyPostWithImages(posts, collection, images)

        if len(posts) <= 0:
            self.redirect("/create-post")
            return


        template_values = {
            "url": url,
            "my_user_key": None,
            "fullname": fullname,
            "username": username,
            "profile_image": getImage(my_user, collection, images),
            "posts": posts,
            "reversed": reversed

        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))
        return

app = webapp2.WSGIApplication([
    webapp2.Route(r'/<post_id:[^/]+>/view-comments', handler=ViewAllCommentsInAPost),
    webapp2.Route(r'/<post_id:[^/]+>/add-comment', handler=CreateCommentPost),
    webapp2.Route(r'/<user_id:[^/]+>/followship/<option:[^/]+>', handler=FollowersFollowingPage),
    webapp2.Route(r'/feeds', handler=MainPage),
    webapp2.Route(r'/<user_id:[^/]+>/update-follow', handler=UpdateFollowStatus),
    webapp2.Route(r'/get-json-objects', handler=APIRequest),
    webapp2.Route(r'/search', handler=SearchUserAccount),
    webapp2.Route(r'/create-post', handler=CreatePost),
    webapp2.Route(r'/edit-profile-uploader', handler=EditProfileUploadHandler),
    webapp2.Route(r'/post-uploader', handler=PostUploadHandler),
    webapp2.Route(r'/update-profile', handler=EditUserProfile),
    webapp2.Route(r'/<user_id:[^/]+>/others-profile', handler=OtherUserProfile),
    webapp2.Route(r'/profile', handler=UserProfile),
    webapp2.Route(r'/', handler=RedirectToFeeds),
], debug = True)
