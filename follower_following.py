import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

from user import User

from helpers import getSelectedUserInstance, getUserListFromFollowship


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class FollowersFollowingPage(webapp2.RequestHandler):
    def get(self, user_id, option):
        url = ''
        my_user = None
        user = users.get_current_user()
        fullname = ""
        username = ""
        selected_user = getSelectedUserInstance(user_id)
        members = []

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
                    fullname = str(selected_user.firstname).capitalize() + " " + str(selected_user.lastname).capitalize()
                    username = str(selected_user.username).lower()
                else:
                    self.redirect('/update-profile')
                    return

        if option == "followers":
            members = getUserListFromFollowship(selected_user.followers)
        else:
            members = getUserListFromFollowship(selected_user.following)

        template_values = {
            "url": url,
            "my_user_key": user_id,
            "fullname": fullname,
            "username": username,
            "option_member": members,
            "option": option,
            "my_user": my_user
        }
        template = JINJA_ENVIRONMENT.get_template('followship.html')
        self.response.write(template.render(template_values))
        return
