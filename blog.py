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
########################################################################################################################
########################################################################################################################
############################### FREELANCE JOBS BIDDING CLASSES #########################################################
########################################################################################################################
########################################################################################################################
import os
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
from datatypes import Reference
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from datatypes import Reference
from jobs import Job
from companies import Company
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))


#WebApp Loader
def doRender(handler, tname='index.html', values={}):
    temp = os.path.join(os.path.dirname(__file__),'templates/' + tname)

    if not os.path.isfile(temp):
        return False

    #make copy of the dictionary and add path
    newval = dict(values)
    newval['path'] = handler.'lkm;hkmnhkrmrequest.path

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True



class MainBlogHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/blog.html')
        context = {}
        self.response.write(template.render(context))


class SubmitBlogPostHandler(webapp2.RequestHandler, MyConstants,ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/blog.html')
        context = {}
        self.response.write(template.render(context))

    def post(self):
        pass

app = webapp2.WSGIApplication([('/blog', MainBlogHandler),
                               ('/blog/submit', SubmitBlogPostHandler)], debug=True)