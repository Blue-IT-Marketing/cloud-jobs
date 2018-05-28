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



from datatypes import Reference
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import logging



DefNameofQualifications = ['website development', 'article writing', 'seo specialist', 'human resource']
DefTypeOfQualifications = ['engineer', 'artisan', 'diploma', 'other', 'batchelor', 'masters', 'doctorate']

class Qualifications (db.Expando, MyConstants, ErrorCodes):

    #constants
    minNameofQualificationsLen = 2
    maxNameOfQualificationsLen = 256

    minTypeOfQualificationsLen = 2
    maxTypeOfQualificationsLen = 256



    strNameOFQualifications = db.StringProperty() #Consider loading name of Qualifications from their own class
    strTypeOfQualifications = db.StringProperty() #consider loading type of qualifications from their own class
    isValid = db.BooleanProperty(default=False)



    #TODO- Finish up the Qualifications class and then finish up everything up until the Job Class
    def readIsValid(self):
        pass

    def readstrNameofQualification (self):

        try:

            temp = str(self.strNameOFQualifications)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self.maxNameOfQualificationsLen) and (len(temp) >= self.minNameofQualificationsLen)):
                self.strNameOFQualifications = temp
                return temp
            else:
                return self.undefined
        except:

            return self._generalError




    def writestrNameOfQualification (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) <= self.maxNameOfQualificationsLen) and (len(strinput) >= self.minNameofQualificationsLen)):
                self.strNameOFQualifications = strinput
                return True
            else:
                return self.undefined
        except:

            return self._generalError


    def readstrTypeOfQualification (self):

        try:

            temp = str(self.strTypeOfQualifications)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self.maxTypeOfQualificationsLen) and (len(temp) >= self.minTypeOfQualificationsLen)):
                self.strTypeOfQualifications = temp
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writestrTypeofQualification (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) <= self.maxTypeOfQualificationsLen) and (len(strinput) >= self.minTypeOfQualificationsLen)):
                self.strTypeOfQualifications = strinput
                return True
            else:
                return False
        except:
            return self._generalError



class RequiredEduQualifications (db.Expando, MyConstants, ErrorCodes):
    _qualifications = Qualifications()
    clsQualification = db.ReferenceProperty(Qualifications, collection_name='required_qualifications_collection')
    #one required Qualifications Record will link to many Qualifications
    isCompulsory = db.BooleanProperty(default=True) # True or false

    def readIsValid(self):
        pass
    # Read a specific educational qualifications record

    def readQualification(self):
        try:
            if not(self.clsQualification == self.undefined):
                return self.clsQualification
            else:
                return self.undefined
        except:
            return self._generalError

    def writeQualification(self, strinput):
        try:

            Guser = users.get_current_user()

            if Guser:
                strinput = str(strinput)
                strinput = strinput.strip()

                if strinput.isalnum():
                    self.clsQualification = strinput
                    return True
                else:
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def saveQualifications(self):
        try:

            Guser = users.get_current_user()

            if Guser:
                if self._qualifications.readIsValid():
                    if self.clsQualification == self.undefined:
                        self.clsQualification = self._qualifications.put()
                        return True
                    else:
                        # there's a pre existing Qualifications record
                        TQual = Qualifications.get(self.clsQualification)
                        if TQual.readIsValid():
                            TQual.writestrNameOfQualification(self._qualifications.readstrNameofQualification())
                            TQual.writestrTypeofQualification(self._qualifications.readstrTypeOfQualification())
                            self.clsQualification = TQual.put()
                            return True
                        else:
                            return self._QualificationsInvalid
                else:
                    return self._QualificationsInvalid
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def retrieveQualifications(self):
        try:
            if not(self.clsQualification == self.undefined):
                TQual = Qualifications.get(self.clsQualification)
                if TQual.readIsValid():
                    return TQual
                else:
                    return self._QualificationsInvalid
            else:
                return self._QualificationsDoNotExist
        except:
            return self._generalError


    def readisCompulsory (self):

        try:
            return self.isCompulsory
        except:
            return self._generalError



    def writeisCompulsory (self, bolinput):
        try:
            if bolinput:
                self.isCompulsory = True
                return True
            else:
                self.isCompulsory = False
                return True
        except:
            return self._generalError