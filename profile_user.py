import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

from user import User

from helpers import getPosts, getImage, getSelectedUserInstance, getFollowedStatus


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class OtherUserProfile(webapp2.RequestHandler):
    def get(self, user_id):
        url = ''
        my_user = None
        user = users.get_current_user()
        fullname = ""
        username = ""
        collection_key = ndb.Key( 'BlobCollection', 1 )
        collection = collection_key.get()
        selected_user = getSelectedUserInstance(user_id)

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
                if selected_user.lastname and selected_user.lastname:
                    fullname = str(selected_user.firstname).capitalize() + " " + str(selected_user.lastname).capitalize()
                    username = str(selected_user.username).lower()
                else:
                    self.redirect('/update-profile')
                    return

        template_values = {
            "url": url,
            "my_user_key": user_id,
            "fullname": fullname,
            "username": username,
            "profile_image": getImage(selected_user, collection, images),
            "posts": getPosts(selected_user, collection, images),
            "post_count": len(selected_user.posts),
            "following_count": len(selected_user.following),
            "followers_count": len(selected_user.followers),
            "followed": getFollowedStatus(my_user.following, user_id),
            "followship_id": str(selected_user.key.id())
        }
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))
        return
