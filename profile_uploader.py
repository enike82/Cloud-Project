import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from datetime import datetime
import time

from post import Post

class EditProfileUploadHandler( blobstore_handlers.BlobstoreUploadHandler ):
    def post( self ):
        user = users.get_current_user()
        my_user_key = ndb.Key('User', user.user_id())
        my_user = my_user_key.get()
        upload = None
        msg = "Invalid form input"

        if len(self.get_uploads()) >= 1:
            upload = self.get_uploads()[ 0 ]

            blobinfo = blobstore.BlobInfo( upload.key() )
            ext = blobinfo.filename.split(".")[1]
            if str(ext).upper() == "JPG" or str(ext).upper() == "PNG":
                filename = "post_" + str(time.mktime(datetime.now().timetuple())) + "." + ext
                lastname = self.request.get('lastname')
                firstname = self.request.get('firstname')
                username = self.request.get('username')

                if self.request.get('lastname') == '' or self.request.get('firstname') == '' or self.request.get('username') == '':
                    url = '/update-profile?msg=' + msg + '&file=Please select upload image&lastname=' + lastname + '&firstname=' + firstname + '&username=' + username
                    self.redirect(url)
                    return
                else:
                    collection_key = ndb.Key( 'BlobCollection', 1 )
                    collection = collection_key.get()
                    collection.filenames.append( filename )
                    collection.blobs.append( upload.key() )
                    collection.put()

                    my_user.lastname = lastname
                    my_user.firstname = firstname
                    my_user.username = username
                    my_user.image_label = filename
                    my_user.email = user.email()
                    my_user.put()
                    url = "/profile"
                    self.redirect(url)
                    return
            else:
                url = '/update-profile?msg=' + msg + '&file=Only JPG or PNG files is allowed'
                self.redirect(url)
                return
        else:
            url = '/update-profile?msg=' + msg + '&file=Please select upload image'
            self.redirect(url)
            return
