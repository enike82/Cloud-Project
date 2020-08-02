import webapp2
import jinja2
import os
import datetime
import json
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from user import User

from helpers import getAccounts
from comment import Comment

class CreateCommentPost( webapp2.RequestHandler ):
    def post( self, post_id ):
        self.response.headers[ 'Content-Type' ] = 'text/html'
        user = users.get_current_user()
        my_user_key = ndb.Key( 'User', user.user_id() )
        my_user = my_user_key.get()
        post = ndb.Key( 'Post', int(post_id) ).get()
        comment_body = self.request.get( 'comment_body' )

        new_comment = Comment(
            comment = comment_body,
            comment_by = my_user.username,
            comment_by_id = str(my_user.key.id())
        )

        if comment_body:
            post.comments.append(new_comment)
            post.put()

        self.redirect("/feeds#"+str(post.key.id()))
