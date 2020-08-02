import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from user import User
from blob_collection import BlobCollection


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class CreatePost(webapp2.RequestHandler):
    def get(self):
        url = ''
        my_user = None
        user = users.get_current_user()
        has_error = False
        file = ""
        caption = ""
        fullname = ""
        username = ""

        try:
            if 'file' in self.request.GET or 'caption' in self.request.GET:
                has_error = True
                file = '' if self.request.get('file') == None else self.request.get('file')
                caption = '' if self.request.get('caption') == None else self.request.get('caption')
        except:
            pass

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

        collection_key = ndb.Key( 'BlobCollection', 1)
        collection = collection_key.get()

        if collection == None:
            collection = BlobCollection( id = 1)
            collection.put()

        template_values = {
            "url": url,
            "fullname": fullname,
            "username": username,
            "post_url": blobstore.create_upload_url( '/post-uploader' ),
            "has_error": has_error,
            "file": file,
            "caption": caption
        }
        template = JINJA_ENVIRONMENT.get_template('create_post.html')
        self.response.write(template.render(template_values))
        return
