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
#




#Module for creating background processes,
#this module will work hand in hand with preferences module to enable automatic functionality of our application for
#freelancers, affiliates, job seekers, employers and all our users.

#The backengine must be designed very carefully so as to minize the cost of trasanctions and calculations.

#The back engine will be run using cron jobs scheduled accordingly to the applications needs.

#it will make use of the memstore heavily to be able to perform longer and complicated calculations



#The backengine will also be responsible with keeping tally of the users presently logged in and showing the results
#on screen

# Class to track logged in and logged of users.
import os
import webapp2
import jinja2
from datatypes import Reference, Person
from google.appengine.api import memcache
from google.appengine.ext import db
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.api import users
import urllib2
from google.appengine.api import urlfetch
# Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))
User = Person()
#APPLICATION_ID
#os.environ['APPLICATION_ID']
class UsersTally(db.Expando, MyConstants, ErrorCodes):
    appID = db.StringProperty()
    #_TotalUsersKey = os.environ['APPLICATION_ID'] + 'TotalUsersKey' # Moved to Constants
    #_UsersListKey = os.environ['APPLICATION_ID'] + 'UsersListKey' # Moved to Constants
    UsersList = db.ListProperty(item_type=str)
    TotalUsers = db.IntegerProperty(default=0)

    def AddUser(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput in self.UsersList):
                self.UsersList.append(strinput)
                self.TotalUsers = self.TotalUsers + 1
                return True
            else:
                return False
        except:
            return self._generalError

    def RemoveUser(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput in self.UsersList:
                self.UsersList.remove(strinput)
                self.TotalUsers = self.TotalUsers - 1
                return True
            else:
                return False
        except:
            return self._generalError

    # Using the APPID as the key store a list of user references of those users online.
    # A Procedure launched by each page while it opens will launch a function that will refresh the references on the list
    # if a reference is not refreshed within a specific time period the user is taken of the list

#This class is used to send an update with the updated list of users to the screen
#will also be responsible with returning more information on such a user.
#it will also launch a refresh cycle for the current user online.
class UsersOnlineHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        Guser = users.get_current_user()
        tUsersList = memcache.get(self._UsersListKey)
        if Guser:
            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            if not(tUsersList == self.undefined):
                tUsersList = tUsersList.remove(reference)

        template = template_env.get_template('templates/whoisonline.html')
        if not(tUsersList == self.undefined):
            context = {'vUsersList': tUsersList}
        else:
            context = {}

        self.response.write(template.render(context))



app = webapp2.WSGIApplication([('/usersonline', UsersOnlineHandler)], debug=True)