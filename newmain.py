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
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
from google.appengine.ext.webapp import template
import datetime
from datatypes import Person, Reference
import jinja2
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from feedback import Feedback
from google.appengine.api import taskqueue
from bidmessages import BidMessages
from reviewbidsnotes import ReviewBidsNotes
from freelancejobs import FreelanceJobs
from jobs import Job
from accounts import AccountDetails
from subscriptions import Subscriptions
from newsletter import Newsletter
import math
from bids import Bids
from messageboard import MessageBoard
from profile import Profiles
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import logging
from google.appengine.api import oauth
GITHUB_API = 'https://api.github.com'





import getpass
import json
from urlparse import urljoin


#Sessions utility
from webapp2_extras import sessions
#BaseHanlder for sessions

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


# User Variable
User = Person()

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
    newval['path'] = handler.request.path

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True



class MainPage(BaseHandler, MyConstants, ErrorCodes):

    def get(self):

        try:

            Guser = users.get_current_user()

            findrequest = db.Query(Profiles).order('-DateTimeCreated')
            tProfiles = findrequest.fetch(limit=self._featuredProfilesLimit)
            reQuestURL = self.request.url
            login_url = "/login"
            logout_url = users.create_logout_url(dest_url='/')

            logging.info('MAIN PAGE NEW GET METHOD')
            fjobs = FreelanceJobs()
            fjobs = fjobs.retrieveJobsByJobType(strinput='freelance jobs')
            if not(fjobs == self._JobsNotFound) and not(fjobs == self._pkeyNotSet) and not(fjobs == self._generalError):
                fjobslist = fjobs
            else:
                fjobslist = []

            logging.info('RETRIEVE FREELANCE JOBS DONE')
            if Guser:
                if isGoogleServer:
                    ReferenceNum = Guser.user_id()
                else:
                    ReferenceNum = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', ReferenceNum)
                results = findquery.fetch(limit=self._maxQResults)

                #Get firstname and surname and vProfession and vDateTimeVerified and vTasks and vNotifications and vNumMessages

                if len(results) > 0:
                    result = results[0]
                    username = result.readUsername()
                    if username == self.undefined:
                        username = Guser.nickname()

                    logging.info('USERNAME FOUND')
                    errorMessage = self.undefined
                    template = template_env.get_template('/templates/index.html')

                    if result.readIsValid():
                        UserNotSubscribed = result.NewsletterSubscription
                        recNames = User.getNamesbyRefNum(strinput=ReferenceNum)
                        if not(recNames == self.undefined) and not(recNames == self._generalError):
                            context = {'user': username, 'vFirstname':recNames.readFirstname(), 'vSurname': recNames.readSurname(), 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'NewsLetterSubscription': UserNotSubscribed,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL, 'freelancejobslist': fjobslist}
                        else:
                            context = {'user': username, 'vFirstname':"John", 'vSurname': "Doe", 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'NewsLetterSubscription': UserNotSubscribed,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL, 'freelancejobslist': fjobslist}

                    else:
                        context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL}

                    self.response.write(template.render(context))
                else:
                    logging.info('USER NAME NICKNAME')
                    username = Guser.nickname()
                    errorMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'
                    template = template_env.get_template('/templates/index.html')

                    context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateSub': ActivateSub,
                               'vProfiles': tProfiles,'reQuestURL': reQuestURL, 'freelancejobslist': fjobslist}
                    self.response.write(template.render(context))
            else:

                logging.info('Username Home')
                username = ''
                errorMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                template = template_env.get_template('/templates/index.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateLogin': ActivateLogin,
                           'vProfiles': tProfiles,'reQuestURL': reQuestURL, 'freelancejobslist': fjobslist}
                self.response.write(template.render(context))

        except:
            errorMessage = 'There was an error accessing our database please try again in a minute'
            doRender(self, 'index.html', {'errorMessage': errorMessage})

    def post(self):
        try:
            Guser = users.get_current_user()
            tComNames = self.request.get('vComNamesr')
            tComEmail = self.request.get('vComEmailr')
            tMainComment = self.request.get('vMainCommenter')
            tMessageHeading = self.request.get('vHeadingsr')
            tMessageBoard = MessageBoard()
            findrequest = db.Query(Profiles).order('-DateTimeCreated')
            tProfiles = findrequest.fetch(limit=self._featuredProfilesLimit)

            fjobs = FreelanceJobs.retrieveJobsByJobType(strinput='freelance jobs')
            if not(fjobs == self._JobsNotFound) and not(fjobs == self._pkeyNotSet) and not(fjobs == self._generalError):
                fjobslist = fjobs
            else:
                fjobslist = []

            if Guser:
                if isGoogleServer:
                    ReferenceNum = Guser.user_id()
                else:
                    ReferenceNum = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', ReferenceNum)
                results = findquery.fetch(limit=self._maxQResults)

                login_url = '/login'
                logout_url = users.create_logout_url(dest_url='/')

                tMessageBoard.createBoardMessage(inSenderNames=tComNames, inSenderEmail=tComEmail, inBoardMessage=tMainComment, inMessageHeading=tMessageHeading, inMessageActivated=True)

                if len(results) > 0:
                    result = results[0]
                    username = result.readUsername()
                    if username == self.undefined:
                        username = Guser.nickname()

                    logging.info('Username Found')
                    errorMessage = self.undefined
                    template = template_env.get_template('/templates/index.html')

                    if result.readIsValid():
                        UserNotSubscribed = result.NewsletterSubscription
                        context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'NewsLetterSubscription': UserNotSubscribed,
                                   'vProfiles': tProfiles, 'freelancejobslist': fjobslist}
                    else:
                        context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage,
                                   'vProfiles': tProfiles, 'freelancejobslist': fjobslist}

                    self.response.write(template.render(context))
                else:
                    username = Guser.nickname()
                    errorMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'
                    template = template_env.get_template('/templates/index.html')

                    context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateSub': ActivateSub,
                               'vProfiles': tProfiles, 'freelancejobslist': fjobslist}
                    self.response.write(template.render(context))
            else:
                login_url = '/login'
                logout_url = users.create_logout_url(dest_url='/')
                tMessageBoard.createBoardMessage(inSenderNames=tComNames, inSenderEmail=tComEmail, inBoardMessage=tMainComment, inMessageActivated=True)
                username = self.undefined
                errorMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                template = template_env.get_template('/templates/index.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateLogin': ActivateLogin,
                           'vProfiles': tProfiles, 'freelancejobslist': fjobslist}
                self.response.write(template.render(context))

        except:
            errorMessage = 'There was an error accessing our database please try again in a minute'
            doRender(self, 'index.html', {'errorMessage': errorMessage})


class loginHandler(BaseHandler, MyConstants, ErrorCodes):

    def get(self):

        Glogin_url = users.create_login_url(dest_url='/')
        FLogin_url = '/facelogin'
        GitLogin_url = '/gitlogin'
        TLogin_url = 'twittlogin'



        template = template_env.get_template('/templates/login.html')
        context = {'GoogleLoginURL': Glogin_url, 'FaceLoginURL': FLogin_url, 'GITLoginURL': GitLogin_url, 'TwitterLoginURL': TLogin_url}
        self.response.write(template.render(context))


    def post(self):

        referrence_url = self.request.uri
        strLoginName = self.request.get('vstrEmail')
        strPassword = self.request.get('vstrPassword')
        bolRemember = self.request.get('vbolRemember')

        logging.info("LOGIN DETAILS")
        logging.info('Email = ' + strLoginName)
        logging.info('Password = ' + strPassword)
        logging.info('Remember Setting = ' + bolRemember)
        logging.info(referrence_url)

        Glogin_url = users.create_login_url(dest_url='/')
        FLogin_url = '/facelogin'
        GitLogin_url = '/gitlogin'
        TLogin_url = '/twittlogin'

        email_result = User.clsReference.writeVerEmail(strinput=strLoginName)
        username_result = User.clsReference.writeUsername(strinput=strLoginName)
        password_result = User.clsReference.writePassword(strinput=strPassword)



        if email_result and username_result and password_result:
            pass
        else:
            template = template_env.get_template('/templates/login.html')
            context = {'ErrorMessage': 'Please Fill in both fields', 'GoogleLoginURL': Glogin_url, 'FaceLoginURL': FLogin_url, 'GITLoginURL': GitLogin_url, 'TwitterLoginURL': TLogin_url}
            self.response.write(template.render(context))
            return self._generalError




        temp_User = User.getReferenceByUsername(strinput=strLoginName)

        if temp_User != self._userNameDonotExist:
            User.getReferenceByUsername(strinput=strLoginName)
            if User.clsReference.readPassword() == strPassword:
                self.session['username'] = strLoginName
                #self.Guser = users.User(User.clsReference.readVerEmail())


                template = template_env.get_template('/templates/index.html')
                context = {'ErrorMessage': 'Login Succesfully', 'GoogleLoginURL': Glogin_url, 'FaceLoginURL': FLogin_url, 'GITLoginURL': GitLogin_url}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('/templates/login.html')
                context = {'ErrorMessage': 'Password not Valid please retype or use recovery methods below', 'GoogleLoginURL': Glogin_url, 'FaceLoginURL': FLogin_url, 'GITLoginURL': GitLogin_url}
                self.response.write(template.render(context))

        else:
            template = template_env.get_template('/templates/login.html')
            context = {'ErrorMessage': 'Username Does Not Exist Please Click on Register New Membership Below or Signin Using Google', 'GoogleLoginURL': Glogin_url, 'FaceLoginURL': FLogin_url, 'GITLoginURL': GitLogin_url}
            self.response.write(template.render(context))





class GITHubLoginHandler(BaseHandler, MyConstants, ErrorCodes):

    def get(self):

        # User Input
        #
        username = raw_input('Github username: ')
        password = getpass.getpass('Github password: ')
        note = raw_input('Note (optional): ')
        #
        # Compose Request
        #
        url = urljoin(GITHUB_API, 'authorizations')
        payload = {}
        if note:
            payload['note'] = note
        #res = requests.post( url, auth = (username, password),data = json.dumps(payload), )
        #
        # Parse Response
        #
        #j = json.loads(res.text)
        #if res.status_code >= 400:
        #    msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
        #    print 'ERROR: %s' % msg
        #    return
        #token = j['token']
        #print 'New token: %s' % token

class FacebookLoginHandler(BaseHandler,MyConstants,ErrorCodes):
    def get(self):
        pass
    def post(self):
        pass

class TwitterLoginHandler(BaseHandler,MyConstants,ErrorCodes):
    def get(self):
        pass
    def post(self):
        pass

class registerHandler(BaseHandler, MyConstants,ErrorCodes):

    def get(self):
        g_sub_url = users.create_login_url(dest_url='/g_register')
        template = template_env.get_template('/templates/register.html')
        context= {'GoogleSubUrl': g_sub_url}
        self.response.write(template.render(context))

    def post(self):
        strFullNames = self.request.get('vstrFullname')
        strEmailAddress = self.request.get('vstrEmail')
        strPassword = self.request.get('vstrPassword')

        if " " in strFullNames:
            names_List = []
            names_List = strFullNames.split(" ")
            strFirstname = names_List[0]
            strLastname = names_List[1]
        else:
            strFirstname = strFullNames
            strLastname = strFullNames

        User.clsReference.writeUsername(strinput=strEmailAddress)
        User.clsReference.writePassword(strinput=strPassword)
        User.clsReference.writeVerEmail(strinput=strEmailAddress)

        result = User.AddReferenceclasstoStore()
        if self._pkeyvalue == result:
            User.clsNames.writeFirstname(name=strFirstname)
            User.clsNames.writeSurname(name=strLastname)
            User.clsNames.writeSecondname(name=strLastname)
            User.addNamesbyUserName(strinput=strEmailAddress)
            g_sub_url = users.create_login_url(dest_url='/g_register')
            template = template_env.get_template('/templates/login.html')
            context= {'ErrorMessage': 'User Succesfully Registered Username : '+ str(strEmailAddress) + 'Please Login and Activate Your Account','GoogleSubUrl': g_sub_url}
        else:
            g_sub_url = users.create_login_url(dest_url='/g_register')
            template = template_env.get_template('/templates/register.html')
            context= {'ErrorMessage': 'User Not Registered : '+ str(strEmailAddress) + 'Please Try Using a different Login Name','GoogleSubUrl': g_sub_url}






class GoogleregisterHandler(BaseHandler, MyConstants, ErrorCodes):
    def get(self):
        pass

    def post(self):
        pass # Get information from google registration

class recoverHandler(BaseHandler, MyConstants,ErrorCodes):

    def get(self):
        template = template_env.get_template('templates/recover.html')
        context = {}
        self.response.write(template.render(context))

    def post(self):
        try:
            strRecoveryEmail = self.request.get('vrecEmail')
            email_result = User.clsReference.writeVerEmail(strinput=strRecoveryEmail)
            if email_result == True:
                result_Reference = User.getReferenceByUsername(strinput=User.clsReference.readVerEmail())
                if result_Reference != self._userNameDonotExist:
                    User.clsReference = result_Reference
                    message = mail.EmailMessage()
                    message.sender = self._AppEmail
                    User.clsReference.CreateEmailVerCode()
                    Verification_Code = User.clsReference.readEmailVerCode()


                    MessageSubject = 'Cloud-Jobs Account Recovery'
                    MessageBody = """
                    Cloud Jobs Account Recovery
                    Please Use the verification code supplied below to Recover your account on http://cloud-jobs.org
                    Recovery Code:""" + Verification_Code + """
                    In order to recover your account please Enter the above mentioned Code
                    on Cloud-Jobs Now.

                    Thank you.
                    Cloud-Jobs.org Team"""

                    message.to = User.clsReference.readVerEmail()
                    message.subject = MessageSubject
                    message.body = MessageBody
                    message.send()

                    template = template_env.get_template('templates/recover.html')
                    context = {'ErrorMessage':'Please Enter The Code that was sent to your registered Email Address'}
                    self.response.write(template.render(context))
                else:
                    template = template_env.get_template('templates/recover.html')
                    context = {'ErrorMessage':'The Username supplied does not exist please Register by clicking on register below'}
                    self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/recover.html')
                context = {'ErrorMessage':'Invalid Recovery Email Address or Username'}
                self.response.write(template.render(context))
        except:
            logging.info("Exceptions Thrown on Account Recovery")









class logoutHandler (BaseHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()
        login_url = users.create_login_url(dest_url='/')
        logout_url = users.create_logout_url(dest_url='/')

        if Guser:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (Guser.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)

class NotFound(BaseHandler, MyConstants, ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/sitemap.html')
        context = {}
        self.response.write(template.render(context))


class termsHandler(BaseHandler, MyConstants, ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/terms.html')
        context = {}
        self.response.write(template.render(context))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'leharg8y94hibigdecf8tf943r3u349hubviwege723684u4hifccbhowuewiygyg5675734gv8747grfvgc8667s56as',
    'cookie_name' : 'cloud-jobs',
}

app = webapp2.WSGIApplication([('/login', loginHandler),
                               ('/facelogin', FacebookLoginHandler),
                               ('/gitlogin', GITHubLoginHandler),
                               ('/twittlogin', TwitterLoginHandler),
                               ('/logout', logoutHandler),
                               ('/register', registerHandler),
                               ('/g_register',GoogleregisterHandler),
                               ('/recover', recoverHandler),
                               ('/tersm', termsHandler),
                               ('/index.html', MainPage),
                               ('/', MainPage),
                               ('/.*', NotFound)], debug=True,config=config)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

########################################################################################################################
########################################################################################################################
##################################### MAIN PAGE HANDLER ################################################################
########################################################################################################################
########################################################################################################################