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


#class created to provide functionality related to a freelancer.
#this class is the cousin of jobseeker in the jobmarket.
#The class can also be useful on the Job Market as it can create functionality for a freelancer there.
from google.appengine.ext import db
from ConstantsAndErrorCodes import MyConstants, ErrorCodes

class Feedback(db.Expando, MyConstants, ErrorCodes):
    Firstname = db.StringProperty()
    Email = db.EmailProperty()
    Subject = db.StringProperty()
    Body = db.StringProperty(multiline=True)
    Attended = db.BooleanProperty(default=False)
    CustomerSatisfied = db.BooleanProperty(default=False)

    def createFeedback(self, inFirstname, inEmail, inSubject, inBody):
        try:
            if self.writeFirstname(inFirstname) and self.writeEmail(inEmail) and self.writeSubject(inSubject) and self.writeBody(inBody):
                tempKey = self.put()
                return tempKey
            else:
                return self.undefined
        except:
            return self._generalError


    def writeCustomerSatisfied(self, Binput):
        try:
            self.CustomerSatisfied = Binput
            return True
        except:
            return self._generalError

    def readFirstname(self):
        try:
            temp = str(self.Firstname)
            temp = temp.strip()

            if temp.isalpha():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeFirstname(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalpha():
                self.Firstname = strinput
                return True
            else:
                return False
        except:
            return self._generalError




    def readEmail(self):
        try:
            temp = str(self.Email)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeEmail(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                findrequest = db.Query(Feedback).filter('Email =', strinput).filter('CustomerSatisfied =', False)
                results = findrequest.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return False
                else:
                    self.Email = strinput
                    return True
            else:
                return False
        except:
            return self._generalError



    def readSubject(self):
        try:
            temp = str(self.Subject)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeSubject(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.Subject = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    def readBody(self):
        try:
            temp = str(self.Body)


            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeBody(self, strinput):
        try:

            strinput = str(strinput)


            if len(strinput) > 0:
                self.Body = strinput
                return True
            else:
                return False
        except:
            return self._generalError

