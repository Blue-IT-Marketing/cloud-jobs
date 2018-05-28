#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'

# Copyright 2014 Freelancing Solutions.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os
import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer

#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))



class smsMessages (db.Expando):


    def sendMessage(self):
        pass
    def receiveMessage(self):
        pass
    def saveNumber(self):
        pass


# A class for identifying a single facebook user.
class FacebookUser(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)


class MyFacebook (db.Expando, MyConstants, ErrorCodes):
    access_token = db.StringProperty(required=True)
    FACEBOOK_APP_ID = "your app id"
    FACEBOOK_APP_SECRET = "your app secret"
    friendlist = db.StringListProperty()
    IndexReference = db.StringProperty()


    def login(self):  # Login to Facebook
        pass

    def logout(self):  # logout of facebook
        pass

    def getfriends(self):  # Obtains the friendlist and save the list on our local database
        pass

    def saveFriendList(self):  # This function will save the friend list of a specific user to our database.
        pass

    def sendWallUpdate(self, inMessage):
        pass

    def sendInvitations(self,InviteMessage):
        pass

    def createScheduledWallMessage(self,ScheduledMessage):
        pass

    def createScheduleFriendInvite(self,ScheduledMessage):
        pass

#  Used to store Facebook Details for each user.
class MainFacebook(db.Expando, MyConstants, ErrorCodes):
    UserFacebook = MyFacebook()
    UserDetails = FacebookUser()
class cloudcommHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')
        template = template_env.get_template('templates/CloudComm.html')
        context = {'loginURL': login_url, 'logoutURL': logout_url}
        self.response.write(template.render(context))

    def post(self):
        pass

app = webapp2.WSGIApplication([('/cloudcomm', cloudcommHandler)], debug=True)