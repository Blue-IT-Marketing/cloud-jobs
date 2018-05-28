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





########################################################################################################################
########################################################################################################################
##################################### MAIN PAGE HANDLER ################################################################
########################################################################################################################
########################################################################################################################

class MainPage(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        try:
            Guser = users.get_current_user()
            findrequest = db.Query(Profiles).order('-DateTimeCreated')
            tProfiles = findrequest.fetch(limit=self._featuredProfilesLimit)
            reQuestURL = self.request.url
            if Guser:
                if isGoogleServer:
                    ReferenceNum = Guser.user_id()
                else:
                    ReferenceNum = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', ReferenceNum)
                results = findquery.fetch(limit=self._maxQResults)

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                #Get firstname and surname and vProfession and vDateTimeVerified and vTasks and vNotifications and vNumMessages

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
                        recNames = User.getNamesbyRefNum(strinput=ReferenceNum)
                        if not(recNames == self.undefined) and not(recNames == self._generalError):
                            context = {'user': username, 'vFirstname':recNames.readFirstname(), 'vSurname': recNames.readSurname(), 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'NewsLetterSubscription': UserNotSubscribed,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL}
                        else:
                            context = {'user': username, 'vFirstname':"John", 'vSurname': "Doe", 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'NewsLetterSubscription': UserNotSubscribed,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL}

                    else:
                        context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage,
                                   'vProfiles': tProfiles,'reQuestURL': reQuestURL}

                    self.response.write(template.render(context))
                else:
                    username = Guser.nickname()
                    errorMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'
                    template = template_env.get_template('/templates/index.html')

                    context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateSub': ActivateSub,
                               'vProfiles': tProfiles,'reQuestURL': reQuestURL}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                username = self.undefined
                errorMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                template = template_env.get_template('/templates/index.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateLogin': ActivateLogin,
                           'vProfiles': tProfiles,'reQuestURL': reQuestURL}
                self.response.write(template.render(context))

        except:
            errorMessage = 'There was an error accessing our database please try again in a minute'
            doRender(self, 'index.html', {'errorMessage': errorMessage})

    def post(self):
        try:
            Guser = users.get_current_user()
            tComNames = self.request.get('vComNames')
            tComEmail = self.request.get('vComEmailr')
            tMainComment = self.request.get('vMainCommenter')
            tMessageHeading = self.request.get('vHeadingsr')
            tMessageBoard = MessageBoard()
            findrequest = db.Query(Profiles).order('-DateTimeCreated')
            tProfiles = findrequest.fetch(limit=self._featuredProfilesLimit)

            if Guser:
                if isGoogleServer:
                    ReferenceNum = Guser.user_id()
                else:
                    ReferenceNum = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', ReferenceNum)
                results = findquery.fetch(limit=self._maxQResults)

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                tMessageBoard.createBoardMessage(inSenderNames=tComNames,inSenderEmail=tComEmail,inBoardMessage=tMainComment, inMessageHeading=tMessageHeading, inMessageActivated=True)

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
                                   'vProfiles': tProfiles}
                    else:
                        context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage,
                                   'vProfiles': tProfiles}

                    self.response.write(template.render(context))
                else:
                    username = Guser.nickname()
                    errorMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'
                    template = template_env.get_template('/templates/index.html')

                    context = {'user': username, 'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateSub': ActivateSub,
                               'vProfiles': tProfiles}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                tMessageBoard.createBoardMessage(inSenderNames=tComNames,inSenderEmail=tComEmail,inBoardMessage=tMainComment,inMessageActivated=True)
                username = self.undefined
                errorMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                template = template_env.get_template('/templates/index.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'errorMessage': errorMessage, 'ActivateLogin': ActivateLogin,
                           'vProfiles': tProfiles}
                self.response.write(template.render(context))

        except:
            errorMessage = 'There was an error accessing our database please try again in a minute'
            doRender(self, 'index.html', {'errorMessage': errorMessage})





class loginHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (Guser.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)






class logoutHandler (webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (Guser.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)


class SubscriptionsHandler (webapp2.RequestHandler):
    def post(self):
        doRender(self, 'subscribe.html')
    def get(self):
        doRender(self, 'subscribe.html')




####################################### ABOUT HANDLERS ################################################################
#######################################################################################################################
# THIS HANDLERS SERVES STATIC HTML FILES THEY WILL HELP WITH THE SEO ##################################################
####################################### ABOUT HANDLERS ################################################################
#######################################################################################################################

class AboutHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/about.html')


            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())

            else:
                User.clsReference.writeUsername(Guser.nickname())
                context = {'loginURL': login_url, 'logoutURL': logout_url}

            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}


            self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/about.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))


class aFreelanceJobsHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/afreelancejobs.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())
            else:
                User.clsReference.writeUsername(Guser.nickname())


            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}

            self.response.write(template.render(context))

        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/afreelancejobs.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))

class aMarketPlaceHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/amarketplace.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())

            else:
                User.clsReference.writeUsername(Guser.nickname())

            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))

        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/amarketplace.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))



class aJobMarketHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/ajobmarket.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())
            else:
                User.clsReference.writeUsername(Guser.nickname())

            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))

        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/ajobmarket.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))


class aAffiliatesHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/aaffiliates.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())

            else:
                User.clsReference.writeUsername(Guser.nickname())

            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}

            self.response.write(template.render(context))

        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/aaffiliates.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))



#################################################MAIN MENU HANDLERS#####################################################
########################################################################################################################




class FreelanceJobsHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/freelancejobs.html')


            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())
                tFreelanceJobs = FreelanceJobs()

                result = tFreelanceJobs.retrieveJobsByJobType('freelance jobs')
                myResult = tFreelanceJobs.GetFreelanceJobsByReference(ReferenceNum)

                if not(myResult == self._generalError) and not(myResult == self._referenceDoNotExist) and not(myResult == self._JobsNotFound):
                    tMFreelanceJobs = myResult
                    tMFreelanceJobs.sort()
                    myFJobsFound = 'Yes'
                else:
                    tMFreelanceJobs = self.undefined
                    myFJobsFound = 'No'

                if not(result == self._JobsNotFound) and not(result == self._pkeyNotSet) and not(result == self._generalError):

                    logging.info('number of jobs :' + str(len(result)))
                    logging.info('number of owned freelance jobs:' + str(len(myResult)))
                    findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                    fSubs = findrequest.fetch(limit=1)

                    if len(fSubs) > 0:
                        fSub = fSubs[0]
                    else:
                        fSub = Subscriptions()
                        fSub.assignOwner(User._pkeyvalue)
                        fSub.put()

                    if not(tMFreelanceJobs == self._JobsNotFound) and not(tMFreelanceJobs == self._referenceDoNotExist) and not(tMFreelanceJobs == self._generalError):
                        context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                'freelancejobslist': result, 'myfreelancejobslist': tMFreelanceJobs, 'myFJobsFound': myFJobsFound,
                                'vJobSubmitCredit': fSub.readJobSubmissionCredit(), 'vBiddingCredit': fSub.readBiddingCredit(),
                                'vProfilePromoCredit': fSub.readProfilePromoCredit()}
                    else:

                        context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                'freelancejobslist': result, 'myFJobsFound': myFJobsFound,
                                'vJobSubmitCredit': fSub.readJobSubmissionCredit(), 'vBiddingCredit': fSub.readBiddingCredit(),
                                'vProfilePromoCredit': fSub.readProfilePromoCredit()}
                else:
                    Usermessage = 'There are presently no freelance jobs please submit freelance jobs'
                    ActivateSubmitButt = 'Yes'
                    context = {'vUsername': User.clsReference.readUsername(), 'logingURL': login_url, 'logoutURL': logout_url,
                               'Usermessage': Usermessage, 'ActivateSubmitButt': ActivateSubmitButt}
            else:
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())
                Usermessage = self._CompleteSubscriptionForm
                ActivateSub = 'Yes'

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': User.clsReference.readUsername(),
                           'Usermessage': Usermessage, 'ActivateSub': ActivateSub}


            self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            tFreelanceJobs = FreelanceJobs()
            result = tFreelanceJobs.retrieveJobsByJobType('freelance jobs')
            MemberMessage = self._userNotLoggedin
            ActivateLogin = 'Yes'



            template = template_env.get_template('/templates/freelancejobs.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url,'freelancejobslist': result, 'Usermessage': MemberMessage,
                       'ActivateLogin': ActivateLogin}
            self.response.write(template.render(context))


    def post(self):
        #Check if the user is logged in.
        #Find the freelance job and see if it exists
        #Create the Bidding Class for the current user and show the bidding form for the job
        #Check on the job if bidding is still open
        #Show the Extra Details of the Job such as the skills and extra notes on the job.
        #Allow the user to create the bid.
        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/freelancejobs.html')


            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())
                tFreelanceJobs = FreelanceJobs()

                tStrJobReference = self.request.get('vJobReference')
                logging.info('JOB REFERENCE WE ARE BIDDING ON :' + tStrJobReference)
                findquery = db.Query(Job).filter('strJobReference =', tStrJobReference)
                results = findquery.fetch(limit=self._maxQResults)
                logging.info('User Logged In and Account Exist:')
                self._bidJobPkey = tStrJobReference
                memcache.set(ReferenceNum, tStrJobReference, time=300000)
                if len(results) > 0:
                    fFreelanceJob = results[0]
                    BidEnding = fFreelanceJob.readDateTimeEndBidorRemove()
                    if fFreelanceJob.readBidsActivated():  # Bidding is activated
                        thistime = datetime.datetime.now()
                        if BidEnding >= thistime:   # Bidding is still active
                            # Show Bidding Form with all the details.
                            # Read from subscriptions and check if bidding credit is available and then subtract the credit needed to place this bid.
                            findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                            results = findrequest.fetch(limit=1)
                            if len(results) > 0:
                                fSubscriptions = results[0]
                            else:
                                fSubscriptions = Subscriptions()
                                fSubscriptions.assignOwner(User._pkeyvalue)
                                fSubscriptions.put()
                            if int(fSubscriptions.readBiddingCredit()) >= int(fFreelanceJob.readPlaceBidCredit()):
                                tempBiddingCr = int(fSubscriptions.readBiddingCredit()) -  int(fFreelanceJob.readPlaceBidCredit())
                                fSubscriptions.writeBiddingCredit(tempBiddingCr)
                                fSubscriptions.put()
                                listJobBudget = fFreelanceJob.translateJobBudget()
                                if len(fFreelanceJob.StrSkillsRequired) > 0:
                                    i = 0
                                    SKillSet = []
                                    while i < len(fFreelanceJob.StrSkillsRequired):
                                        SSkill = fFreelanceJob.StrSkillsRequired[i]
                                        if SSkill == 'englishus':
                                            SSkill = 'English US'
                                        elif SSkill == 'englishuk':
                                            SSkill = 'English UK'
                                        elif SSkill == 'html':
                                             SSkill = 'HTML'
                                        elif SSkill == 'seo':
                                             SSkill = 'SEO'
                                        elif SSkill == 'css3':
                                            SSkill = 'CSS3'
                                        elif SSkill == 'xml':
                                            SSkill = 'XML'
                                        elif SSkill == 'gae':
                                            SSkill = 'GAE'

                                        else:
                                            SSkill = SSkill.title()
                                        SKillSet.append(SSkill)
                                        i = i + 1

                                    # Removing Duplicates
                                    i = 0
                                    while i < len(SKillSet):
                                        Skill = SKillSet[i]
                                        j = i + 1
                                        while j < len(SKillSet):
                                            if Skill == SKillSet[j]:
                                                SKillSet.remove(Skill)
                                            j = j + 1
                                        i = i + 1
                                vMilestoneEstimate = int(math.floor(int(listJobBudget[0]) * 0.75))
                                vMilestoneMarker = 75
                                vSponsorBid = 0
                                logging.info('BIDDING ACTIVATED FOR ALL FREELANCE JOBS')
                                vFreelanceJobBid = int(math.floor(int(listJobBudget[0]) + (0.1 * int(listJobBudget[1]))))
                                vFreelanceJobBid = str(vFreelanceJobBid)
                                template = template_env.get_template('/templates/fbiddingform.html')
                                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL':  logout_url,'ActivateGetMore': 'No',
                                           'vJobSubmitCredit': fSubscriptions.readJobSubmissionCredit(), 'vBiddingCredit': fSubscriptions.readBiddingCredit(),
                                           'vProfilePromoCredit': fSubscriptions.readProfilePromoCredit(), 'vFreelanceJobTitle': fFreelanceJob.readstrJobTitle(),
                                           'vFreelanceJobDefinition': fFreelanceJob.readJobDefinition(), 'vFreelanceJobNotes': fFreelanceJob.readNotes(),
                                           'vFreelanceJobReference': fFreelanceJob.strJobReference, 'SkillList': SKillSet,
                                           'vFreelanceJobMinBudget': listJobBudget[0], 'vFreelanceJobMaxBudget': listJobBudget[1],
                                           'vFreelanceJobBid': vFreelanceJobBid ,'vMilestoneEstimate' : vMilestoneEstimate,
                                           'vSponsorBid': vSponsorBid, 'vMilestoneMarker': vMilestoneMarker}
                                self.response.write(template.render(context))
                            # display the bidding form with all the variables and allow the user to create a bid
                        else:
                            logging.info(self._BiddingClosedOn)
                            context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL':  logout_url, 'Usermessage': self._BiddingClosedOn, 'ActivateGetMore': 'Yes'}
                            self.response.write(template.render(context))
                    else:
                        logging.info('SECOND ONE :' + self._BiddingClosedOn)
                        context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'Usermessage': self._BiddingClosedOn, 'ActivateGetMore': 'Yes'}
                        self.response.write(template.render(context))
                else:
                    logging.info(self._FreelanceJobNoLongerExist + tStrJobReference)
                    context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'Usermessage': self._FreelanceJobNoLongerExist}
                    self.response.write(template.render(context))
            else:
                logging.info(self._clsReferenceDonotExist)
                User.clsReference.writeUsername(Guser.nickname())
                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'Usermessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))


        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/freelancejobs.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))


class FreelancingJobsEmployersSubmitHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):

        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/submitfreelancejobs.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                VerifiedAccount = result.readIsUserVerified()
                if not(VerifiedAccount == self._generalError):
                    if VerifiedAccount == True:
                        User.clsReference.writeUsername(result.readUsername())
                        findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                        results = findrequest.fetch(limit=self._maxQResults)
                        if len(results) > 0:
                            logging.info('SUBSCRIPTIONS FOUND')
                            tSubs = results[0]
                        else:
                            tSubs = Subscriptions()
                            tSubs.assignOwner(User._pkeyvalue)
                            tSubs.put()
                            logging.info('SUBSCRIPTIONS NOT FOUND')
                        KeyRef = str(User._pkeyvalue)
                        findrequest = db.Query(AccountDetails).filter('IndexReference =', KeyRef)
                        results = findrequest.fetch(limit=1)
                        if len(results) > 0:
                            context = {'vUsername': User.clsReference.readUsername(), 'logingURL': login_url, 'logoutURL': logout_url,
                                   'vJobSubmitCredit': tSubs.readJobSubmissionCredit(), 'vBiddingCredit': tSubs.readBiddingCredit(),
                                   'vProfilePromoCredit': tSubs.readProfilePromoCredit() }
                        else:
                            MemberMessage = self._clsAccountDetailsDoNotExist
                            context = {'vUsername': User.clsReference.readUsername(), 'logingURL': login_url, 'logoutURL': logout_url,
                                   'MemberMessage': MemberMessage}

                    else:
                        User.clsReference.writeUsername(result.readUsername())
                        MemberMessage = self._UserNotVerified

                        context = {'vUsername': User.clsReference.readUsername(), 'logingURL': login_url, 'logoutURL': logout_url,
                                   'MemberMessage': MemberMessage}

            else:
                User.clsReference.writeUsername((Guser.nickname()))
                User.clsReference.writeVerEmail(Guser.email())
                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}


            self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/submitfreelancejobs.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))



    def post(self,):

        Guser = users.get_current_user()

        if Guser:
            if isGoogleServer:
                ReferenceNum = Guser.user_id()
            else:
                ReferenceNum = self._tempCode

            result = User.GetReferenceByRefNum(ReferenceNum)

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/FjobsSubmissionResults.html')

            if not(result == self.undefined) and not(result == self._referenceDoNotExist) and not(result == self._generalError):
                User.clsReference.writeUsername(result.readUsername())
                User.clsReference.writeDateTimeVerified(result.readDatetimeVerified())
                User.clsReference.writeVerEmail(result.readVerEmail())
                User.clsReference.writeReference(result.readReference())
                User.clsReference.writeIDNumber(result.readIDNumber())
                User.clsReference.writeIsUserVerified(result.readIsUserVerified())
                User.clsReference.writeLogoPhoto(result.readLogoPhoto())
                User.clsReference.writePassword(result.readPassword())

                tFreelanceJob = FreelanceJobs()
                logging.info(User._pkeyvalue)

                result = tFreelanceJob.clsJob.writeJobOwner()  # The Owner of the freelance job

                logging.info(str(result))
                result = tFreelanceJob.clsJob.writeOwnerReference(ReferenceNum)
                logging.info(str(result))


                vJobKindr = self.request.get('vJobKindr')



                # Private Job
                if vJobKindr == tFreelanceJob.clsJob._lstJobKinds[1]:
                    tFreelanceJob.clsJob.strJobKind = tFreelanceJob.clsJob._lstJobKinds[1]


                vAttribute = self.request.get('vJobAttrib_')

                if vAttribute ==  tFreelanceJob.clsJob._lstJobAttributes[0]:
                    tFreelanceJob.clsJob.strJobAttribute = 'sponsored jobs'


                if vAttribute ==  tFreelanceJob.clsJob._lstJobAttributes[1]:
                    tFreelanceJob.clsJob.strJobAttribute = 'urgent jobs'


                if vAttribute ==  tFreelanceJob.clsJob._lstJobAttributes[2]:
                    tFreelanceJob.clsJob.strJobAttribute = 'premium jobs'

                if vAttribute == tFreelanceJob.clsJob._lstJobAttributes[3]:
                    tFreelanceJob.clsJob.strJobAttribute = 'general jobs'


                if (tFreelanceJob.clsJob.calcJobCost(inJobKind=vJobKindr, inJobAttribute=vAttribute) == self._generalError):
                    tFreelanceJob.clsJob.strJobCost = '0'


                #Jobtype is freelance jobs as default

                vBudget = self.request.get('vBudget')

                if vBudget == tFreelanceJob.clsJob._lstFreelanceJobBudget[1]:
                    tFreelanceJob.clsJob.strFreelanceJobBudget = tFreelanceJob.clsJob._lstFreelanceJobBudget[1]

                if vBudget == tFreelanceJob.clsJob._lstFreelanceJobBudget[2]:
                    tFreelanceJob.clsJob.strFreelanceJobBudget = tFreelanceJob.clsJob._lstFreelanceJobBudget[2]

                if vBudget == tFreelanceJob.clsJob._lstFreelanceJobBudget[3]:
                    tFreelanceJob.clsJob.strFreelanceJobBudget = tFreelanceJob.clsJob._lstFreelanceJobBudget[3]

                if vBudget == tFreelanceJob.clsJob._lstFreelanceJobBudget[4]:
                    tFreelanceJob.clsJob.strFreelanceJobBudget = tFreelanceJob.clsJob._lstFreelanceJobBudget[4]

                if vBudget == tFreelanceJob.clsJob._lstFreelanceJobBudget[5]:
                    tFreelanceJob.clsJob.strFreelanceJobBudget = tFreelanceJob.clsJob._lstFreelanceJobBudget[5]

                # Create a Skills class and read the skills from the form and then create a skills class
                # After creating a skills class store the key on the reference field of our job class

                # the job class can help me create the skills class

                vAfrikaans = self.request.get('vAfrikaans')
                if vAfrikaans:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='afrikaans')

                vEnglishUS = self.request.get('vEnglishUS')

                if vEnglishUS:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='englishus')

                vEnglishUK = self.request.get('vEnglishUK')
                if vEnglishUK:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='englishuk')

                vSpanish = self.request.get('vSpanish')
                if vSpanish:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='spanish')

                vFrench = self.request.get('vFrench')
                if vFrench:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='french')

                vPortuguese = self.request.get('vPortuguese')
                if vPortuguese:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill(strinput='portuguese')

                vArticleWriting = self.request.get('vArticleWriting')
                if vArticleWriting:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('article writing')

                vProofReading = self.request.get('vProofReading')
                if vProofReading:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('proof reading')

                vCopyWriting = self.request.get('vCopyWriting')
                if vCopyWriting:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('copy writing')




                vWebsiteDevelopment = self.request.get('vWebsiteDevelopment')
                if vWebsiteDevelopment:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('website development')

                vLandingPage = self.request.get('vLandingPage')
                if vLandingPage:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('landing page development')

                vAndroidApp = self.request.get('vAndroidApp')
                if vAndroidApp:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('android')

                vWebApp = self.request.get('vWebApp')
                if vWebApp:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('webapp')

                vHTML = self.request.get('vHTML')
                if vHTML:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('html')

                vCSS3 = self.request.get('vCSS3')
                if vCSS3:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('css3')

                vXML = self.request.get('vXML')
                if vXML:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('xml')

                vSEO = self.request.get('vSEO')
                if vSEO:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('seo')

                vJAVA = self.request.get('vJAVA')
                if vJAVA:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('java')

                vJavaScript = self.request.get('vJavaScript')
                if vJavaScript:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('java script')

                vPHP = self.request.get('vPHP')
                if vPHP:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('php')

                vPython = self.request.get('vPython')
                if vPython:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('python')

                vPerl = self.request.get('vPerl')
                if vPerl:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('perl')

                vCsharp = self.request.get('vCsharp')
                if vCsharp:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('csharp')

                vGAE = self.request.get('vGAE')
                if vGAE:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('gae')

                vJinja2 = self.request.get('vJinja2')
                if vJinja2:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('jinja2')

                vDjango = self.request.get('vDjango')
                if vDjango:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('django')

                vGo = self.request.get('vGo')
                if vGo:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('go')

                vJQuery = self.request.get('vJQuery')
                if vJQuery:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('jquery')

                vWordPress = self.request.get('vWordPress')
                if vWordPress:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('wordpress')

                vJoomla = self.request.get('vJoomla')
                if vJoomla:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('joomla')

                vCPlusPlus = self.request.get('vCPlusPlus')
                if vCPlusPlus:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('cplusplus')

                vC = self.request.get('vC')
                if vC:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('c')

                vNet = self.request.get('vNet')
                if vNet:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('net')

                vPascal = self.request.get('vPascal')
                if vPascal:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('pascal')

                vFreePascal = self.request.get('vFreePascal')
                if vFreePascal:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('freepascal')

                vDelphi = self.request.get('vDelphi')
                if vDelphi:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('delphi')

                vVisualBasic = self.request.get('vVisualBasic')

                if vVisualBasic:
                    tFreelanceJob.clsJob._skillsrequired.AddSkill('visualbasic')


                tFreelanceJob.clsJob.StrSkillsRequired = tFreelanceJob.clsJob._skillsrequired.skills
                logging.info('NEAR')

                tFreelanceJob.clsJob.writeJobDefinition(self.request.get('vJobDefinitionr'))
                logging.info('SO WHAT')
                tFreelanceJob.clsJob.writestrJobTitle(self.request.get('vJobTitler'))
                tFreelanceJob.clsJob.writeNotes(self.request.get('vNotesr'))

                tFreelanceJob._jobPkey = tFreelanceJob.clsJob.put()
                tFreelanceJob.clsJob.strJobReference = str(tFreelanceJob.clsJob.key())
                tFreelanceJob.clsJob.put()

                findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tSubs = results[0]
                else:
                    tSubs = Subscriptions()
                    if not(User._pkeyvalue == self.undefined):
                        tSubs.assignOwner(User._pkeyvalue)
                        tSubs.put()
                    else:
                        findrequest = db.Query(Reference).filter('strReferenceNum =', ReferenceNum)
                        results = findrequest.fetch(limit=self._maxQResults)
                        tRef = results[0]
                        tSubs.assignOwner(tRef.key())
                        tSubs.put()




                tJSubCredit = tSubs.readJobSubmissionCredit()




                #Continue creating

                # Load the complete reference class from the store

                # Get all the form values and store them on the _constants using the jobs class from the freelance jobs class

                # Create a freelance job and note to turn of the bidding constant. it will be turned on once the job has been paid for.
                if not(tFreelanceJob._jobPkey == self.undefined):
                    if len(tFreelanceJob.clsJob.StrSkillsRequired) > 0:
                        SubmissionResult = 'Freelance Jobs Succesfully Submitted'
                        ActivateBidPayment = 'Yes'
                        JobSubmitted = tFreelanceJob.clsJob
                    else:
                        SubmissionResult = 'Required Skills Not Saved freelance job not created'
                        db.delete(tFreelanceJob._jobPkey)
                        ActivateBidPayment = 'No'
                        JobSubmitted = self.undefined
                else:
                    SubmissionResult = 'Freelance Job Not Created please submit your job again'
                    ActivateBidPayment = 'No'
                    JobSubmitted = self.undefined

                context = {'vUsername': User.clsReference.readUsername(), 'logingURL': login_url, 'logoutURL': logout_url, 'SubmissionResult': SubmissionResult, 'ActivateBidPayment': ActivateBidPayment, 'JobReference': tFreelanceJob.clsJob.strJobReference, 'JobSubmitted': JobSubmitted,'vAvailableCredit': tJSubCredit}

            else:
                context = {'loginURL': login_url, 'logoutURL': logout_url}

            self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/submitfreelancejobs.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))








class MarketPlaceHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode


                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/marketplace.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/marketplace.html')
                    User.clsReference.writeVerEmail(Guser.email())
                    User.clsReference.writeUsername(Guser.nickname())
                    ActivateSub = 'Yes'
                    MemberMessage = self._CompleteSubscriptionForm


                    context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage,
                               'ActivateSub': ActivateSub}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                MemberMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                template = template_env.get_template('/templates/marketplace.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage, 'ActivateLogin': ActivateLogin}
                self.response.write(template.render(context))



class AffiliatesHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/affiliates.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/affiliates.html')
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())
                    MemberMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'

                    context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage,
                               'ActivateSub': ActivateSub}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/affiliates.html')
                MemberMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'
                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage,
                           'ActivateLogin': ActivateLogin}
                self.response.write(template.render(context))


class JobmarketHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/jobmarket.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/jobmarket.html')
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())
                    MemberMessage = self._CompleteSubscriptionForm
                    ActivateSub = 'Yes'

                    context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage,
                               'ActivateSub': ActivateSub}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/jobmarket.html')
                MemberMessage = self._userNotLoggedin
                ActivateLogin = 'Yes'

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage,
                           'ActivateLogin': ActivateLogin}
                self.response.write(template.render(context))


class BrowsePortfolioHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/BrowsePortfolios.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())


                    template = template_env.get_template('/templates/BrowsePortfolios.html')

                    context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())


                template = template_env.get_template('/templates/BrowsePortfolios.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))


class FreelanceEmployersSubmissionResultsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def post(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):


                User.clsReference.writeUsername(result.readUsername())
                User.clsReference.writeVerEmail(result.readVerEmail())
                User.clsReference.writeDateTimeVerified(result.readDatetimeVerified())
                User.clsReference.writeIDNumber(result.readIDNumber())
                User.clsReference.writeIsUserVerified(result.readIsUserVerified())
                User.clsReference.writeLogoPhoto(result.readLogoPhoto())
                User.clsReference.writeReference(result.readReference())

                PKEYFreelanceJob = self.request.get('JobReference')

                ref = str(User._pkeyvalue)
                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)
                logging.info('CHECKING TO SEE AS TO WEATHER ACCOUNT DETAILS WHERE FOUND: ' + str(len(results)))

                if (len(results) > 0):
                    result = results[0]  # Wallet Exist and Freelance Job
                    tAccountDetails = AccountDetails.get(result.key())
                    tJob = Job.get(PKEYFreelanceJob)

                    findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=self._maxQResults)
                    logging.info('CHECKING TO SEE IF SUBSCRIPTIONS WHERE FOUND: ' + str(len(results)))
                    if len(results) > 0:
                        tSubs = results[0]


                        if int(tSubs.readJobSubmissionCredit()) >= int(tJob.readJobCost()):
                            #Make Atomic
                            tJob.BidsActivated = True

                            # Returns the present date and time
                            today = datetime.datetime.now()
                            # Writing The start date of bid display
                            tJob.writeDateTimeOfBidsDisplay(today)

                            #Advancing Date to Deactivate Bid by 30 days
                            #todo-allow the employer to close bidding on any job when it is awarded.

                            BidEndDateTime = today
                            BidEndDateTime = self.Advance30Days(indate=BidEndDateTime)
                            tJob.writeDateTimeEndBidorRemove(clsinput=BidEndDateTime) # Writing the date to close bidding on the

                            # Saving the edited job
                            if tJob.writeJobType(tJob._lstJobTypes[2]):
                                tJob.put()
                            else:
                                tJob.put()

                            tCredit = tSubs.readJobSubmissionCredit()
                            tCredit = str(int(tCredit) - int(tJob.readJobCost()))
                            tRes = tSubs.writeJobSubmissionCredit(tCredit)
                            if tRes == True:
                                tSubs.put()
                            else:
                                tSubs.writeJobSubmissionCredit(tCredit)

                            #End Atomic
                            #Show Job Submission Success and Bid Activated

                            ActivateBidPayment = 'No'
                            SubmissionResult = 'Job Succesfully Submitted and Bidding Activated'
                            template = template_env.get_template('/templates/FjobsSubmissionResults.html')
                            context = context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url,
                                                 'logoutURL': logout_url, 'ActivateBidPayment': ActivateBidPayment, 'SubmissionResult': SubmissionResult,
                                                 'JobSubmitted': tJob, 'vAvailableCredit': tCredit}
                            self.response.write(template.render(context))
                        else:
                            template = template_env.get_template('/templates/Services.html')
                            CreditRequested = int(tJob.readJobCost()) - int(tSubs.readJobSubmissionCredit())
                            CreditRequested = str(CreditRequested)

                            context = context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                                 'JobSubmissionCredit': CreditRequested, 'vBankNamer': tAccountDetails.readNameOfInstitution(),
                                                 'vAccountTyper': tAccountDetails.readAccountType(), 'vAccountNumberr': tAccountDetails.readAccountNumber(),
                                                 'vBranchCoder': tAccountDetails.readBranchCode(), 'vPayPalEmailr': tAccountDetails.readPayPalEmail(),
                                                 'vBalancer': tAccountDetails.readInternalBalance()}
                            self.response.write(template.render(context))


                            #Show Top-UP
                    else:
                        template = template_env.get_template('/templates/Services.html')
                        context = context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                             'vBankNamer': tAccountDetails.readNameOfInstitution(),
                                             'vAccountTyper': tAccountDetails.readAccountType(), 'vAccountNumberr': tAccountDetails.readAccountNumber(),
                                             'vBranchCoder': tAccountDetails.readBranchCode(), 'vPayPalEmailr': tAccountDetails.readPayPalEmail(),
                                             'vBalancer': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))

                else:
                    template = template_env.get_template('/templates/EditAccountDetails.html')
                    context = context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))

                    # Account Details Do Not Exist

            else:
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/FjobsSubmissionResults.html')
                context = context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}
                self.response.write(template.render(context))

        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/FjobsSubmissionResults.html')
            context = context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))































class FreelanceJobsSubscriptionsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def post(self):
        try:
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')


            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                User.clsReference.writeReference(reference)

                UReference = User.GetReferenceByRefNum(reference)

                # Every User has a subscriptions class read it for each user and populate the services form
                # Allow the user to change their subscriptions once each month

                MSubscriptions = Subscriptions()

                BidPackage = self.request.get('vBidPackages')
                ProfilePromo = self.request.get('vProfilePromoPackages')
                JobSubmissions = self.request.get('vJobSubmissionPack')

                # test if the Reference Class is found
                # test if user has been Verified

                if not(User._pkeyvalue == self.undefined):
                    if UReference.readIsUserVerified:

                        findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                        results = findrequest.fetch(limit=self._maxQResults)
                        if len(results) > 0:
                            MSubscriptions = results[0]

                            if MSubscriptions.readIsValid():
                                logging.info('Bid Package :' + str(BidPackage))
                                logging.info('PROFILE PROMO :' + str(ProfilePromo))
                                logging.info('JOB SUBMISSION :' + str(JobSubmissions))
                                tSubAmount =  MSubscriptions.CalculateTotalSubAmount(inBidCredit=BidPackage, inProfileCredit=ProfilePromo, inJobSubCredit=JobSubmissions)

                                ref = str(User._pkeyvalue)
                                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                                results = findrequest.fetch(limit=self._maxQResults)
                                if len(results) > 0:
                                    UAccount = results[0]
                                    logging.info('INTERNAL BALANCE: ' + UAccount.readInternalBalance())
                                    logging.info('TOTAL SUBSCRIPTION AMOUNT: ' + str(tSubAmount))
                                    if int(UAccount.readInternalBalance()) >= tSubAmount:
                                        tBal = int(UAccount.readInternalBalance()) - tSubAmount
                                        if UAccount.writeInternalBalance(tBal) == True:
                                            UAccount.put()
                                            logging.info('INTERNAL BALANCE WRITTEN NEW BALANCE: ' + str(tBal))
                                        # Save The Current Subscription Values

                                        MSubscriptions.put() #This Assumes that all subscription values have already been saved.

                                        # Consider Loading a form with the current total user subscription values
                                        showMessage = 'Subscription Credits added successfully'
                                        #todo-Load a form with the current total subscription credits for the user and
                                        #todo- thank the user for succesfully loading the credits.
                                        #todo- you must also note that every user will get additional free credits every month
                                        showMessage = 'Credits Purchased Succesfully'
                                        #Todo- Design a template for issuing balances on credits
                                        template = template_env.get_template('/templates/SubscriptionResults.html')
                                        context = {'vUsername': UReference.readUsername(), 'loginURL': login_url,
                                                   'logoutURL': logout_url, 'MemberMessage': showMessage,
                                                   'vBankName': UAccount.readNameOfInstitution(), 'vAccountType': UAccount.readAccountType(),
                                                   'vAccountNumber': UAccount.readAccountNumber(), 'vBranchCode': UAccount.readBranchCode(),
                                                   'vPayPalEmail': UAccount.readPayPalEmail(),
                                                   'vBalance': UAccount.readInternalBalance(), 'vFreelanceJobSubCredit': MSubscriptions.readJobSubmissionCredit(),
                                                   'vProfilePromoCredit': MSubscriptions.readProfilePromoCredit(), 'vBidsCredit': MSubscriptions.readBiddingCredit()}
                                        self.response.write(template.render(context))
                                    else:
                                        showMessage = self._InsufficientFunds
                                        template = template_env.get_template('/templates/TopUp.html')
                                        context = {'vUsername': UReference.readUsername(), 'loginURL': login_url,
                                                   'logoutURL': logout_url, 'MemberMessage': showMessage,
                                                   'vBankName': UAccount.readNameOfInstitution(), 'vAccountType': UAccount.readAccountType(),
                                                   'vAccountNumber': UAccount.readAccountNumber(), 'vBranchCode': UAccount.readBranchCode(),
                                                   'vPayPalEmail': UAccount.readPayPalEmail(),
                                                   'vBalance': UAccount.readInternalBalance()}
                                        self.response.write(template.render(context))
                                else: # Theres no account associated with this user launch a screen to create a new account
                                    showMessage = self._clsAccountDetailsDoNotExist
                                    template = template_env.get_template('/templates/EditAccountDetails.html')
                                    context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': showMessage}
                                    self.response.write(template.render(context))

                            else: # The Current subscriptions class is invalid inform the user and tell him/her to retry later
                                logging.info('CURRENT SUBSCRIPTIONS CLASS IS INVALID')
                        else: # There's no subscriptions class create a new one assign it to the present user and add the default
                            # Subscription values, and then present the results to the user.
                            if MSubscriptions.assignOwner(UReference.key()):
                                MSubscriptions.put()
                                showMessage = 'Freelance Subscription values refreshed please try again later'
                                template = template_env.get_template('/templates/Services.html')
                                context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'fMemberMessage': showMessage}
                                self.response.write(template.render(context))
                            else:
                                MSubscriptions.put()
                                showMessage = 'Failed to create freelance jobs subscription values'
                                template = template_env.get_template('/templates/Services.html')
                                context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'fMemberMessage': showMessage}
                                self.response.write(template.render(context))


                            logging.info('Create a subscriptions class')


                    else: # user not verified lauch the verification form and allow the user to verify his/her accout
                        pass
                else: # User Reference Class do not exist launch a form to enter personal information and inform the user of this
                    pass
            else:
                # User not logged in
                # Inform the user and enable them to login
                pass
        except:
            logging.info('EXCEPTION OCCURING WHILE PURCHASING CREDITS')
            pass



class FreelancingJobsEmployersReviewHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                Uref = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):

                    findrequest = db.Query(Job).filter('strOwnerReference =', reference)
                    results = findrequest.fetch(limit=self._maxQResults)
                    JobList = results
                    logging.info('Length of Review Results :' + str(len(results)))

                    i = 0
                    fJobList = []
                    while i < len(JobList):
                        tJob = JobList[i]
                        if tJob.readBidsActivated() == True:
                            fJobList.append(tJob)
                        i = i + 1

                    JobList = fJobList

                    findrequest1 = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                    results = findrequest1.fetch(limit=1)
                    if len(results) > 0:
                        USubs = results
                    else:
                        USubs = Subscriptions()

                    if len(JobList) > 0:
                        #try finding all the bids for each job
                        FJob = JobList[0]
                        FJobKey = FJob.key()
                        ShowforJob = str(FJobKey)
                        memBidreview = reference + 'bidreview'
                        memcache.set(memBidreview, ShowforJob, time=300000)

                        template = template_env.get_template('/templates/fjobreview.html')
                        logging.info('THE BID REVIEW PROCESS LOADING...')
                        context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'JobList': JobList}

                        self.response.write(template.render(context))
                    else:
                        Usermessage = 'You have no Active Jobs to Review The Bidding Process on'
                        template = template_env.get_template('/templates/fjobreview.html')
                        logging.info('BID REVIEW PROCESS NEVER LOADED NO JOBS ON THE BIDING PROCESS')
                        context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'Usermessage': Usermessage}

                        self.response.write(template.render(context))
                else:
                    logging.info('USER REFERENCE CLASS DO NOT EXIST')
            else:
                logging.info('USER NOT LOGGED IN TO GOOGLE')
        except:
            logging.info('THROWING EXCEPTIONS LAUNCHING THE BID REVIEW PROCESS...')

    def post(self):

        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ShowforJob = self.request.get('JobReferencer')
                logging.info('JOB REFERENCER :' + ShowforJob)
                memBidreview = reference + 'bidreview'
                memcache.set(memBidreview, ShowforJob, time=300000)

                Uref = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):

                    findrequest = db.Query(Job).filter('strOwnerReference =', reference).filter('BidsActivated =', True)
                    results = findrequest.fetch(limit=self._maxQResults)
                    logging.info('Length of Review Results :' + str(len(results)))

                    if len(results) > 0:
                        JobList = results
                        #try finding all the bids for each job
                        i = 0
                        while i < len(JobList):
                            tjob = JobList[i]
                            if tjob.strJobReference == ShowforJob:
                                JobList.remove(tjob)
                                JobList.append(tjob)
                                JobList.reverse()
                                i = len(JobList)
                            i = i + 1


                        template = template_env.get_template('/templates/fjobreview.html')
                        context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'JobList': JobList}
                        self.response.write(template.render(context))
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except:
            pass

class fjobslisthandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):

        findrequest = db.Query(Job).filter('strJobType =', 'freelance jobs')
        results = findrequest.fetch(limit=self._maxQResults)
        if len(results) > 0:

            template = template_env.get_template('/templates/fjobslist.html')
            context = {'freelancejobslist': results}
            self.response.write(template.render(context))
        else:
            template = template_env.get_template('/templates/fjobslist.html')
            context = {'freelancejobslist': results}
            self.response.write(template.render(context))





class femployerJobListHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):

        Guser = users.get_current_user()
        results = []
        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode


            findrequest = db.Query(Job).filter('strOwnerReference =', reference)
            results = findrequest.fetch(limit=self._maxQResults)
            if len(results) > 0:

                template = template_env.get_template('/templates/fjobslist.html')
                context = {'freelancejobslist': results}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('/templates/fjobslist.html')
                context = {'freelancejobslist': results}
                self.response.write(template.render(context))
        else:
           template = template_env.get_template('/templates/fjobslist.html')
           context = {'freelancejobslist': results}
           self.response.write(template.render(context))


class FreelancingJobsPlaceBidHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        try:
            logging.info('ARE WE EVEN ONLINE')
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            if Guser:
                logging.info('ARE WE EVEN ONLINE')
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                logging.info('USER REFERENCE : ' + reference)

                if not(User._pkeyvalue == self.undefined):
                    tFJobReference = self.request.get('vFreelanceJobReferencer')
                    tFMinJobBudget = self.request.get('vFreelanceJobMinBudgetr')
                    tFMaxJobBudget = self.request.get('vFreelanceJobMaxBudgetr')
                    tFYourFJobBid = self.request.get('vFreelanceBidr')
                    tFJobMilestone = self.request.get('vFreelanceMilestoner')
                    tFMilestoneMarker = self.request.get('vMilestoneMarkerr')
                    tFBidSponsorCredit = self.request.get('vSponsorBidr')
                    tFBidNotes = self.request.get('vFreelanceBiddingNotesr')
                    tfBiddingCredit = self.request.get('vBiddingCreditr')



                    logging.info('JOB REFERENCE: ' + tFJobReference)
                    logging.info('MIN JOB BUDGET: ' + tFMinJobBudget)
                    logging.info('MAX JOB BUDGET: ' + tFMaxJobBudget)
                    logging.info('YOUR FREELANCE JOB BID: ' + tFYourFJobBid)
                    logging.info('MILESTONE PAYMENT: ' + tFJobMilestone)
                    logging.info('MILESTONE MARKER: ' + tFMilestoneMarker)
                    logging.info('BID SPONSORED: ' + tFBidSponsorCredit)
                    logging.info('BID NOTES: ' + tFBidNotes)
                    logging.info('BIDDING CREDIT: ' + tfBiddingCredit )
                    self._bidJobPkey = tFJobReference

                    tBids = Bids()
                    logging.info('Bids class is created')
                    findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=1)
                    logging.info('Subscriptions class returned :' + str(len(results)))
                    if len(results) > 0:
                        fSubs = results[0]

                    # (self, inBidAmount, inBidNotes, inBidOnThisJob, inMilestone, inMilestoneMarker):
                    tbidpsponsor = int(tFBidSponsorCredit)
                    logging.info(str(tbidpsponsor))
                    tbiddingcredit = int(tfBiddingCredit)
                    logging.info(str(tbiddingcredit))


                    findrequest = db.Query(Job).filter('strJobReference =', tFJobReference)
                    results = findrequest.fetch(limit=1)
                    fJob = results[0]

                    if fJob.readBidsActivated == True:

                        if int(tbidpsponsor) <= int(tbiddingcredit):

                            BidResult = tBids.createBid(inBidAmount=tFYourFJobBid, inBidNotes=tFBidNotes, inBidOnThisJob=tFJobReference, inMilestone=tFJobMilestone, inMilestoneMarker=tFMilestoneMarker, inSponsorCredit=tFBidSponsorCredit)

                            # Subtract The Sponsor Credits
                            tCredit = int(fSubs.readBiddingCredit()) - int(tFBidSponsorCredit)
                            if fSubs.writeBiddingCredit(tCredit):
                                fSubs.put()
                            elif fSubs.writeBiddingCredit(tCredit):
                                fSubs.put()

                        else:
                            BidResult = self._NotEnoughCreditToSponsorBid





                        if BidResult == True:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Bid Created Succesfully'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message,
                                       'vJobSubmitCredit': fSubs.readJobSubmissionCredit(), 'vBiddingCredit': fSubs.readBiddingCredit(),
                                       'vProfilePromoCredit': fSubs.readProfilePromoCredit(), 'vFreelanceJobTitle': fJob.readstrJobTitle(),
                                       'vFreelanceJobDefinition': fJob.readJobDefinition(), 'vFreelanceJobNotes': fJob.readNotes(),
                                       'vFreelanceJobReference': tFJobReference, 'SkillList': fJob.readSkillsRequired(),
                                       'vFreelanceJobMinBudget': tFMinJobBudget, 'vFreelanceJobMaxBudget': tFMaxJobBudget,
                                       'vFreelanceJobBid': tFYourFJobBid, 'vMilestoneEstimate': tFJobMilestone,
                                       'vMilestoneMarker': tFMilestoneMarker, 'vSponsorBid': tFBidSponsorCredit, 'vFreelanceBiddingNotes': tFBidNotes
                                        }
                            self.response.write(template.render(context))
                            # Bid is created
                            # Show The Same Bids Form with User Bid Showed and Bidding closed and Editing Enabled
                            logging.info('SUCCESS CREATING BIDS')
                        elif BidResult == self._ErrorCreatingBid:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Error Creating Bid'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))

                            logging.info('FAILURE CREATING BIDS : ' + self._ErrorCreatingBid)

                            # Failure Creating new Bid
                        elif BidResult == self._CannotBidOnOwnJob:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Fialure Creating Bid you cannot BID on your own freelance job'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))

                            logging.info('FAILURE CREATING BIDS : ' + self._CannotBidOnOwnJob)

                        elif BidResult == self._generalError:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Ther was a General Error while creating BID please try again later'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))
                            logging.info('FAILURE CREATING BIDS : ' + self._generalError)

                        elif BidResult == self._userNotLoggedin:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Bid Created Succesfully'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))

                            logging.info('FAILURE CREATING BIDS : ' + self._userNotLoggedin)

                        elif BidResult == self._NotEnoughCreditToSponsorBid:

                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = self._NotEnoughCreditToSponsorBid
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))



                        else:
                            template = template_env.get_template('templates/fbiddingform.html')
                            Message = 'Bid Created Succesfully'
                            context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,'Message': Message}
                            self.response.write(template.render(context))

                            BidResulter = BidResult[0]
                            #Display the Existing Bid
                    else:
                        logging.info('BIDDING CLOSED ON THIS JOB')
                else:
                    logging.info('USER NOT COMPLETELY SUBSCRIBED')
                    pass
                    # User cot completely subscribed he/she must create their records
            else:
                logging.info('USER NOT LOGGED IN ')
                pass
                # User not loggedin
        except:
            logging.info('THROWING EXCEPTIONS CREATING BIDS 12345')
            pass
            # An Error Occurred


class activebidshandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        logging.info('ACTIVE BIDS IS BEING CALLED NICELY')
        # memcache.set(ReferenceNum, tStrJobReference, time=300000)
        Guser = users.get_current_user()
        if isGoogleServer:
            reference = Guser.user_id()
        else:
            reference = self._tempCode

        self._bidJobPkey = memcache.get(reference)
        if not(self._bidJobPkey == self.undefined):

            findrequest = db.Query(Bids).filter('BidonThisJob =', self._bidJobPkey)
            results = findrequest.fetch(limit=self._maxQResults)


            template = template_env.get_template('/templates/activebids.html')
            context = {'BidsList': results}
            self.response.write(template.render(context))
        else:
            template = template_env.get_template('/templates/activebids.html')
            context = {'Message': 'There are no Other Bids on this Job'}
            self.response.write(template.render(context))





class BidsProcessHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        logging.info('BIDS PROCESS IS BEING CALLED NICELY')
        # memcache.set(ReferenceNum, tStrJobReference, time=300000)
        Guser = users.get_current_user()
        if isGoogleServer:
            reference = Guser.user_id()
        else:
            reference = self._tempCode

        memBidreview = reference + 'bidreview'
        self._bidJobPkey = memcache.get(memBidreview)
        if not(self._bidJobPkey == self.undefined):

            findrequest = db.Query(Bids).filter('BidonThisJob =', self._bidJobPkey)
            results = findrequest.fetch(limit=self._maxQResults)
            BidList = results
            tFreelancerList = []
            for Bid in BidList:
                tReference = Bid.readPBidder()
                tFreelancer = User.GetReferenceByRefNum(tReference)
                tFreelancerList.append(tFreelancer)

            if len(BidList) > 0:
                template = template_env.get_template('/templates/BidProcess.html')
                context = {'BidsList': BidList, 'FreelancerList': tFreelancerList }
                self.response.write(template.render(context))
            else:
                Message = 'There are no Active Bids at the Moment'
                template = template_env.get_template('/templates/BidProcess.html')
                context = {'BidsList': BidList, 'FreelancerList': tFreelancerList,'Message': Message }
                self.response.write(template.render(context))

        else:
            template = template_env.get_template('/templates/BidProcess.html')
            context = {'Message': 'There are no Other Bids on this Job'}
            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if isGoogleServer:
            reference = Guser.user_id()
        else:
            reference = self._tempCode

        tFreelancer = self.request.get('vFreelancerr')
        tBid = self.request.get('vBidReferencer')
        tFreelanceJob = self.request.get('vBidOnThisJobr')
        tAction = self.request.get('vBidProcess')
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        Uref = User.GetReferenceByRefNum(reference)


        if tAction == 'award':
            logging.info('BID AWARD HAS BEEN CALLED')
            if (len(tFreelancer) > 0) and (len(tBid) > 0) and (len(tFreelanceJob) > 0):
                FJob = Job.get(tFreelanceJob)
                if FJob.readisValid():
                    if FJob.writeAwardedTo(strinput=tFreelancer) and FJob.setDateTimeAwarded():
                        FJob.BidsActivated = False
                        FJob.put()
                        BBid = Bids.get(tBid)


                        BBid.ShowBid = False
                        logging.info('BID FOUND AND SHOW BID TURNED TO FALSE')
                        BBid.put()
                        BidderReference = BBid.readPBidder()
                        UNames = User.getNamesbyRefNum(BidderReference)
                        UContacts = User.getContactDetailsByRefNum(BidderReference)
                        MemStoreKey = reference + self._AwardedComMessages
                        memcache.set(MemStoreKey, BBid.readBidReference())

                        if not(User._pkeyvalue == self.undefined):

                            tSurname = UNames.readSurname()
                            if tSurname == self._generalError:
                                tSurname = self.undefined

                            tFirstname = UNames.readFirstname()
                            if tFirstname == self._generalError:
                                tFirstname = self.undefined
                            tCell = UContacts.readCell()
                            if tCell == self._generalError:
                                tCell = self.undefined
                            tEmail = UContacts.readEmail()
                            if tEmail == self._generalError:
                                tEmail = self.undefined
                            tSkype = UContacts.readSkype()
                            if tSkype == self._generalError:
                                tSkype = self.undefined
                            tFax = UContacts.readFax()
                            if tFax == self._generalError:
                                tFax = self.undefined
                            tBlog = UContacts.readBlog()
                            if tBlog == self._generalError:
                                tBlog = self.undefined
                            tWebsite = UContacts.readWebsite()
                            if tWebsite == self._generalError:
                                tWebsite = self.undefined
                            tFacebook = UContacts.readFacebook()
                            if tFacebook == self._generalError:
                                tFacebook = self.undefined
                            tTwitter = UContacts.readTwitter()
                            if tTwitter == self._generalError:
                                tTwitter = self.undefined
                            tGooglePlus = UContacts.readGooglePlus()
                            if tGooglePlus == self._generalError:
                                tGooglePlus = self.undefined
                            tLinkedIn = UContacts.readLinkedIn()
                            if tLinkedIn == self._generalError:
                                tLinkedIn = self.undefined

                            findrequest = db.Query(Subscriptions).filter('indexReference =', User._pkeyvalue)
                            results = findrequest.fetch(limit=1)
                            if len(results) > 0:
                                USubs = results[0]
                            else:
                                USubs = Subscriptions()

                            template = template_env.get_template('/templates/BidAward.html')
                            context = {'vUsername': Uref.readUsername(), 'logoutURL': logout_url, 'loginURL': login_url,
                                      'vFreelanceJobTitle': FJob.readstrJobTitle(),'vFreelanceJobDefinition': FJob.readJobDefinition(),
                                      'vFreelanceJobCost': FJob.readJobCost(), 'SkillsList': FJob.readSkillsRequired(),'vBidCurrency': BBid.CurrencySymbol,
                                      'vBidAmount': BBid.readBidAmount(), 'vBidPoints':BBid.readBidPoints(), 'vBidSponsor': BBid.readSponsorCredit(),
                                      'vBidNotes': BBid.readBidNotes(),
                                      'vMilestoneCurrency': BBid.CurrencySymbol, 'vMilestoneAmount': BBid.readMilestonePayment(),'vMilestoneMarker': BBid.readMilestoneMarker(),
                                      'vMileStoneNotes': BBid.readMileStoneNotes(),'vFreelancerFirstname': tFirstname,
                                      'vFreelancerSurname': tSurname,'vCell': tCell, 'vEmail': tEmail,
                                      'vSkype': tSkype, 'vFax': tFax,'vBlog': tBlog,
                                      'vWebsite': tWebsite,'vBFacebook': tFacebook,'vBTwitter': tTwitter,
                                      'vBGooglePlus': tGooglePlus, 'vBLinkedIn': tLinkedIn, 'vBidReference': BBid.readBidReference(),
                                      'vJobSubmitCredit': USubs.readJobSubmissionCredit() ,'vBiddingCredit': USubs.readBiddingCredit(), 'vProfilePromoCredit': USubs.readProfilePromoCredit(),}
                            self.response.write(template.render(context))


                # Use this procedure to award the freelance job to a freelancer who made the bid.
                # The award procedure must deactivate the bidding process on the freelance job.
                # The values for the BID, Freelancer who placed the BID, and the freelance job must be passed along.
                # The freelance job must then be awarded to the freelancer in question.

                        # Show status indicating that the job has been awarded and Bidding Closed
            else:
                logging.info('SOME CALLED VALUES ARE NOT RETURNED')
        elif tAction == 'freelancer':  # show freelancer details
            pass

        elif tAction == 'job':  # show freelance job details
            pass
        else:  # indicate to the user that they need to select an action
            pass


class FreelancingJobsEmployersAwarded(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):

        Guser = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')
        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

        Uref = User.GetReferenceByRefNum(reference)
        template = template_env.get_template('templates/BidAward.html')
        context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url}

        self.response.write(template.render(context))





class ContactHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/contact.html')
        context = {}
        self.response.write(template.render(context))

class FeedbackHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        Guser = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            tFirstname = self.request.get('vFirstnamer')
            tEmail = self.request.get('vEmailr')
            tSubject = self.request.get('vSubjectr')
            tBody = self.request.get('vBodyr')

            Uref = User.GetReferenceByRefNum(reference)
            tFeedback = Feedback()
            if mail.is_email_valid(tEmail):
                result = tFeedback.createFeedback(inFirstname=tFirstname, inEmail=tEmail, inSubject=tSubject, inBody=tBody)
            else:
                result = self.undefined

            if not(result == self.undefined) and not(result == self._generalError):
                FeedbackMessage = self._FeedbackCreatedSuccesfully
            else:
                FeedbackMessage = self._FeedbackNotCreatedSuccesfully


            template = template_env.get_template('templates/contact.html')

            if not(User._pkeyvalue == self.undefined):
                context = {'vUsername': Uref.readUsername(), 'Logout': logout_url, 'Login': login_url, 'FeedbackMessage': FeedbackMessage}
            else:
                Tusername = Guser.nickname()
                context = {'vUsername':Tusername, 'Logout': logout_url, 'Login': login_url, 'FeedbackMessage': FeedbackMessage}

            self.response.write(template.render(context))
        else: # User not logged in
            tFirstname = self.request.get('vFirstnamer')
            tEmail = self.request.get('vEmailr')
            tSubject = self.request.get('vSubjectr')
            tBody = self.request.get('vBodyr')

            tFeedback = Feedback()
            result = tFeedback.createFeedback(inFirstname=tFirstname, inEmail=tEmail, inSubject=tSubject, inBody=tBody)
            if not(result == self.undefined) and not(result == self._generalError):
                FeedbackMessage = self._FeedbackCreatedSuccesfully
            else:
                FeedbackMessage = self._FeedbackNotCreatedSuccesfully


            template = template_env.get_template('templates/contact.html')

            context = {'Logout': logout_url, 'Login': login_url, 'FeedbackMessage': FeedbackMessage}

            self.response.write(template.render(context))




class FeedbackResponseHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        Guser = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        if Guser:
            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

        tFirstname = self.request.get('vFirstnamer')
        tEmail = self.request.get('vEmailr')
        tSubject = self.request.get('vSubjectr')
        tBody = self.request.get('vBodyr')
        tResponse = self.request.get('vResponser')

        Uref = User.GetReferenceByRefNum(reference)

        findrequest = db.Query(Feedback).filter('Email =', tEmail).filter('CustomerSatisfied =', False)
        results = findrequest.fetch(limit=self._maxQResults)
        if len(results) > 0:
            tFeedback = results[0]
            result = tFeedback.writeCustomerSatisfied(Binput=True)
            if not(result == self._generalError):
                #Send the response to receipient
                if mail.is_email_valid(tEmail):
                    message = mail.EmailMessage()
                    message.sender = self._AppEmail
                    message.to = tEmail
                    message.subject = tFirstname + ' ' + tSubject
                    message.body = '''Your Message:
                    ''' + tBody + '''
                    Freelancing Solutions Response
                    ''' + tResponse
                    message.send()
                    tFeedback.put()
                    template = template_env.get_template('templates/admin.html')
                    findrequest = db.Query(Feedback).filter('CustomerSatisfied =', False)
                    results = findrequest.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        FeedbackList = results
                        context = {'vUsername': Uref.readUsername(), 'Logout': logout_url, 'Login': login_url, 'FeedbackList': FeedbackList }
                        self.response.write(template.render(context))

                else:
                    pass
                    # Do nothing



#######################################################################################################################
#######################################################################################################################
##APPLICATION STARTS HERE
#######################################################################################################################
#######################################################################################################################

#CRON JOBS

class PurgeFeedbackHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        findrequest = db.Query(Feedback).filter('CustomerSatisfied =', True)
        results = findrequest.fetch(limit=self._maxGoogleResults)
        if len(results) > 0:
            tFeedbackList = results
        else:
            tFeedbackList = []


        if len(tFeedbackList) > 0:
            i = 0
            while i < len(tFeedbackList):
                tFeedback = tFeedbackList[i]
                db.delete(tFeedback.key())
                i = i + 1


class SendNewsLettersHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        findrequest = db.Query(Newsletter).filter('NewsletterSent =', False)
        results = findrequest.fetch(limit=self._maxGoogleResults)
        if len(results) > 0:
            NewsletterList = results

            i = 0
            while i < len(NewsletterList):
                tNewsletter = NewsletterList[i]
                result = tNewsletter.sendNewsLetter()
                if (result == True) and tNewsletter.SetNewsletterSent():
                    tNewsletter.put()
                    i = i + 1
                else:
                    i = i + 1
        else:
            taskqueue.add(queue_name='NewsLettersQueue')
            # Quee a task to change all NewsletterSent to False


class NewsLettersQueueHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        findrequest = db.Query(Newsletter).filter('NewsletterSent =', True)
        results = findrequest.fetch(limit=self._maxGoogleResults)
        if len(results) > 0:
            NewsletterList = results

            i = 0
            while i < len(NewsletterList):
                tNewsletter = NewsletterList[i]
                if tNewsletter.ResetNewsletterSent():
                    tNewsletter.put()
                i = i + 1

class SendFreelanceJobsSummary(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        findrequest = db.Query(Job).filter('strJobType =', 'freelance jobs').order('+DateTimeSubmitted')
        results = findrequest.fetch(limit=self._maxQResults)

        if len(results) > 0:
            FreelanceJobsList = results
        else:
            FreelanceJobsList = []

        findrequest = db.Query(Newsletter)
        results = findrequest.fetch(limit=self._maxGoogleResults)

        if len(results) > 0:
            NewsLetterList = results
        else:
            NewsLetterList = []

        i = 0
        while i < len(NewsLetterList):
            tNewsletter = NewsLetterList[i]
            # Create a Queue for sending freelance jobs to this email Pass the value for the newsletter and the value for freelancejobslist
            i = i + 1
            key = self._FreelanceJobsListMemCacheKey
            success = memcache.set(key, FreelanceJobsList)
            if success == True:
                taskqueue.add(queue_name='SendFreelanceJobsQueue', params={'News_LetterKey': str(tNewsletter.key()),
                'FreelanceJobsList': key}) #learn how to pass variables to the queue

class SendFreelanceJobsQueueHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        NewsLetterKey = self.request.get('News_LetterKey')
        FJobsKey = self.request.get('FreelanceJobsList')
        tNewsletter = Newsletter.get(NewsLetterKey)
        FreelanceJobsList = memcache.get(FJobsKey)

        MessageBody = """
        Freelancing Solutions Freelance Jobs
        """
        for FreelanceJob in FreelanceJobsList:
            pass





        # Run a while loop that will construct a table for each freelance job

# Purpose to update the friendsList for every User in our system
# This Event will occur every saturday midnight so that on sunday morning all the facebook friends list on our program will be up to date
class UpdateFaceBookFriendsList(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        pass
    #The Best thing to do here will be to spawn tasks for each user to actually do the updating of friendlists by searching facebook


# Go Over every Reference Class load the ones that are not verified and send a verification email with the code and a link to the verification
# Page.
class SendVerEmailHandlerCron(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        findrequest = db.Query(Reference).filter('IsUserverified =', False)
        URefUnverified = findrequest.fetch(limit=self._maxGoogleResults)
        if len(URefUnverified) > 0:
            i = 0
            message = mail.EmailMessage()
            message.sender = self._AppEmail
            while i < len(URefUnverified):
                URef = URefUnverified[i]
                URef.CreateEmailVerCode()
                tVerCode = URef.readEmailVerCode()
                MessageSubject = 'Please: ' + URef.readUsername() +  ' Activate your Account in Freelancing Solutions'
                MessageBody = """
                Freelancing Solutions Account Verification
                Please Use the verification code supplied below to activate your account in freelancing solutions
                Verification Code:""" + tVerCode + """
                In order to verify your account please visit go to:
                <a href="http://jobcloud.freelancing-seo.com/membersVerifications">http://jobcloud.freelancing-seo.com/membersVerifications</a>
                and press Verify Email and enter the Verification Code Above.

                Thank you.
                Freelancing Solutions Team"""

                message.to = URef.readVerEmail()
                message.subject = MessageSubject
                message.body = MessageBody
                message.send()
                i = i + 1



class UpdateBiAwardResponses(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        Guser = users.get_current_user()
        if isGoogleServer:
            reference = Guser.user_id()
        else:
            reference = self._tempCode

        logging.info('BID AWARD RESPONSES IS BEING CALLED NICELY')
        MemStoreKey = reference + self._AwardedComMessages
        logging.info('MEMSTORE KEY :' + MemStoreKey)
        tBidReference = memcache.get(MemStoreKey)
        logging.info('MEM CACHE BID REFERECE: ' + tBidReference)
        tBidMessages = BidMessages()
        tBidMessagesList = tBidMessages.getBidMessages(strinput=tBidReference)
        template = template_env.get_template('templates/bidAwardResponses.html')
        context = {'tBidMessagesList': tBidMessagesList}
        self.response.write(template.render(context))

    def post(self):
        try:
            Guser = users.get_current_user()
            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode
            logging.info('YOUR REFERENCE IN BID AWARD RESPONSES :' + reference)
            Uref = User.GetReferenceByRefNum(reference)
            tBidReference = self.request.get('vBidReferencer')
            tMessage = self.request.get('vMessager')
            logging.info('MESSAGE :' + tMessage + 'BID REFERENCE :' + tBidReference)
            tBidMessages = BidMessages()
            tBidMessages.writeBidMessage(inBidRef=tBidReference,inMessage=tMessage,inMessageSender=Uref.readUsername())
            tBidMessagesList = tBidMessages.getBidMessages(strinput=tBidReference)
            template = template_env.get_template('templates/bidAwardResponses.html')
            context = {'tBidMessagesList': tBidMessagesList}
            self.response.write(template.render(context))
        except:
            logging.info('EXCEPTIONS THROWN ON BIDRESPONSE:...')

class UpdateScrapNotesHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        try:
            Guser = users.get_current_user()

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode
            template = template_env.get_template('templates/scrapnotes.html')
            findrequest = db.Query(ReviewBidsNotes).filter('fReference =', reference)
            findrequest = findrequest.order('-DateTimeCreated')
            results = findrequest.fetch(limit=self._maxQResults)

            if len(results) > 0:
                context = {'ScrapNotesList': results}
                self.response.write(template.render(context))
            else:
                context = {'UserMessages': 'There are Currently no Scrap Notes'}
                self.response.write(template.render(context))
        except:
            logging.info('EXCEPTIONS ARE THROWN READING SCRAP NOTES')

    def post(self):
        try:
            Guser = users.get_current_user()

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode
            tScrapNotes = ReviewBidsNotes()
            ScrapNote = self.request.get('vScrapNoter')
            ScrapNoteHeading = self.request.get('vScrapNoteHeadingr')
            tScrapNotes.createScrapNote(inScrapNote=ScrapNote,inReference=reference, inScrapNoteHeading=ScrapNoteHeading)
        except:
            logging.info('EXCEPTIONS THROWN WRITING SCRAP NOTES')



class ScrapNotesActionsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        try:
            ScrapKey = self.request.get('vScrapNoteReferencer')
            tAction = self.request.get('vActioner')
            logging.info('SCRAP KEY :' + ScrapKey)
            logging.info('ACTION :' + tAction)
            if tAction == 'edit':
                template = template_env.get_template('templates/ScrapNotesEditor.html')
                ScrapNote = ReviewBidsNotes.get(ScrapKey)
                context = {'ScrapNote': ScrapNote}
                self.response.write(template.render(context))
            elif tAction == 'delete':
                Result = db.delete(ScrapKey)
        except:
            logging.info('THROWING EXCEPTIONS ON SCRAP NOTES ACTIONS HANDLER:')


class NotFound(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        template = template_env.get_template('templates/sitemap.html')
        context = {}
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([('/login', loginHandler), ('/logout', logoutHandler),
                               ('/subscribe', SubscriptionsHandler),
                               ('/BrowsePortfolios', BrowsePortfolioHandler),
                               ('/about', AboutHandler),
                               ('/afreelancejobs', aFreelanceJobsHandler),
                               ('/amarketplace', aMarketPlaceHandler),
                               ('/ajobmarket', aJobMarketHandler),
                               ('/aaffiliates', aAffiliatesHandler),
                               ('/FreelancingJobs', FreelanceJobsHandler),
                               ('/FreelancingJobsPlaceBid', FreelancingJobsPlaceBidHandler),
                               ('/FreelancingJobsEmployersSubmit', FreelancingJobsEmployersSubmitHandler),
                               ('/FreelanceEmployersSubmissionResult', FreelanceEmployersSubmissionResultsHandler),
                               ('/MarketPlace', MarketPlaceHandler),
                               ('/Affiliates', AffiliatesHandler),
                               ('/JobMarket', JobmarketHandler),
                               ('/freelanceJobsSubscriptions', FreelanceJobsSubscriptionsHandler),
                               ('/FreelancingJobsEmployersReview', FreelancingJobsEmployersReviewHandler),
                               ('/fjobslist', fjobslisthandler),
                               ('/femployerJobList', femployerJobListHandler),
                               ('/activebids', activebidshandler),
                               ('/BidsProcess', BidsProcessHandler),
                               ('/FreelancingJobsEmployersAwarded', FreelancingJobsEmployersAwarded),
                               ('/contact', ContactHandler),
                               ('/feedback', FeedbackHandler),
                               ('/FeedbackResponse', FeedbackResponseHandler),
                               ('/cron/purgefeedback', PurgeFeedbackHandler),
                               ('/cron/SendNewsLetter', SendNewsLettersHandler),
                               ('/cron/SendFreelanceJobsSummary', SendFreelanceJobsSummary),
                               ('/cron/UpdateFaceBookFriends', UpdateFaceBookFriendsList),
                               ('/cron/SendVerificationEmail', SendVerEmailHandlerCron),
                               ('/_ah/queue/NewsLettersQueue', NewsLettersQueueHandler),
                               ('/_ah/queue/SendFreelanceJobsQueue',  SendFreelanceJobsQueueHandler),
                               ('/BidAwardResponses', UpdateBiAwardResponses),
                               ('/ScrapNotes', UpdateScrapNotesHandler),
                               ('/ScrapNotesActions', ScrapNotesActionsHandler),
                               ('/index.html', MainPage),
                               ('/', MainPage),
                               ('/.*', NotFound)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
