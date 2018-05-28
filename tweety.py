#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'

# Copyright 2014 Freelancing Solutions.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import webapp2
from datatypes import Reference
import datetime
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from datatypes import Reference
import logging
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
from google.appengine.ext.webapp import template
import datetime
from datatypes import Person, Reference
import jinja2
from tweepy import *
import time, sys

class freelancingsolutionsAppTwitter (db.Expando, MyConstants, ErrorCodes):
    #enter the corresponding information from your Twitter application:
    CONSUMER_KEY = 'Z5OBHoTagvRqfo4HcFwzHDAqF'#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = 'l82wzMmc7E0JwIPUJDirccv34f3PduXlZiBWgvhbRVSgTD1FPL'#keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = '1585367040-dSpu8oFY9mXdv0twAtkOjyBpCyzKmKAHwfRX5S8s'#keep the quotes, replace this with your access token
    ACCESS_SECRET = 'odHeYbMuugRWafkVexOAfDus1nZxeumganHXwYYdcmhDC'#keep the quotes, replace this with your access token secret

    def authorise (self):
        try:
            auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
            auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
            api = tweepy.API(auth)
            return True
        except:
            return self._generalError


    def update_status(self, strStatus):
        try:
            auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
            auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
            api = tweepy.API(auth)
            if len(strStatus) > 0 :
                api.update_status(strStatus)
            else:
                api.update_status("Freelancing Solutions introducing <a href='http://jobcloud.freelancing-seo.com/FreelanceJobs' target='_self'>Freelance Jobs</a>")
            return True
        except:
            return self._generalError


class freelancingSolutionsAppHandler (webapp2.RequestHandler, MyConstants, ErrorCodes, freelancingsolutionsAppTwitter):
    def get(self):
        try:
            Authorized = self.authorise()
            if not(Authorized == self._generalError):
                StatusUpdated = self.update_status(strStatus='Just Testing on twitter')
                if StatusUpdated :
                    logging.info('Twitting Successfully')
                else:
                    logging.info('Unable to Twiitt')
            else:
                logging.info('Failing to get authorization when twitting')
        except:
            return self._generalError


app = webapp2.WSGIApplication([('/cron/promotionalTweets', freelancingSolutionsAppHandler)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()