#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'


# Copyright 2014 Freelancing Solutions.
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

#######################################################################################################################
############################### FREELANCE PROFILE #####################################################################
#######################################################################################################################
############ The profile must also included banking details and internal account balances. ############################
# a way to intergrated PayPal, BitCoin and credit card payments must eb included. #####################################
#######################################################################################################################
import os
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
from edu import EducationalQualifications
from accounts import Wallet
from datatypes import Reference, Person
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from skills import Skills
from testcentre import TestResults
from profilemessages import ProfileMessages
from ProfileReviews import ProfileReviews
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import logging

User = Person()
# Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

class Profiles (db.Expando, MyConstants, ErrorCodes):
    ProfileReference = db.StringProperty()  # The Index Key for this profile will be stored Here

    ProfileName = db.StringProperty(indexed=True) #  This is the last portion of the profile URL
    indexReference = db.ReferenceProperty(Reference, collection_name='user_profiles')
    UReferenceNum = db.StringProperty() # The Reference Number of the user who owns the profile

    ProfileSEOTitle = db.StringProperty() # The Title of the Profile not to exceed 69 Characters
    ProfileTags = db.ListProperty(item_type=str)  # A List of Keywords or Tags for the profile
    ProfileSEODefinition = db.StringProperty(multiline=True)  # The SEO Definition of the USer Profile...
    Heading = db.StringProperty()  # The Heading of the Profile...
    Introduction = db.StringProperty(multiline=True) # The Page Introduction of the overall Profile...
    Body = db.TextProperty()  #  The Body Property of the overall Profile...

    #Freelancer Details
    FreelancerHireURL = db.StringProperty()
    ProfileReviewURL = db.StringProperty()
    ProfileProposalURL = db.StringProperty()
    PortfolioURL = db.StringProperty()
    ProfileSendMessageURL = db.StringProperty()
    ProfileSocialURL = db.StringProperty()

    #User Sub Profiles
    FreelanceJobsProfileURL = db.StringProperty()
    MarketPlaceProfileURL = db.StringProperty()
    AffiliatesProfileURL = db.StringProperty()
    JobMarketProfileURL =db.StringProperty()

    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)
    ProfileNumber = db.IntegerProperty()

    def findMyProfile(self, myReference):
        try:

            Uref = Reference.get(myReference)
            User._pkeyvalue = Uref.key()

            if not(User._pkeyvalue == self.undefined):
                findquery = db.Query(Profiles).filter('indexReference =', User._pkeyvalue)
                results = findquery.fetch(limit=1)
                if len(results) > 0:
                    tProfile = results[0]
                    return tProfile
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError


    def readProfileSocialURL(self):
        try:
            temp = str(self.ProfileSocialURL)
            if (len(temp) > 0) and not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readFreelanceJobsProfileURL(self):
        try:
            temp = str(self.FreelanceJobsProfileURL)
            if (len(temp) > 0) and not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readMarketPlaceProfileURL(self):
        try:
            temp = str(self.MarketPlaceProfileURL)
            if (len(temp) > 0) and not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readAffiliatesProfileURL(self):
        try:
            temp = str(self.AffiliatesProfileURL)
            if (len(temp) > 0) and not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def readJobMarketProfileURL(self):
        try:
            temp = str(self.JobMarketProfileURL)
            if (len(temp) > 0) and not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError



    def createProfileSocialURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/social'
            self.ProfileSocialURL = temp
            return temp
        except:
            return self._generalError

    def createFreelanceJobsProfileURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/freelance'
            self.FreelanceJobsProfileURL = temp
            return temp
        except:
            return self._generalError

    def createMarketPlaceProfileURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/marketplace'
            self.MarketPlaceProfileURL = temp
            return temp
        except:
            return self._generalError

    def createAffiliatesProfileURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/affiliates'
            self.AffiliatesProfileURL = temp
            return temp
        except:
            return self._generalError

    def createJobMarketProfileURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/jobmarket'
            self.JobMarketProfileURL = temp
            return temp
        except:
            return self._generalError

    def createFreelancerHireURL(self, Profilename):
        try:
            temp = '/profiles/'+  Profilename + '/freelanceHire'
            self.FreelancerHireURL = temp
            return temp
        except:
            return self._generalError

    def createProfileReviewURL(self, Profilename):
        try:
            temp = '/profiles/'+ Profilename + '/reviews'
            self.ProfileReviewURL = temp
            return temp
        except:
            return self._generalError

    def createProfileProposalURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/proposals'
            self.ProfileProposalURL = temp
            return temp
        except:
            return self._generalError

    def createFreelancePortfolioURL(self, Profilename):
        try:
            temp = '/FPortfolios/'+ Profilename
            self.PortfolioURL = temp
            return temp
        except:
            return self._generalError

    def createProfileSendMessageURL(self, Profilename):
        try:
            temp = '/profiles/' + Profilename + '/SendMessage'
            self.ProfileSendMessageURL = temp
            return temp
        except:
            return self._generalError

#     FreelanceJobsProfileURL = db.StringProperty()
#    MarketPlaceProfileURL = db.StringProperty()
#   AffiliatesProfileURL = db.StringProperty()
#    JobMarketProfileURL =db.StringProperty()
    #@db.transactional(retries=10)
    def createHomeProfile(self,inIndex, inUReference, inProfileName, inProfileSEOTitle, inProfileSEODef, inProfileHeading, inProfileIntroduction, inProfileBody):
        try:
            logging.info('SUCCESFULLY ENTERED THE CREATE HOME PROFILE')
            findrequest = db.Query(Profiles).filter('indexReference =', inIndex)
            results = findrequest.fetch(limit=1)
            if len(results) > 0:
                tProfile = results[0]
                if tProfile.writeProfileName(strinput=inProfileName) and tProfile.writeProfileSEOTitle(strinput=inProfileSEOTitle) \
                and tProfile.writeProfileSEODefinition(strinput=inProfileSEODef) and tProfile.writeHeading(strinput=inProfileHeading) \
                and tProfile.writeIntroduction(strinput=inProfileIntroduction) and tProfile.writeBody(strinput=inProfileBody) and tProfile.writeUReferenceNum(inUReference):

                    tProfile.createFreelancerHireURL(inProfileName)
                    tProfile.createProfileReviewURL(inProfileName)
                    tProfile.createProfileProposalURL(inProfileName)
                    tProfile.createFreelancePortfolioURL(inProfileName)
                    tProfile.createProfileSendMessageURL(inProfileName)
                    tProfile.createFreelanceJobsProfileURL(inProfileName)
                    tProfile.createMarketPlaceProfileURL(inProfileName)
                    tProfile.createAffiliatesProfileURL(inProfileName)
                    tProfile.createJobMarketProfileURL(inProfileName)
                    tProfile.createProfileSocialURL(inProfileName)
                    tProfile.indexReference = inIndex
                    tProfile.ProfileReference = str(tProfile.put())
                    if tProfile.writeProfileNumber(inNum=1) == True:
                        logging.info('HOME PROFILE SUCCESFULLY WRITEN WITH PROFILE NUMBER: ' + tProfile.readProfileNumber())
                    tProfile.put()

                    return True


            else:
                if self.writeProfileName(strinput=inProfileName) and self.writeProfileSEOTitle(strinput=inProfileSEOTitle) \
                and self.writeProfileSEODefinition(strinput=inProfileSEODef) and self.writeHeading(strinput=inProfileHeading) \
                and self.writeIntroduction(strinput=inProfileIntroduction) and self.writeBody(strinput=inProfileBody) and self.writeUReferenceNum(strinput=inUReference):

                    self.createFreelancerHireURL(inProfileName)
                    self.createProfileReviewURL(inProfileName)
                    self.createProfileProposalURL(inProfileName)
                    self.createFreelancePortfolioURL(inProfileName)
                    self.createProfileSendMessageURL(inProfileName)
                    self.createFreelanceJobsProfileURL(inProfileName)
                    self.createMarketPlaceProfileURL(inProfileName)
                    self.createAffiliatesProfileURL(inProfileName)
                    self.createJobMarketProfileURL(inProfileName)
                    self.createProfileSocialURL(inProfileName)
                    self.indexReference = inIndex
                    # Atomic Starts Here
                    #Find the Latest Profile Number advance it and write a new one.
                    findrequest = db.Query(Profiles).order('-ProfileNumber')
                    lastProfile = findrequest.fetch(limit=1)
                    if len(lastProfile) > 0:
                        tLastProfile = lastProfile[0]
                        tProfileNumber = tLastProfile.readProfileNumber()
                        tProfileNumber = int(tProfileNumber)
                        tProfileNumber = tProfileNumber + 1
                    else:
                        tProfileNumber = 1
                    self.writeProfileNumber(inNum=tProfileNumber)
                    self.ProfileReference = str(self.put())
                    self.put()
                    # Atomic ends here
                    return True
                else:
                    return False
        except:
            return self._generalError
    # UReferenceNum
    def readUReferenceNum(self):
        try:
            temp = str(self.UReferenceNum)
            if len(temp)> 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeUReferenceNum(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.UReferenceNum = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def writeProfileNumber(self, inNum):
        try:
            inNum = str(inNum)
            inNum = inNum.strip()
            if inNum.isdigit():
                logging.info('PROFILE NUMBER IS TRULLY DIGIT')
                self.ProfileNumber = int(inNum)
                return True
            else:
                logging.info('PROFILE NUMBER IS NOT A DIGIT')
                return False
        except:
            logging.info('RAISING EXCEPTIONS')
            return self._generalError

    def readProfileNumber(self):
        try:
            temp = str(self.ProfileNumber)
            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def readProfileSendMessageURL(self):
        try:
            temp = str(self.ProfileSendMessageURL)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileSendMessageURL(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.ProfileSendMessageURL = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    def readPortfolioURL(self):
        try:
            temp = str(self.PortfolioURL)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writePortfolioURL(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.PortfolioURL = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readFreelancerHireURL(self):
        try:
            temp = str(self.FreelancerHireURL)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeFreelancerHireURL(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.FreelancerHireURL = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readProfileReviewURL(self):
        try:
            temp = str(self.ProfileReviewURL)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileReviewURL(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.ProfileReviewURL = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readProfileProposalURL(self):
        try:
            temp = str(self.ProfileProposalURL)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileProposalURL(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.ProfileProposalURL = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readindexReferencer(self):
        try:
            temp = str(self.indexReference)
            if len(temp) > 0:
                return self.indexReference
            else:
                return self.undefined
        except:
            return self._generalError

    def writeindexReference(self, strinput):
        try:
            if len(strinput) > 0:
                self.indexReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readProfileName(self):
        try:
            temp = str(self.ProfileName)
            temp = temp.strip()
            temp = temp.lower()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if len(strinput) > 0:
                self.ProfileName = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readProfileSEOTitle(self):
        try:
            temp = str(self.ProfileSEOTitle)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileSEOTitle(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.ProfileSEOTitle = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readProfileTags(self):
        try:
            temp = str(self.ProfileTags)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfileTags(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.ProfileTags = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readProfileSEODefinition(self):
        try:
            temp = str(self.ProfileSEODefinition)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeProfileSEODefinition(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.ProfileSEODefinition = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readHeading(self):
        try:
            temp = str(self.Heading)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeHeading(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.Heading = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readIntroduction(self):
        try:
            temp = str(self.Introduction)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeIntroduction(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.Introduction = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBody(self):
        try:
            temp = self.Body

            if temp == self._generalError or temp == self.undefined:
                return self.undefined
            else:
                return temp
        except:
            return self._generalError

    def writeBody(self, strinput):
        try:
            if len(strinput) > 0:
                self.Body = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    #note that a class to browse profiles must be created.

#todo-VERY IMPROTANT INCLUDE THE AFFILIATE CLASS WHICH WILL WORK WITH THE WHOLE PROGRAM
# its features can be as follows the ability to communicate through Facebook, Twitter, Google+ and Linkedin
# The ability to communicate through this application.
# it must have a control panel where products and services can be added by affiliate partners
# Read more about this on the AffiliateNotes File on this project.

################################################################################################
##################PROFILES HANDLER##############################################################
################################################################################################

# Load The Public profile as requested by the URL. for example if the request url is
# /profiles/john then load johns profile and if the requested profile is /profiles/
# then load featured profiles.

# The Handler can simply request data from the database using the profile name supplied.
# Meaning The Profile Class must have a place for profile names...
# And also A Place for Profile Information about the user or company...
# Profile Names must always be unique...

class FavouriteProfiles(db.Expando, MyConstants, ErrorCodes):
    indexReference = db.ReferenceProperty(Reference, collection_name='favourite_profiles')
    FavouriteReference = db.StringProperty() # The Reference Index of the profile favoured
    FavouriteProfileName = db.StringProperty()
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)

    # Given the indexReference Key this function will return a list of all favourite profiles
    def returnMyFavouriteProfiles(self, myIndex):
        try:
            temp = str(myIndex)
            if len(temp) > 0:
                findrequest = db.Query(FavouriteProfiles).filter('indexReference =', myIndex)
                results = findrequest.fetch(limit=self._maxHomeProfileList)
                if len(results) > 0:
                    NProfileList = []
                    i = 0
                    while i < len(results):
                        tFav = results[i]
                        tNProfile = Profiles.get(tFav.readFavouriteReference())
                        NProfileList.append(tNProfile)
                        i = i + 1

                    return NProfileList
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    def addToMyFavouriteList(self, inFavouriteReference):
        try:
            Guser = users.get_current_user()
            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                Uref = User.GetReferenceByRefNum(reference)
                if not(User._pkeyvalue == self.undefined):


                    findrequest = db.Query(FavouriteProfiles).filter('FavouriteReference =', inFavouriteReference)
                    results = findrequest.fetch(limit=1)
                    if len(results) > 0:
                        return False
                    else:
                        tProfile = Profiles()
                        logging.info('THE CURRENT PKEY VALUE : ' + str(User._pkeyvalue))
                        tProfile = tProfile.findMyProfile(User._pkeyvalue)
                        if not(tProfile == self.undefined) and not(tProfile == self._generalError):
                            if self.writeindexReference(strinput=User._pkeyvalue) and self.writeFavouriteReference(strinput=inFavouriteReference) and \
                                    self.writeFavouriteProfileName(strinput=tProfile.readProfileName()):
                                logging.info('THE FAVOURITE CLASS WAS WRITTEN WITH EVERYTHING INTACT')
                                self.put()
                                logging.info('WE HAVE SUCCESFULLY WRITTEN THE FAVOURITE PROFILE')
                                return True
                            else:
                                return False
                        else:
                            return False
                else:
                    return False
            else:
                return False
        except:
            return self._generalError




    def readindexReference(self):
        try:
            if not(self.indexReference == self.undefined):
                return self.indexReference
            else:
                return self.undefined
        except:
            return self._generalError

    def writeindexReference(self, strinput):
        try:
            temp = str(strinput)
            if len(temp) > 0:
                self.indexReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readFavouriteReference(self):
        try:
            temp =self.FavouriteReference
            temp2 = str(temp)

            if len(temp2) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeFavouriteReference(self, strinput):
        try:
            tkey = strinput
            strinput = str(strinput)
            if len(strinput) > 0:
                self.FavouriteReference = tkey
                return True
            else:
                return False
        except:
            return self._generalError

    def readFavouriteProfileName(self):
        try:
            temp = str(self.FavouriteProfileName)
            temp = temp.lower()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeFavouriteProfileName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.lower()
            if len(strinput) > 0:
                self.FavouriteProfileName = strinput
                return True
            else:
                return False
        except:
            return self._generalError





class ProfilesHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    #Show the Profiles Home Page Allowing the Creation of Profiles, Browsing of Profiles Searching Profiles and other management tasks
    def get(self):
        template = template_env.get_template('templates/profile.html')
        context = {}
        self.response.write(template.render(context))




app = webapp2.WSGIApplication([('/profile', ProfilesHandler)], debug=True)


