import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

from user import User

from helpers import getSelectedUserInstance, getFollowedStatus


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class UpdateFollowStatus(webapp2.RequestHandler):
    def post(self, user_id):
        my_user = None
        user = users.get_current_user()

        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            my_user_key = ndb.Key('User', user.user_id())
            my_user = my_user_key.get()

            if my_user == None:
                my_user = User(id=user.user_id())
                my_user.put()
                self.redirect('/update-profile')
                return
            else:
                if my_user.lastname and my_user.lastname:
                    pass
                else:
                    self.redirect('/update-profile')
                    return

        selected_user = getSelectedUserInstance(user_id)
        my_user_id = str(my_user.key.id())
        selected_user_id = str(selected_user.key.id())

        if getFollowedStatus(my_user.following, selected_user_id):
            my_user.following.remove(selected_user_id)
            my_user.put()

            selected_user.followers.remove(my_user_id)
            selected_user.put()
        else:
            my_user.following.append(selected_user_id)
            my_user.put()

            selected_user.followers.append(my_user_id)
            selected_user.put()

        self.redirect('/' + selected_user_id + '/others-profile')


        
