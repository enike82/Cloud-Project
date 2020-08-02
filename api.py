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

class APIRequest( webapp2.RequestHandler ):
    def post( self ):
        self.response.headers[ 'Content-Type' ] = 'application/json'
        user = users.get_current_user()
        my_user_key = ndb.Key( 'User', user.user_id() )
        my_user = my_user_key.get()
        data = self.request.body
        search_string = data.split('=')[1]
        accounts = getAccounts(str(my_user.key.id()), search_string)
        self.response.write( json.dumps( [ dict(user.to_dict(), **dict(id=user.key.id())) for user in  accounts ] ) )
        return
