import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from datetime import datetime
import time

from post import Post

class PostUploadHandler( blobstore_handlers.BlobstoreUploadHandler ):
    def post( self ):
        user = users.get_current_user()
        my_user_key = ndb.Key('User', user.user_id())
        my_user = my_user_key.get()
        upload = None

        if len(self.get_uploads()) >= 1:
            upload = self.get_uploads()[ 0 ]

            blobinfo = blobstore.BlobInfo( upload.key() )
            ext = blobinfo.filename.split(".")[1]
            if str(ext).upper() == "JPG" or str(ext).upper() == "PNG":
                filename = "post_" + str(time.mktime(datetime.now().timetuple())) + "." + ext
                post_caption = self.request.get( 'post_caption' )

                if post_caption != "":
                    collection_key = ndb.Key( 'BlobCollection', 1 )
                    collection = collection_key.get()
                    collection.filenames.append( filename )
                    collection.blobs.append( upload.key() )
                    collection.put()

                    new_post = Post(
                        image = filename,
                        caption = post_caption,
                        created_at = datetime.now(),
                        owner_id = str(my_user.key.id())
                    )

                    post_key = new_post.put()

                    my_user.posts.append(str(post_key.get().key.id()))
                    my_user.put()
                    url = "/feeds"
                    self.redirect(url)
                    return
                else:
                    url = "/create-post?caption=Caption is required"
                    self.redirect(url)
            else:
                url = "/create-post?file=Only JPG or PNG files is allowed"
                self.redirect(url)
                return
        else:
            url = "/create-post?file=Please select upload image"
            self.redirect(url)
            return
