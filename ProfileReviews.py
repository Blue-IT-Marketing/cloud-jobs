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
from datatypes import Reference
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
import logging


class ProfileReviews(db.Expando, MyConstants, ErrorCodes):
    PReviewRef = db.StringProperty()
    indexReference = db.ReferenceProperty(reference_class=Reference,collection_name='profile_reviews') # to the owner of the Profile
    UReferenceNum = db.StringProperty() # A Reference Number from the Profile Owner Reference Class
    # A Reference Number to the user who placed the Review
    RReferenceNum = db.StringProperty()
    Firstname = db.StringProperty()
    Email = db.EmailProperty()
    Subject = db.StringProperty()
    Rating = db.StringProperty()
    Review = db.StringProperty()
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def createProfileReview(self, inIndex, inUReference, inRReference,inFirstname,inEmail,inSubject,inRating,inReview):
        try:

            if self.writeIndexReference(strinput=inIndex) and self.writeUReferenceNum(strinput=inUReference) \
                and self.writeFirstname(strinput=inFirstname) and self.writeEmail(strinput=inEmail) and \
                self.writeSubject(strinput=inSubject) and self.writeRating(strinput=inRating) and \
                self.writeReview(strinput=inReview) and self.writeRReferenceNum(strinput=inRReference):
                logging.info('PROFILE REVIEW INITIAL PASSED')
                self.PReviewRef = str(self.put())
                self.put()
                return True
            else:
                logging.info('SIMPLE FAILURE IN CREATING PROFILE REVIEWS')
                return False
        except:
            logging.info('SERIOUS FAILURE IN CREATING PROFILE REVIEWS')
            return self._generalError

    def readRReferenceNum(self):
        try:
            temp = str(self.RReferenceNum)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeRReferenceNum(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.RReferenceNum = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readIndexReference(self):
        try:
            temp = self.indexReference
            if not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeIndexReference(self, strinput):
        try:
            temp = str(strinput)
            if len(temp) > 0:
                self.indexReference = strinput
                logging.info('WRITE INDEX FOR PROFILE REVIEW PASSED')
                return True
            else:
                return False
        except:
            return self._generalError

    def readUReferenceNum(self):
        try:
            temp = str(self.UReferenceNum)

            if len(temp) > 0:
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
                logging.info('WRITE UREFERENCE PASSED ON PROFILE REVIEWS')
                return True
            else:
                return False
        except:
            return self._generalError


    def readFirstname(self):
        try:
            temp = str(self.Firstname)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeFirstname(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.Firstname = strinput
                logging.info('WRITE FIRST NAME PASSED ON PROFILE REVIEWS')
                return True
            else:
                return False
        except:
            return self._generalError

    def readEmail(self):
        try:
            temp = str(self.Email)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeEmail(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.Email = strinput
                logging.info('WRITE EMAIL PASSED ON PROFILE REVIEWS')
                return True
            else:
                return False
        except:
            return self._generalError

    def readSubject(self):
        try:
            temp = str(self.Subject)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSubject(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.Subject = strinput
                logging.info('WRITE SUBJECT PASSED ON PROFILE REVIEWS')
                return True
            else:
                return False
        except:
            return self._generalError

    def readRating(self):
        try:
            temp = int(self.Rating)
            if (temp > 0) and (temp < 11):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeRating(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if strinput.isdigit():
                tRating = int(strinput)
            else:
                tRating = 0

            if (tRating > 0) and (tRating < 11):
                self.Rating = str(tRating)
                logging.info('WRITE RATING PASSED ON PROFILE REVIEWS')
                return True
            else:
                return False
        except:
            return self._generalError


    def readReview(self):
        try:
            temp = str(self.Review)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeReview(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.Review = strinput
                return True
            else:
                return False
        except:
            return self._generalError
