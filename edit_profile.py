import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore

from user import User
from blob_collection import BlobCollection

from helpers import getImage

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class EditUserProfile(webapp2.RequestHandler):
    def get(self):
        url = ''
        my_user = None
        user = users.get_current_user()
        msg = ""
        firstname = ""
        lastname = ""
        username = ""
        file = ""
        has_error = False
        collection_key = ndb.Key( 'BlobCollection', 1 )
        collection = collection_key.get()

        if collection == None:
            collection = BlobCollection( id = 1)
            collection.put()

        try:
            if 'msg' in self.request.GET:
                has_error = True
                msg = self.request.get('msg')
                firstname = self.request.get('firstname')
                lastname = self.request.get('lastname')
                username = self.request.get('username')
                file = self.request.get('file')
        except:
            pass


        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            url = users.create_logout_url( self.request.uri )
            my_user_key = ndb.Key('User', user.user_id())
            my_user = my_user_key.get()

            if my_user:
                if my_user.lastname and my_user.lastname:
                    firstname = str(my_user.firstname).capitalize()
                    lastname = str(my_user.lastname).capitalize()
                    username = str(my_user.username).lower()

        template_values = {
            "url": url,
            "user": user,
            "msg": msg,
            "profile_image": getImage(my_user, collection, images),
            "edit_profile_url": blobstore.create_upload_url( '/edit-profile-uploader' ),
            "has_error": has_error,
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "file": file
        }
        template = JINJA_ENVIRONMENT.get_template('update_profile.html')
        self.response.write(template.render(template_values))
        return
