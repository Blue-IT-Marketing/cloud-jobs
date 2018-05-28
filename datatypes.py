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
#names class takes care of the names of an individual

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer

#Make sure to encrypt everything on the datatype
from datetime import date
import logging
from utilities import Util
#Importing Custom Email and Website from Utilities
from utilities import CustomEmail
from utilities import Website
######################################################################################################################
#CONSTANTS
dateseparator = '/'
undefined = None #meaning no value and does not infer any type
LegalYearLimit = 120


class Reference (db.Expando, MyConstants,ErrorCodes):

    _maxReferenceLen = 256
    _maxIDNumberLen = 13
    _maxUserNameLen = 64
    _minUserNameLen = 8
    _maxPasswordLen = 64
    _minPasswordLen = 8
    _maxVerEmail = 256
    _minVerEmail = 8


    strReferenceNum = db.StringProperty() #Required Code Enforced It is also a Key this value is found on teh Google Account used
    #to login to the system
    strIDNum = db.StringProperty()
    isValid = False #Required Code Enforced
        #Added values for login in
    strUsername = db.StringProperty() #Required Code Enforced
    strPassword = db.StringProperty() #Required Code Enforced
    IsUserverified = db.BooleanProperty(default=False) #After registration users must verify their accounts.
    strVerificationEmail = db.EmailProperty() #Used to store the email used to send  verification details.
    DateTimeVerified = db.DateTimeProperty() #Date and time account was verified.
    DateTimeEdited = db.DateTimeProperty(auto_now=True)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)
    logoPhoto = db.BlobProperty()
    NewsletterSubscription = db.BooleanProperty(default=False)
    IsCellVerified = db.BooleanProperty(default=False)
    EmailVerCode = db.StringProperty()
    SMSVerCode = db.StringProperty()

    def readIsCellVerified(self):
        try:
            return self.IsCellVerified
        except:
            return self.undefined

    def CreateEmailVerCode(self):
        try:
            if isGoogleServer:
                tempverCode = self.strReferenceNum[10: 18]
                self.EmailVerCode = tempverCode
                return tempverCode
            else:
                tempverCode = self.strReferenceNum
                self.EmailVerCode = tempverCode
                return tempverCode
        except:
            return self.undefined

    def CreateSMSVerCode(self):
        try:
            if isGoogleServer:
                tempverCode = self.strReferenceNum[10: 18]
                self.SMSVerCode = tempverCode
                return tempverCode
            else:
                tempverCode = self.strReferenceNum
                self.SMSVerCode = tempverCode
                return tempverCode
        except:
            return self.undefined


    def readEmailVerCode(self):
        try:
            temp = str(self.EmailVerCode)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readSMSVerCode(self):
        try:
            temp = str(self.SMSVerCode)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readLogoPhoto(self):
        try:
            return self.logoPhoto
        except:
            return self._generalError

    def writeLogoPhoto(self, byteLogoPhoto):
        try:
            self.logoPhoto = byteLogoPhoto
            return True
        except:
            return self._generalError

    def readDatetimeVerified(self):
        try:
            temp = self.DateTimeVerified
            return temp
        except:
            return self._generalError

    def writeDateTimeVerified(self, strDateTime):
        pass

    def readDateTimeEdited(self):
        try:
            temp = self.DateTimeEdited
            return temp
        except:
            return self._generalError

    def readDateTimeCreated(self):

        try:
            temp = self.DateTimeCreated
            return temp
        except:
            return self._generalError

    def readIsUserVerified(self):
        try:

            return self.IsUserverified
        except:
            return self._generalError

    #Note IsUserVerified will be written by the verification function. by calling this function
    #If set the function will return true and if failed it will return false
    def writeIsUserVerified(self, verified):
        try:
            if verified == True:
                self.IsUserverified = True
                return True
            else:
                self.IsUserverified = False
                return True
        except:
            return self._generalError


    def readVerEmail(self):
        try:
            temp = str(self.strVerificationEmail)
            # Decrypt Temp
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self._maxVerEmail) and (len(temp) >= self._minVerEmail)):
                # Encrypt Temp
                self.strVerificationEmail = temp
                # Decrypt Temp

                return temp
            else:
                self.strVerificationEmail = self.undefined
                return self.undefined
        except:
            return self._generalError


    #note that the verification email must be verified by the User class

    def writeVerEmail(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if ((len(strinput) <= self._maxVerEmail) and (len(strinput) >= self._minVerEmail)):
                # Encrypt strinput
                self.strVerificationEmail = strinput
                return True
            else:
                self.strVerificationEmail = self.undefined
                return False
        except:
            return self._generalError

    def readUsername(self):
        try:
            temp = str(self.strUsername)
            temp = temp.strip()
            if ((len(temp) <= self._maxUserNameLen) and (len(temp) >= self._minUserNameLen)):
                self.strUsername = temp
                return temp
            else:
                self.strUsername = self.undefined
                return self.undefined
        except:
            return self._generalError

    def writeUsername(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if ((len(strinput) <= self._maxUserNameLen) and (len(strinput) >= self._minUserNameLen)):
                self.strUsername = strinput
                logging.info('Username  Ok')
                return True
            else:
                self.strUsername = self.undefined
                logging.info('Username Failure')
                return False
        except:
            return self._generalError

    def readPassword(self):
        try:
            temp = str(self.strPassword)
            temp = temp.strip()
            if ((len(temp) <= self._maxPasswordLen) and (len(temp) >= self._minPasswordLen)):
                logging.info('READ PASSWORD SUCCESS')
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePassword(self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((len(strinput) <= self._maxPasswordLen) and (len(strinput) >= self._minPasswordLen)):
                self.strPassword = strinput
                logging.info('Password OK')
                return True
            else:
                logging.info('Password Failure')
                return False
        except:
            logging.error('Catastrophic Failure')
            return self._generalError


    def readReference(self):

        try:
            temp = str(self.strReferenceNum)
            temp = temp.strip()
            temp = temp.lower()
            if ((temp.isalnum() or temp.isalpha() or temp.isdigit()) and (len(temp) <= self._maxReferenceLen)):
                self.strReferenceNum = temp
                logging.info('READ REFERENCE SUCCESS')
                return temp
            else:
                self.strReferenceNum = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeReference(self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if ((strinput.isalnum() or strinput.isalpha() or strinput.isdigit()) and (len(strinput) <= self._maxReferenceLen)):
                self.strReferenceNum = strinput
                logging.info('Reference OK')
                return True
            else:
                logging.info('Reference Failure')
                self.strReferenceNum = self.undefined
                return False
        except:
            logging.error('Catastrophic Failure on write reference')
            self.strReferenceNum = undefined
            return self._generalError

    def readIDNumber (self):

        try:

            temp = str(self.strIDNum)
            temp = temp.strip()


            if ((temp.isdigit()) and (len(temp) == self._maxIDNumberLen)):
                self.strIDNum = temp
                logging.info('READ ID NUMBER SUCCESSS')
                return temp
            else:
                self.strIDNum = self.undefined
                return self.undefined
        except:

            return self._generalError

    def writeIDNumber (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()


            if ((strinput.isdigit()) and (len(strinput) == self._maxIDNumberLen)):
                self.strIDNum = strinput
                logging.info('WRITE ID NUMBER SUCCESS')
                return True
            else:
                self.strIDNum = self.undefined
                return False
        except:
            return self._generalError

    def readIsValid (self):
        try:
            self.setIsValid()
            return True
        except:
            return self._generalError

    def setIsValid (self):
        try:

            if not(self.readReference() == self.undefined):
                if not(self.readUsername() == self.undefined):
                    if not(self.readPassword() == self.undefined):
                        self.isValid = True
                    else:
                        self.isValid = False
                else:
                    self.isValid = False
            else:
                self.isValid = False
        except:
            self.isValid = False





########################################################################################################################
########################################################################################################################
########################################################################################################################
####################### NAMES CLASS BEGIN------------------------------------------------------------------------------
########################################################################################################################




class Names(db.Expando, MyConstants, ErrorCodes):

    _minNamesLen = 1
    _maxNamesLen = 256
    _minInitialsLen = 1
    _maxInitialsLen = 4
    _utilities = Util()

    indexReference = db.ReferenceProperty(Reference, collection_name='names_and_titles') #This create a link to the reference class
    strInitials = db.StringProperty()
    strTitle = db.StringProperty() #Required Code Enforced
    strFirstname = db.StringProperty() #Required Code Enforced
    strSecondname = db.StringProperty()
    strSurname = db.StringProperty() #Required Code Enforced
    isValid = False
    DateTimeEdited = db.DateTimeProperty(auto_now=True)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def readDateTimeEdited(self):
        try:
            temp = self.DateTimeEdited
            return temp
        except:
            return self._generalError

    def readDateTimeCreated(self):
        try:
            temp = self.DateTimeCreated
            return temp
        except:
            return self._generalError


    def readInitials(self):
        try:
            temp = str(self.strInitials)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.isalpha()) and (len(temp) <= self._minInitialsLen) and (len(temp) >= self._maxInitialsLen)):
                self.strInitials = temp
                logging.info('READ INITIALS SUCCESS')
                return temp
            else:
                self.strInitials = self.undefined
                return self.undefined
        except:
            return self._generalError

    def writeInitials(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.isalpha()) and (len(strinput) <= self._maxInitialsLen) and (len(strinput) >= self._minInitialsLen)):
                self.strInitials = strinput
                logging.info('WRITE INITIALS SUCCESS')
                return True
            else:
                self.strInitials = self.undefined
                return False
        except:
            return self._generalError


    def readTitle(self):

        try:
            if self._utilities.is_title(self.strTitle):
                logging.info('READ TITLE SUCCESS')
                return self.strTitle
            else:
                return self.undefined
        except:
            return self._generalError

    def writeTitle(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if self._utilities.is_title(strinput):
                logging.info('WRITE TITLE SUCESS')
                self.strTitle = strinput
                return True
            else:
                self.strTitle = self.undefined
                return False
        except:
            return self._generalError




    def readFirstname(self):
        try:
            temp = str(self.strFirstname)
            temp = temp.strip()
            temp = temp.title()

            if ((len(temp) <= self._maxNamesLen) and (len(temp) >= self._minNamesLen)):
                self.strFirstname = temp
                logging.info('READ FIRSTNAME SUCCESS' + self.strFirstname)
                return temp
            else:
                return self.undefined #corrupted data on string
        except:
            return self._generalError #returning nothing because there was an error


    def readSecondname(self):
        try:
            temp = str(self.strSecondname)
            temp = temp.strip()
            temp = temp.title()

            if ((len(temp) <= self._maxNamesLen) and (len(temp) >= self._minNamesLen)):
                self.strSecondname = temp
                logging.info('SECOND NAME WAS READ')
                return temp #returning a prepared string
            else:

                return self.undefined #corrupted data on string
        except:
            return self._generalError #returning an empty string

    def readSurname(self):
        try:
            temp = str(self.strSurname)
            temp = temp.strip()
            temp = temp.title()
            if ((len(temp) <= self._maxNamesLen) and (len(temp) >= self._minNamesLen)):
                logging.info('READ SURNAME SUCCESS')
                self.strSurname = temp
                return temp
            else:
                return self.undefined # corrupted data on string
        except:
            return self._generalError #an error occured somewhere returning an empty string


    def writeFirstname(self,name):
        try:
            name = str(name) #converting input to string
            name = name.strip() #striping the string
            name = name.title() # converting to lower case
            if ((name.isalpha()) and (len(name) <= self._maxNamesLen) and (len(name) >= self._minNamesLen)):
                self.strFirstname = name
                logging.info('WRITE FIRSTNAME SUCCESS')
                return True
            else:
                self.strFirstname = self.undefined
                return False
        except:
            return self._generalError

    def writeSecondname(self,name):
        try:
            name = str(name) # converting input to string
            name = name.strip() # stripping the input string
            name = name.title() # converting to lowercase
            if ((name.isalpha()) and (len(name) <= self._maxNamesLen) and (len(name) >= self._minNamesLen)):
                self.strSecondname = name
                logging.info('WRITE SECOND NAME SUCCESS')
                return True
            else:
                self.strSecondname = self.undefined
                return False
        except:
            return self._generalError


    def writeSurname(self, name):
        try:
            name = str(name) # converting input to string
            name = name.strip() # strpping the input string
            name = name.title() # converting to lowercase
            if ((name.isalpha()) and (len(name) <= self._maxNamesLen) and (len(name) >= self._minNamesLen)):
                self.strSurname = name
                logging.info('WRITE SURNAME SUCCESS')
                return True
            else:
                self.strSurname = self.undefined
                return False
        except:
            return self._generalError

    def readisValid(self):

        try:

            self.setIsValid()  # making sure valid has the latest value
            return self.isValid  # returning that value to the calling function
        except:
            return self._generalError

    def setIsValid(self):

        try:

            if not(self.readFirstname() == self.undefined):
                if not(self.readSurname() == self.undefined):
                    self.isValid = True
                else:
                    self.isValid = False
            else:
                self.isValid = False
        except:
            self.isValid = False





########################################################################################################################
########################################################################################################################
########################################################################################################################
#The private class contains private information of an individual
########################################################################################################################
########################################################################################################################
########################################################################################################################


class Private_info(db.Expando, MyConstants, ErrorCodes):

    _lowerage = 0
    _higherage = 120
    _minCriminalRecord = 2
    _maxCriminalRecord = 256
    _minDependents = 0
    _maxDependents = 256
    _minLanguageLen = 1
    _maxLanguageLen = 256

    _minCountryLen = 2
    _maxCountryLen = 256

    _minEthnicLen = 2
    _maxEthnicLen = 256
    _allGenders = ['male', 'female']


    indexReference = db.ReferenceProperty(Reference, collection_name='private_information') # Creating a reference link
    # to the Reference class
    strGender = db.StringProperty()  # Required Code Enforced
    strAge = db.StringProperty()
    strMarital_Status = undefined  # Required Code Enforced
    strDate_Birth = db.DateProperty()
    strCriminal_Record = undefined
    strDependants = undefined
    strHome_Language = undefined
    strPreferred_Language = undefined  # Required Code Enforced
    strNationality = undefined  # Required Code Enforced
    strEthnic_Group = undefined
    isValid = False
    DateTimeEdited = db.DateTimeProperty(auto_now=True)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def readDateTimeEdited(self):

        try:
            temp = self.DateTimeEdited
            return temp
        except:
            return self._generalError

    def readDateTimeCreated(self):

        try:
            temp = self.DateTimeCreated
            return temp
        except:
            return self._generalError


    def setIsValid (self):
        try:

            if not(self.readGender() == self.undefined):
                if not(self.readMarital_Status() == self.undefined):
                    if not(self.readPrefferedLanguage() == self.undefined):
                        if not(self.readNationality() == self.undefined):
                            self.isValid = True
                        else:
                            self.isValid = False
                    else:
                        self.isValid = False
                else:
                    self.isValid = False
            else:
                self.isValid = False
        except:
            self.isValid = False

    def readisValid (self):

        try:
            self.setIsValid()
            return self.isValid
        except:
            return self._generalError


    # Beginning Functions
    #this function reads the gender
    def readGender(self):

        try:
            logging.info('Read Gender Executed')
            temp = self.strGender.strip()
            temp = temp.lower()
            if temp == 'male':
                self.strGender = temp #making sure that if there was any corruption it is corrected
                return temp #return the corrected value to the calling procedure
            elif temp == 'female':
                self.strGender = temp #making sure that the corrected value gets stored back.
                return temp
            else:
                self.strGender = self.undefined
                return self.undefined
        except:
            return self._generalError


    # End of ReadGender Function
    #this function writes teh gender if it is anything other
    #than male or female it writes undefined

    def writeGender(self, strinput):
        try:
            strinput = str(strinput) #converting input to string in case it is in another format
            strinput = strinput.strip() #stripping leading and trailing spaces
            strinput = strinput.lower() #converting the input string to all lower case
            if strinput == 'male':
                self.strGender = 'male'
                return True
            elif strinput == 'female':
                self.strGender = 'female'
                return True
            else:
                self.strGender = self.undefined
                return False
        except:
            return self._generalError



    #this function will try to read the age if it is any value
    # not between 0 and 120 it returns zero

    def readAge (self):
        #this function does not return a number but a string.
        try:
            logging.info('Read Age Executed')
            temp = self.strAge.strip() #performing a strip function only and avoiding a lower case function

            if temp.isdigit():
                intage = int(temp)
                if ((intage >= self._lowerage) and (intage <= self._higherage)):
                    self.strAge = temp
                    return temp  # returning the stripped down text version of the number.
                else:
                    self.strAge = self.undefined
                    return self.undefined
            else:
                self.strAge = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeAge (self, strinput):

        try:
            strinput = str(strinput) #converting the input to string in case it is numeric or any other data type
            strinput = strinput.strip()
            if strinput.isdigit():
                intage = int(strinput)
                if (intage >= self._lowerage) and (intage <= self._higherage):
                    self.strAge = strinput
                    return True
                else:
                    self.strAge = self.undefined
                    return False
            else:
                self.strAge = self.undefined
                return False
        except:
            return self._generalError

    def readMarital_Status (self):
        try:
            logging.info('Read Marital Status Executed')
            temp = self.strMarital_Status.strip()
            temp = temp.lower()

            if temp == 'married':
                self.strMarital_Status = temp
                return 'married'
            elif temp == 'single':
                self.strMarital_Status = temp
                return 'single'
            elif temp == 'divorced':
                self.strMarital_Status = temp
                return 'divorced'
            elif temp == 'widow':
                self.strMarital_Status = temp
                return 'widow'
            elif temp == 'widower':
                self.strMarital_Status = temp
                return 'widower'
            else:
                self.strMarital_Status = self.undefined
                return self.undefined
        except:
            return self._generalError



    def writeMarital_Status (self,strinput):

        try:
            #convert the input to lower case
            strinput = str(strinput) #converting everything to string in case it is numeric
            strinput = strinput.strip()
            strinput = strinput.lower()

            if len(strinput) > 0:
                if strinput == 'single':
                    self.strMarital_Status = 'single'
                    return True
                elif strinput == 'married':
                    self.strMarital_Status = 'married'
                    return True
                elif strinput == 'divorced':
                    self.strMarital_Status = 'divorced'
                    return True
                elif strinput == 'widow':
                    self.strMarital_Status = 'widow'
                    return True
                elif strinput == 'widower':
                    self.strMarital_Status = 'widower'
                    return True
                else:
                    self.strMarital_Status = self.undefined
                    return False
            else:
                self.strMarital_Status = self.undefined
                return False
        except:
            return self._generalError


        #Decide on the format of the date of birth
        #Decide on the valid birth years bound them from minimum age to maximum age

    def readDateof_Birth(self):
        try:
            logging.info('READ DATE OF BIRTH EXECUTED')
            if self.strDate_Birth:
                strout = str(self.strDate_Birth.year) + '/'
                strout = strout + str(self.strDate_Birth.month) + '/'
                strout = strout + str(self.strDate_Birth.day)

                return strout
            else:
                logging.info('BIRTHDATE IS EMPTY ON READ OPERATIONS')
                return self.undefined

        except:
            return self._generalError


    def writeDateofBirth (self, strinput):
        try:
            if len(strinput) == 9:
                myear = int(strinput[0: 4])
                mmonth = int(strinput[5: 6])
                mday = int(strinput[7: 9])
                self.strDate_Birth = date(myear, mmonth, mday)
                logging.info(self.strDate_Birth)
                return True
            elif len(strinput) == 10:
                myear = int(strinput[0: 4])
                mmonth = int(strinput[5: 7])
                mday = int(strinput[8: 10])
                self.strDate_Birth = date(myear, mmonth, mday)
                logging.info(self.strDate_Birth)
                return True
            else:
                logging.info('INVALID DATETIME')
                return False
        except:
            logging.info('RAISING AN EXCEPTION ON WRITING BIRTHDATE')
            return self._generalError


    def readCriminalRecord (self):
        try:
            temp = str(self.strCriminal_Record)
            temp = temp.strip()
            temp = temp.lower()

            if (len(temp) <= self._maxCriminalRecord) and (len(temp) >= self._minCriminalRecord):
                self.strCriminal_Record = temp
                return temp
            else:
                self.strCriminal_Record = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeCriminalRecord (self,strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (len(strinput) <= self._maxCriminalRecord) and (len(strinput) >= self._minCriminalRecord):
                self.strCriminal_Record = strinput
                return True
            else:
                self.strCriminal_Record = self.undefined
                return False
        except:
            return self._generalError

    def readDependents (self):

        try:
            logging.info('Read Dependents executed')
            temp = str(self.strDependants)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.isdigit()) and (int(temp) >= self._minDependents) and (int(temp) <= self._maxDependents)):
                self.strDependants = temp
                return temp
            else:
                self.strDependants = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeDependents (self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.isdigit()) and (int(strinput) >= self._minDependents) and (int(strinput) <= self._maxDependents)):
                self.strDependants = strinput
                return True
            else:
                self.strDependants = self.undefined
                return False
        except:
            return self._generalError


    def readHomeLanguage (self):

        try:
            temp = str(self.strHome_Language)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.isalpha()) and (len(temp) >= self._minLanguageLen) and (len(temp) <= self._maxLanguageLen)):
                self.strHome_Language = temp
                return temp
            else:
                self.strHome_Language = self.undefined
                return self.undefined
        except:
            return self._generalError



    def writeHomeLanguage (self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.isalpha()) and (len(strinput) >= self._minLanguageLen) and (len(strinput) <= self._maxLanguageLen)):
                self.strHome_Language = strinput
                return True
            else:
                self.strHome_Language = self.undefined
                return False
        except:
            return self._generalError


    def readPrefferedLanguage(self):

        try:
            logging.info('Read Preffered Language Executed')
            temp = str(self.strPreferred_Language)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.isalpha()) and (len(temp) >= self._minLanguageLen) and (len(temp) <= self._maxLanguageLen)):
                self.strPreferred_Language = temp
                return temp
            else:
                self.strPreferred_Language = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writePreferredLanguage(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.isalpha()) and (len(strinput) >= self._minLanguageLen) and (len(strinput) <= self._maxLanguageLen)):
                self.strPreferred_Language = strinput
                return True
            else:
                self.strPreferred_Language = self.undefined
                return False
        except:
            return self._generalError


    def readNationality (self):

        try:

            temp = str(self.strNationality)
            temp = temp.strip()
            temp = temp.lower()
            logging.info('READ NATIONALITY EXECUTED REALLY WITH: '+ temp)
            if ((len(temp) >= self._minCountryLen) and (len(temp) <= self._maxCountryLen)):
                self.strNationality = temp
                return temp
            else:
                self.strNationality = self.undefined
                return self.undefined
        except:
            return self._generalError

    def writeNationality (self, strinput):

        try:
            logging.info('WRITE NATIONALITY EXECUTED: ' + strinput)

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()
            logging.info('ORIGINAL STRINPUT: '+ strinput)
            if ((len(strinput) >= self._minCountryLen) and (len(strinput) <= self._maxCountryLen)):
                self.strNationality = strinput
                logging.info('THIS IS ACTUALLY WRITTEN TO THE STORE: ' + strinput)
                return True
            else:
                self.strNationality = self.undefined
                return False
        except:
            return self._generalError



    def readEthnicGroup (self):

        try:

            temp = str(self.strEthnic_Group)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.isalpha()) and (len(temp) >= self._minEthnicLen) and (len(temp) <= self._maxEthnicLen)):
                self.strEthnic_Group = temp
                return temp
            else:
                self.strEthnic_Group = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeEthnicGroup (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.isalpha()) and (len(strinput) <= self._maxEthnicLen) and (len(strinput) >= self._minEthnicLen)):
                self.strEthnic_Group = strinput
                return True
            else:
                self.strEthnic_Group = self.undefined
                return False
        except:
            return self._generalError



#end of private class


#This class defines the Physical Address

class PhysicalAddress(db.Expando, MyConstants, ErrorCodes):

    #constants note this values can be changed by the program thereby allowing complete configuration.
    _maxStandNumberLen = 12
    _minStandNumberLen = 1

    _maxStreetNameLen = 120
    _minStreetNameLen = 1

    _maxCityTownLen = 120
    _minCityTownLen = 1

    _maxProvinceStateLen = 120
    _minProvinceStateLen = 1

    _maxPostalZipCodeLen  = 8
    _minPostalZipCodeLen = 4
    _utilityfunctions = Util()

    #Variables
    indexReference = db.ReferenceProperty(Reference, collection_name='physical_address')
    strStandNumber = undefined #Code Enforced Required Field
    strStreetName = undefined #Code Enforced Required Field
    strCityTown = undefined #Code Enforced Required Field
    strProvinceState = undefined #Optional Address Field
    strCountry = undefined # Required
    strPostalZipCode = undefined # Required
    isValid = False
    DateTimeEdited = db.DateTimeProperty(auto_now=True)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def readDateTimeEdited(self):
        try:
            temp = self.DateTimeEdited
            return temp
        except:
            return self._generalError

    def readDateTimeCreated(self):

        try:
            temp = self.DateTimeCreated
            return temp
        except:
            return self._generalError


    def readIsValid(self):

        try:
            self.setIsValid()
            return self.isValid
        except:
            return self._generalError


    def setIsValid(self):

        try:

            if not(self.readStandNumber() == self.undefined):
                if not(self.readStreetName() == self.undefined):
                    if not(self.readCityTown() == self.undefined):
                        if not(self.readCountry() == self.undefined):
                            if not(self.readPostalZipCode() == self.undefined):
                                self.isValid = True
                            else:
                                self.isValid = False
                        else:
                            self.isValid = False
                    else:
                        self.isValid = False
                else:
                    self.isValid = False
            else:
                self.isValid = False
        except:
            self.isValid = False



    def readStandNumber (self):

        try:
            logging.info('Read Stand Number Executed')
            temp = str(self.strStandNumber)
            temp = temp.strip()
            temp = temp.lower()


            if (len(temp) <= self._maxStandNumberLen) and (len(temp) >= self._minStandNumberLen):
                self.strStandNumber = temp
                logging.info('WE ARE ACTUALLY READING THIS ON STAND NUMBER: ' + temp)
                return temp
            else:
                self.strStandNumber = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeStandNumber (self, strinput):

        try:
            logging.info('WRITE Stand Number Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (len(strinput) <= self._maxStandNumberLen) and (len(strinput) >= self._minStandNumberLen):
                self.strStandNumber = strinput
                return True
            else:
                self.strStandNumber = self.undefined
                return False
        except:
            return self._generalError



    def readStreetName(self):

        try:
            logging.info('READ Street Name Executed')
            temp = str(self.strStreetName)
            temp = temp.strip()
            temp = temp.lower()


            if (len(temp) <= self._maxStreetNameLen) and (len(temp) >= self._minStreetNameLen):
                self.strStreetName = temp
                return temp
            else:
                self.strStreetName = self.undefined
                return self.undefined

        except:
            return self._generalError


    def writeStreetName(self, strinput):

        try:
            logging.info('WRITE STREET NAME EXECUTED')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (len(strinput) <= self._maxStreetNameLen) and (len(strinput) >= self._minStreetNameLen):
                self.strStreetName = strinput
                return True
            else:
                self.strStreetName = self.undefined
                return False
        except:
            return self._generalError


    def readCityTown (self):

        try:
            logging.info('READ CITY TOWN EXECUTED')
            temp = str(self.strCityTown)
            temp = temp.strip()
            temp = temp.lower()

            if (len(temp) <= self._maxCityTownLen) and (len(temp) >= self._minCityTownLen):
                self.strCityTown = temp
                return temp
            else:
                self.strCityTown = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeCityTown (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if ((len(strinput) <= self._maxCityTownLen) and (len(strinput) >= self._minCityTownLen)):
                self.strCityTown = strinput
                return True
            else:
                self.strCityTown = self.undefined
                return False
        except:
            return self._generalError



    def readProvinceState(self):

        try:
            logging.info('Read Province State Executed')
            temp = str(self.strProvinceState)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self._maxProvinceStateLen) and (len(temp) >= self._minProvinceStateLen)):
                self.strProvinceState = temp
                return temp
            else:
                self.strProvinceState = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeProvinceState(self, strinput):

        try:
            logging.info('WRITE PROVINCE STATE EXECUTED')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if ((len(strinput) <= self._maxProvinceStateLen) and (len(strinput) >= self._minProvinceStateLen)):
                self.strProvinceState = strinput
                return True
            else:
                self.strProvinceState = self.undefined
                return False
        except:
            return self._generalError


    def readCountry(self):

        try:
            logging.info('Read Country Executed')
            temp = str(self.strCountry)
            temp = temp.strip()
            temp = temp.title()

            if (self._utilityfunctions.isCountry(temp)):
                self.strCountry = temp
                return temp
            else:
                self.strCountry = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeCountry(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            if (self._utilityfunctions.isCountry(strinput)):
                self.strCountry = strinput
                return True
            else:
                self.strCountry = self.undefined
                return False
        except:
            return self._generalError


    def readPostalZipCode(self):

        try:
            logging.info('Read Postal ZIP Code Executed')
            temp = str(self.strPostalZipCode)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self._maxPostalZipCodeLen) and (len(temp) >= self._minPostalZipCodeLen)):
                self.strPostalZipCode = temp
                return temp
            else:
                self.strPostalZipCode = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writePostalZipCode(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) <= self._maxPostalZipCodeLen) and (len(strinput) >= self._minPostalZipCodeLen)):
                self.strPostalZipCode = strinput
                return True
            else:
                self.strPostalZipCode = self.undefined
                return False
        except:
            return self._generalError




class ContactDetails(CustomEmail, Website, db.Expando, MyConstants, ErrorCodes):

    #control constants
    _minCellLen = 10
    _maxCellLen = 13

    _minTelLen = 10
    _maxTelLen = 13

    _minFaxLen = 10
    _maxFaxLen = 13

    _minEmailLen = 5
    _maxEmailLen = 256

    _GooglePlusURL = 'https://plus.google.com'
    _minGooglePlusLen = 24
    _maxGooglePlusLen = 256

    _FacebookURL = 'http://facebook.com'
    _minFacebookLen = 21
    _maxFacebookLen = 256

    _TwitterURL = 'http://twitter.com'
    _minTwitterLen = 20
    _maxTwitterLen = 256

    _PinterestURL = 'http://pinterest.com'
    _minPinterestLen = 22
    _maxPinterestLen = 256

    _AboutMeURL = 'http://about.me'
    _minAboutMeLen = 17
    _maxAboutMeLen = 256

    _LinkeinURL = 'http://linkedin.com'
    _minLinkedinLen = 22
    _maxLinkedinLen = 256

    _WhosWhoURL = 'http://whoswho.co.za'
    _minWhosWhoLen = 22
    _maxWhosWhoLen = 256


    _minBlogLen = 4
    _maxBlogLen = 256

    _minWebsiteLen = _minBlogLen
    _maxWebsiteLen = _maxBlogLen



    #variables for storing data
    indexReference = db.ReferenceProperty(Reference, collection_name='contact_details')
    strCell = db.StringProperty() #Required Fields requirement enforced on code
    strTel = db.StringProperty()
    strFax = db.StringProperty()
    strEmail = db.EmailProperty() #Required Fields requirement enforced on code
    strGooglePlus = db.URLProperty()
    strFacebook = db.URLProperty()
    strTwitter = db.URLProperty()
    strPinterest = db.URLProperty()
    strAboutMe = db.URLProperty()
    strLinkedin = db.URLProperty()
    strWhosWho = db.URLProperty()
    strSkype = db.StringProperty()
    strWebsite = db.URLProperty()
    strBlog = db.URLProperty()
    isValid = False
    DateTimeEdited = db.DateTimeProperty(auto_now=True)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def readDateTimeEdited(self):
        try:
            temp = self.DateTimeEdited
            return temp
        except:
            return self._generalError

    def readDateTimeCreated(self):
        try:
            temp = self.DateTimeCreated
            return temp
        except:
            return self._generalError


    def readIsValid(self):

        try:

            self.setIsValid()
            return self.isValid
        except:
            return self._generalError

    def setIsValid(self):

        try:

            if not(self.readCell() == undefined):
                if not(self.readEmail() == undefined):
                    self.isValid = True

                else:
                    self.isValid = False
            else:
                self.isValid = False
        except:
            self.isValid = False



    #Trust Cloud and Smarterer will be included on the profile




    def readCell(self):

        try:
            logging.info('Read The Cell Phone')
            temp = str(self.strCell)
            temp = temp.strip()


            if (temp.isdigit() and (len(temp) <= self._maxCellLen) and (len(temp) >= self._minCellLen)):
                self.strCell = temp
                return temp
            else:
                self.strCell = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeCell(self, strinput):

        try:
            logging.info('Write Cell Executed')
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (len(strinput) <= self._maxCellLen) and (len(strinput) >= self._minCellLen)):
                self.strCell = strinput
                logging.info('Cell Value' + strinput)
                return True
            else:
                logging.info('unfortunately Cell Value not added')
                self.strCell = self.undefined
                return False
        except:
            return self._generalError

    def readTel(self):

        try:
            logging.info('Read Tel executed')
            temp = str(self.strTel)
            temp = temp.strip()

            if ((temp.isdigit()) and (len(temp) <= self._maxTelLen) and (len(temp) >= self._minTelLen)):
                self.strTel = temp
                return temp
            else:
                self.strTel = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeTel(self, strinput):

        try:
            logging.info('Write tel Executed')
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (len(strinput) <= self._maxTelLen) and (len(strinput) >= self._minTelLen)):
                self.strTel = strinput
                return True
            else:
                self.strTel = self.undefined
                return False
        except:
            return self._generalError


    def readFax(self):

        try:
            logging.info('Read fax executed')
            temp = str(self.strFax)
            temp = temp.strip()

            if ((temp.isdigit()) and (len(temp) <= self._maxFaxLen) and (len(temp) >= self._minFaxLen)):
                self.strFax = temp
                return temp
            else:
                self.strFax = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeFax(self, strinput):

        try:
            logging.info('write Fax Executed')
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (len(strinput) <= self._maxFaxLen) and (len(strinput) >= self._minFaxLen)):
                self.strFax = strinput
                logging.info('Fax Value Added' + strinput)
                return True
            else:
                self.strFax = self.undefined
                logging.info('Unfortunately fax value do not make it to datastore')
                return False
        except:
            return self._generalError

    def readEmail(self):

        try:
            temp = str(self.strEmail)
            temp = temp.strip()
            temp = temp.lower()
            #verifying an email with isemail is causing problems
            logging.info('Read Email Executed')
            if self.isemail(temp):
                self.strEmail = temp
                logging.info('Email Returned by Read Email')
                return temp
            else:
                self.strEmail = self.undefined
                logging.info('Email not returned by read')
                return self.undefined
        except:
            return self._generalError

    def writeEmail(self, strinput):

        try:
            logging.info('Write Email Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if self.isemail(strinput):
                self.strEmail = strinput
                logging.info('Email Address Written')
                return True
            else:
                self.strEmail = self.undefined
                return False
        except:
            return self._generalError

    def readWebsite(self):

        try:
            logging.info('Read Website Executed')
            temp = str(self.strWebsite)
            temp = temp.strip()
            temp = temp.lower()

            if self.iswebsite(temp):
                self.strWebsite = temp
                return temp
            else:
                self.strWebsite = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeWebsite(self, strinput):

        try:
            logging.info('Write Website Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if self.iswebsite(strinput):
                self.strWebsite = strinput
                return True
            else:
                self.strWebsite = self.undefined
                return False
        except:
            return self._generalError


    def readBlog(self):

        try:
            logging.info('read blog executed')
            temp = str(self.strBlog)
            temp = temp.strip()
            temp = temp.lower()

            if self.iswebsite(temp):
                self.strBlog = temp
                return temp
            else:
                self.strBlog = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeBlog(self, strinput):

        try:
            logging.info('Write Blog Executed:')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if self.iswebsite(strinput):
                self.strBlog = strinput
                return True
            else:
                self.strBlog = self.undefined
                return False
        except:
            return self._generalError


    def readGooglePlus(self):

        try:
            logging.info('Read GooglePlus Executed')
            temp = str(self.strGooglePlus)
            temp = temp.strip()
            temp = temp.lower()

            if((temp.startswith(self._GooglePlusURL)) and (len(temp) <= self._maxGooglePlusLen) and (len(temp) >= self._minGooglePlusLen)):
                self.strGooglePlus = temp
                return temp
            else:
                self.strGooglePlus = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeGooglePlus(self, strinput):

        try:
            logging.info('Write Google Plus Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._GooglePlusURL)) and (len(strinput) <= self._maxGooglePlusLen) and (len(strinput) >= self._minGooglePlusLen)):
                self.strGooglePlus = strinput
                return True
            else:
                self.strGooglePlus = self.undefined
                return False
        except:
            return self._generalError


    def readFacebook(self):

        try:
            logging.info('Read Facebook executed')
            temp = str(self.strFacebook)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._FacebookURL)) and (len(temp) <= self._maxFacebookLen) and (len(temp) >= self._minFacebookLen)):
                self.strFacebook = temp
                return temp
            else:
                self.strFacebook = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeFacebook(self, strinput):

        try:
            logging.info('write facebook executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._FacebookURL)) and (len(strinput) <= self._maxFacebookLen) and (len(strinput) >= self._minFacebookLen)):
                self.strFacebook = strinput
                logging.info('Succesfully writing facebook URL' + strinput)
                return True
            else:
                self.strFacebook = self.undefined
                return False
        except:
            return self._generalError


    def readTwitter(self):

        try:
            logging.info('read twitter executed')
            temp = str(self.strTwitter)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._TwitterURL)) and (len(temp) <= self._maxTwitterLen) and (len(temp) >= self._minTwitterLen)):
                self.strTwitter = temp
                return temp
            else:
                self.strTwitter = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeTwitter(self, strinput):

        try:
            logging.info('Write Twitter Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._TwitterURL)) and (len(strinput) <= self._maxTwitterLen) and (len(strinput) >= self._minTwitterLen)):
                self.strTwitter = strinput
                return True
            else:
                self.strTwitter = self.undefined
                return False
        except:
            return self._generalError

    def readPinterest(self):

        try:
            logging.info('Read Pinterest Executed')
            temp = str(self.strPinterest)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._PinterestURL)) and (len(temp) <= self._maxPinterestLen) and (len(temp) >= self._minPinterestLen)):
                self.strPinterest = temp
                return temp
            else:
                self.strPinterest = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writePinterest(self, strinput):

        try:
            logging.info('Write Pinterest Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._PinterestURL)) and (len(strinput) <= self._maxPinterestLen) and (len(strinput) >= self._minPinterestLen)):
                self.strPinterest = strinput
                return True
            else:
                self.strPinterest = self.undefined
                return False
        except:
            return self._generalError



    def readAboutMe(self):

        try:
            logging.info('Read About Me Executed')
            temp = str(self.strAboutMe)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._AboutMeURL)) and (len(temp) <= self._maxAboutMeLen) and (len(temp) >= self._minAboutMeLen)):
                self.strAboutMe = temp
                return temp
            else:
                self.strAboutMe = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeAboutMe(self, strinput):

        try:
            logging.info('Write About Me Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._AboutMeURL)) and (len(strinput) <= self._maxAboutMeLen) and (len(strinput) >= self._minAboutMeLen)):
                self.strAboutMe = strinput
                return True
            else:
                self.strAboutMe = self.undefined
                return False
        except:
            return self._generalError


    def readLinkedIn(self):


        try:
            logging.info('Read Linkedin Executed')
            temp = str(self.strLinkedin)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._LinkeinURL)) and (len(temp) <= self._maxLinkedinLen) and (len(temp) >= self._minLinkedinLen)):
                self.strLinkedin = temp
                return temp
            else:
                self.strLinkedin = self.undefined
                return self.undefined
        except:
            return self._generalError

    def writeLinkedIn(self, strinput):

        try:
            logging.info('Write Linkedin Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._LinkeinURL)) and (len(strinput) <= self._maxLinkedinLen) and (len(strinput) >= self._minLinkedinLen)):
                self.strLinkedin = strinput
                return True
            else:
                self.strLinkedin = self.undefined
                return False
        except:
            return self._generalError


    def readWhosWho(self):

        try:
            logging.info('Read Whos Who Executed')
            temp = str(self.strWhosWho)
            temp = temp.strip()
            temp = temp.lower()

            if ((temp.startswith(self._WhosWhoURL)) and (len(temp) <= self._maxWhosWhoLen) and (len(temp) >= self._minWhosWhoLen)):
                self.strWhosWho = temp
                return temp
            else:
                self.strWhosWho = self.undefined
                return self.undefined
        except:
            return self._generalError


    def writeWhosWho(self, strinput):

        try:
            logging.info('Write WhosWho Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((strinput.startswith(self._WhosWhoURL)) and (len(strinput) <= self._maxWhosWhoLen) and (len(strinput) >= self._minWhosWhoLen)):
                self.strWhosWho = strinput
                return True
            else:
                self.strWhosWho = self.undefined
                return False
        except:
            return self._generalError

    def readSkype(self):

        try:
            logging.info('Read Skype Executed')
            temp = str(self.strSkype)
            temp = temp.strip()
            temp = temp.lower()

            if self.isemail(temp):
                self.strSkype = temp
                return temp
            else:
                self.strSkype = self.undefined
                return self.undefined
        except:
            return self._generalError

    def writeSkype(self, strinput):

        try:
            logging.info('Write Skype Executed')
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if self.isemail(strinput):
                self.strSkype = strinput
                return True
            else:
                self.strSkype = self.undefined
                return False
        except:
            return self._generalError




#MAKE FINAL DECISION AS TO HOW I AM GOING TO IMPLEMENT THIS
#######################################################################################################################
#######################################################################################################################
#Begin of Address Class
#######################################################################################################################
#######################################################################################################################



class Address(MyConstants, ErrorCodes):


    PAddress = PhysicalAddress()
    CDetails = ContactDetails()

    def readPhysicalAddress(self):

        try:

            temp = PhysicalAddress()


            if temp.writeCityTown(self.PAddress.readCityTown()):
                if temp.writeCountry(self.PAddress.readCountry()):
                    if temp.writePostalZipCode(self.PAddress.readPostalZipCode()):
                        if temp.writeStreetName(self.PAddress.readStreetName()):
                            if temp.writeStandNumber(self.PAddress.readStandNumber()):
                                temp.writeProvinceState(self.PAddress.readProvinceState())
                                return temp
                            else:
                                return self.undefined
                        else:
                            return self.undefined
                    else:
                        return self.undefined
                else:
                    return self.undefined
            else:
                return self.undefined

        except:
            return self._generalError

    def writePhysicalAddress (self, clsinput):

        try:

            clsinput = PhysicalAddress(clsinput)


            if self.PAddress.writeCityTown(clsinput.readCityTown()):
                if self.PAddress.writeStandNumber(clsinput.readStandNumber()):
                    if self.PAddress.writePostalZipCode(clsinput.readPostalZipCode()):
                        if self.PAddress.writeCountry(clsinput.readCountry()):
                            if self.PAddress.writeStreetName(clsinput.readStreetName()):
                                #The Province or State Field is not Mandatory
                                #All the Other Fields are mandatory
                                self.PAddress.writeProvinceState(clsinput.readProvinceState())
                                return True
                            else:
                                return False
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


    def readContactDetails(self):

        try:

            temp = ContactDetails()



            if temp.writeCell(self.CDetails.readCell()):
                if temp.writeEmail(self.CDetails.readEmail()):
                    temp.writeWebsite(self.CDetails.readWebsite())
                    temp.writeWhosWho(self.CDetails.readWhosWho())
                    temp.writeBlog(self.CDetails.readBlog())
                    temp.writeTel(self.CDetails.readTel())
                    temp.writeFax(self.CDetails.readFax())
                    temp.writeSkype(self.CDetails.readSkype())
                    temp.writeGooglePlus(self.CDetails.readGooglePlus())
                    temp.writeFacebook(self.CDetails.readFacebook())
                    temp.writeTwitter(self.CDetails.readTwitter())
                    temp.writeLinkedIn(self.CDetails.readLinkedIn())
                    temp.writeAboutMe(self.CDetails.readAboutMe())
                    temp.writePinterest(self.CDetails.readPinterest())
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined

        except:
            return self._generalError

    def writeContactDetails(self, clsinput):

        try:

            clsinput = ContactDetails(clsinput)
            if self.CDetails.writeCell(clsinput.readCell()):
                if self.CDetails.writeEmail(clsinput.readEmail()):
                    self.CDetails.writeWebsite(clsinput.readWebsite())
                    self.CDetails.writeWhosWho(clsinput.readWhosWho())
                    self.CDetails.writeBlog(clsinput.readBlog())
                    self.CDetails.writeTel(clsinput.readTel())
                    self.CDetails.writeFax(clsinput.readFax())
                    self.CDetails.writeSkype(clsinput.readSkype())
                    self.CDetails.writeGooglePlus(clsinput.readSkype())
                    self.CDetails.writeFacebook(clsinput.readFacebook())
                    self.CDetails.writeTwitter(clsinput.readTwitter())
                    self.CDetails.writeLinkedIn(clsinput.readLinkedIn())
                    self.CDetails.writeAboutMe(clsinput.readAboutMe())
                    return True
                else:
                    return False

        except:
            return self._generalError




#Person is a control class where the logic for personal information gets executed
#input and output for reference class, names class, physical address class, private info class and contact details class
#will be maintained here
#all the search queries related to personal information will be executed here.as

class Person(db.Expando, MyConstants, ErrorCodes):


    #todo-VERY IMPORTANT FIND A WAY TO ENCRYPT AND DECRYPT DATA WHILE STORING IN THE DATASTORE
    #nOTE THE ENCRYPTION KEY COULD BE THE COMBINATION OF THE KEYVALUE USERNAME PASSWORD AND REFERENCE NUMBER
    #TODO- VERY IMPORTANT FIND A WAY TO CREATE A REFERENCE NUMBER GENERATOR FUNCTION FOR THE REFERENCE CLASS
    #NOTE THE REFERENCE GENERATOR FUNCTION SHOULD BE INCLUDED WITHIN THE REFERENCE CLASS AND ONLY CALLED WITH THE RELEVANT
    #VALUES OR IT MUST FIND A WAY TO READ THE PRESENT REFERENCE VALUE AND INCREMENT ON IT.
    #The Reference Generator function can create references and store them in the cache and when it is called
    #it can then first check to see if the Cache contains available References if it does it takes one out and
    #deletes it and then use it for the present user if it does not contain References it performs a calculation based
    #on the last Valid Reference stored on the Datastore
    #TODO-Find a way to store the last reference Used or at least find out what it is

    #todo-Create a friend list class and its related functionality
    #The friend list class is important as it allows persons to have relationship and to be able to share data
    clsReference = Reference()
    clsNames = Names()
    clsPrivate = Private_info()
    clsContactDetails = ContactDetails()
    clsPhysicalAddress = PhysicalAddress()

    #todo-The functions here must also take care of user login by using username and password
    #todo-try to intergrate the login functions with the google user accounts
    #todo-create the read and write functions for all the classes here they will help with the data input and output


    #Assuming that the present value of cls reference is the value i need to add to the datastore
    #returns the primary key value of the reference key
    #stores the reference key of the present user to _pkeyvalue

    def AddReferenceclasstoStore(self):

        try:

            if self.clsReference.readIsValid():
                #check to see if a reference record with the same username or with the same reference number exists
                #if it does abort if the error is the username inform the user with an error message or if the error
                #is the reference number inform the program in which case it should create a new reference number

                #The Add reference function Update
                #Check the supplied reference Number
                #Check the supplied Username
                #if there's a collision or something is wrong then specify this and do nothing


                if  (self.GetReferenceByRefNum(self.clsReference.readReference())  == self._referenceDoNotExist ):

                    if (self.getReferenceByUsername(self.clsReference.readUsername()) == self._userNameDonotExist):
                        self._pkeyvalue = self.clsReference.put() #Storing the primary key to _pkeyvalue and storing the
                        #reference class to the datastore
                        return self._pkeyvalue
                    else:
                        return self._userNameConflict
                else:
                    return self._referenceNumConflict

            else:
                return False
        except:
            return self._generalError


    def editReferenceByPkey(self):

        try:

            if (not(self._pkeyvalue == self.undefined) and (self.clsReference.readIsValid())):

                temp = Reference.get(self._pkeyvalue) # i am assuming that the pkey value will always be available as long as its set

                temp.writeReference(self.clsReference.readReference())
                temp.writeUsername(self.clsReference.readUsername())
                temp.writeIDNumber(self.clsReference.readIDNumber())
                temp.writePassword(self.clsReference.readPassword())

                if temp.readIsValid():
                    tempkey = temp.put()
                    return tempkey
                else:
                    return self.undefined
            else:
                return self._pkeyNotSet
        except:
            return self._generalError




    def getReferenceByPkey(self):

        try:

            if not(self._pkeyvalue == self.undefined):
                temp = Reference.get(self._pkeyvalue)
                return temp
            else:
                return self.undefined
        except:
            return self._generalError



     #This function returns The Reference Class itself or undefined
        #todo-in teh future investigate if some of this function cannot be a security risk as a certain user can
        #todo-realistically gather information about users and then attemp a hack on their accounts
    def GetReferenceByRefNum (self,strRefNum):

        try:
            #Check to see if strRefNum is valid
            #make sure strRefNum is a propertype
            #get it from the database and pass it as a function result

            strRefNum = str(strRefNum)
            strRefNum = strRefNum.strip()


            #Testing the length of the string
            temp = Reference()

            if temp.writeReference(strRefNum):
                #Then if this function succesfully wrote the reference number then it is valid
                strRefNum = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strRefNum)
                results = findquery.fetch(limit=self._maxQResults) #In case of Compatibility
                if len(results) > 0:
                    xReference = results[0]
                    self._pkeyvalue = xReference.key()
                    logging.info('Reference Class was found by Reference Number from store')
                else:
                    xReference = self._referenceDoNotExist
                    self._pkeyvalue = self.undefined

                return xReference
            else:
                self._pkeyvalue = self.undefined
                return self._referenceDoNotExist

        except:
            return self._generalError


    #with a certain IDNumber get a reference back
    def getReferenceByIDNumber (self, strIDNumber):

        try:
            #Check to see if IDnumber is valid
            #make sure the type is correct
            #get the id number from the database and pass the results on the function
            strIDNumber = str(strIDNumber)
            strIDNumber = strIDNumber.strip()

            temp = Reference()

            if temp.writeIDNumber(strIDNumber):
                strIDNumber = temp.readIDNumber()

                findquery = db.Query(Reference).filter('strIDNum =', strIDNumber)

                results = findquery.fetch(limit=self._maxQResults) #Returning upto max results this is in case of
                #compatibility


                if (len(results) > 0):
                    xReference = results[0]
                    self._pkeyvalue = xReference.key()

                else:
                    xReference = self.undefined
                    self._pkeyvalue = self.undefined

                return  xReference

            else:
                self._pkeyvalue = self.undefined
                return self.undefined

        except:
            return self._generalError

    #with a certain reference number get Reference Back
    #Note this functions will return a list of Reference Class
    def getReferenceByUsername(self, strinput):


        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            temp = Reference()

            if temp.writeUsername(strinput):
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =',strinput)

                results = findquery.fetch(limit=self._maxQResults)#Returning upto max results by default
                if len(results)> 0:
                    xReference = results[0]
                    self._pkeyvalue = xReference.key() #Setting teh pkeyvalue for the reference record
                else:
                    xReference = self._userNameDonotExist
                    self._pkeyvalue = self.undefined

                return xReference
            else:
                self._pkeyvalue = self.undefined
                return self._userNameDonotExist
        except:
            return self._generalError


    #Returns the number of results from the first item and cannot be more than the limit for the first page
    def getReferenceX(self,numAmount):

        try:

            numAmount = str(numAmount)
            numAmount = numAmount.strip()

            if numAmount.isdigit():

                numAmount = int(numAmount)
                if numAmount <= self._maxResults:

                    findquery = db.Query(Reference)

                    return findquery.fetch(limit=numAmount)
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError


    #returns the maximum number of results on a specific page of results one page is governed by _maxResults

    def getReferencePageX(self,numPage):

        try:

            numPage = str(numPage)
            numPage = numPage.strip()

            if numPage.isalnum():
                numPage = int(numPage)
                if ((numPage > 0) and (numPage <= (1000/self._maxResults))):
                    #1000 is the maximum results that Googlestore can return
                    findquery = db.Query(Reference)
                    results = findquery.fetch(limit= self._maxResults, offset= (numPage * self._maxResults))
                    #The Offset is equal to the page length multiplied by the page number
                    return results
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    #give a certin input as a reference number delete that entity from the datastore.

    def removeReferenceByRef (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()


            temp = Reference()

            if temp.writeReference(strinput):
                strinput = temp.readReference()

                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()

                    db.delete(keyvalue)
                    self._pkeyvalue = self.undefined
                    return True
                else:
                    return self._referenceDoNotExist
                #todo-investigate weather i have to manually remove all the instances of this user
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError


    def removeReferenceByIDNum(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()



            temp = Reference()

            if temp.writeIDNumber(strinput):
                strinput = temp.readIDNumber()
                findquery = db.Query(Reference).filter('strIDNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()
                    db.delete(keyvalue)
                    self._pkeyvalue = self.undefined
                    #todo-investigate weather i have to manually remove all the instances of this user
                    return True
                else:
                    return self._IDNumDonotExist
            else:
                return self._IDNumDonotExist
        except:
            return self._generalError


    def removeReferenceByUsername (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()


            temp = Reference()
            if temp.writeUsername(strinput):
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()
                    db.delete(keyvalue)
                    self._pkeyvalue = self.undefined #resetting the pkey value so it has undefined as we no longer have a valid
                    #Reference Record
                    #todo-investigate weather i have to manually remove all the instances of this user
                    #todo-it will seem we have to since we are left with orphaned classes without an owner on the datastore
                    #todo-the method can be to create a generic cleanup function which will delete all classes pointing to this one
                    #todo-using their reference key
                    #the user must be logged of after deleting their own Reference key since they no longer
                    ## have an account on the system
                    return True
                else:
                    return self._userNameDonotExist
            else:
                return self._userNameDonotExist
        except:
            return self._generalError



    #ADDING NAMES TO THE DATASTORE AND CREATING A RELATIONSHIP TO THE REFERENCE CLASS ALREADY ON THE DATASTORE
    ########################################################################################################################

    #with a certain reference add names class and create a relationship to the reference class stored on the datastore
    #return the keyvalue for the names class stored on the datastore if succesfull
    #return undefined if the names class is not valid
    #return reference do not exist error if the reference was not found
    #otherwise if an error occured it returns general error


    #The functions to addNames can practically add more than one name for the same USER or Reference Class find out
    #todo-consider wether to allow multiple names for single Reference Class or disbale this using Code

    def addNamesByRefNum(self, strinput):


        #Note the present record clsnames holds the information we need to add to the datastore
        #The function will return true if it succeeds or false if the names record is not correct or if there
        # was an error writing the record to the datastore
        #otherwise it will return an explanation for any error due to the reference number


        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()
            temp = Reference() #Temp will be used to insure that the input Reference Number is valid


            if temp.writeReference(strinput):
                #it is valid
                strinput = temp.readReference() #getting back the reference number we just wrote in

                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()

                    if self.clsNames.readisValid():
                        self.clsNames.indexReference = keyvalue
                        self._namesPkeyvalue = self.clsNames.put() #setting the _namesPkeyValue to the present Names Class Pkey
                        #the above statement also saves the Names class to the Datastore
                        return self._namesPkeyvalue #returning the keyvalue for the present class
                    else:
                        logging.info('NAMES CLASS NOT VALID')
                        self._namesPkeyvalue = self.undefined
                        return self._referenceDoNotExist
                else:
                    logging.info('THERES NO NAMES RECORD ADD A NEW ONE')
                    self._namesPkeyvalue = self.undefined
                    return self.undefined
            else:
                self._namesPkeyvalue = self.undefined
                return self._referenceDoNotExist
        except:
            return self._generalError


    #Returns the keyvalue for the saved class
    # or undefined if the names class is not valid
    # returns an erro _usernameDonot Exist if the username is bad or just is not available
    # in case of any general error it returns _generalError

    def addNamesbyUserName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            temp = Reference()

            if temp.writeUsername(strinput):
                #Then username is valid
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                temp = results[0]
                keyvalue = temp.key()
                if self.clsNames.readisValid():
                    self.clsNames.indexReference = keyvalue
                    self._namesPkeyvalue = self.clsNames.put() #saving the Names Class and returning the nameskeyvalue
                    #to the constants
                    return self._namesPkeyvalue #It returns the keyvalue for names class
                else:
                    return self.undefined

            else:
                return self._userNameDonotExist
        except:
            return self._generalError

    #this function assumes the reference primary key is stored on the _Pkeyvalue
    #this would be the case after logon or during initial user creation

    def addNamesbyRefPKey(self):

        try:

            if not(self._pkeyvalue == self.undefined): #checking to see if pkey contains a valid primary key for the user
                if self.clsNames.readisValid(): #checking to see if the Names class contains a valid class
                    self.clsNames.indexReference = self._pkeyvalue #create a relationship with the previously saved Reference
                    self._namesPkeyvalue = self.clsNames.put() #returns the pkey for Names and saves Names on the datastore
                    #also saves pkey value on the _namesPkeyValue
                    return self._namesPkeyvalue  #returning the pkey value
                else:
                    return self.undefined #the Names clas is not valid
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #this function assumes that the Names _pkey is stored on the _namesPkeyValue
    #this would be the case if the user was making changes to names record
    #on logon if the names class has already been created the names class pkey would also be loaded meaning the user can change this field

    def editNamesbyNamesPkey(self):

        try:

            if (not(self._namesPkeyvalue == self.undefined) and (self.clsNames.readisValid())):

                temp = Names.get(self._namesPkeyvalue)
                temp.writeFirstname(self.clsNames.readFirstname())
                temp.writeSurname(self.clsNames.readSurname())
                temp.writeSecondname(self.clsNames.readSecondname())

                if temp.readisValid():
                    resultKey = temp.put()
                    return resultKey
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    def getNamesbyRefNum(self, strinput):
        try:
            strinput = str(strinput)

            temp = Reference()

            if temp.writeReference(strinput): #checking to see if reference is valid
                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0] #Reference is a unique therefore it will return only one class
                    #searching the Names Class
                    findquery = db.Query(Names).filter('indexReference =', temp.key())
                    #returning results on the names class that matches
                    #the keyvalue for Reference

                    names_list = findquery.fetch(limit=self._maxQResults)

                else:
                    names_list = []

                if len(names_list) == 1:
                    temp = names_list[0]
                    self._namesPkeyvalue = temp.key()
                    return temp
                elif len(names_list) > 1:
                    logging.info('The Names record is returning more than one record for a single reference number the application is returning teh first occurence')
                    temp = names_list[0]
                    self._namesPkeyvalue = temp.key()
                    return temp
                else:
                    logging.info('Theres no names recording mathcing teh supplied Reference meaning a new one can be created')
                    self._namesPkeyvalue = self.undefined
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    #Taking a single USername it returns a list of names if more than one name is found this function will return allthe
    #names NOTE: a situation might arise where one Reference Class has many names if the person class does not take maeasures
    #to avoid the ability that this class might save more than one class for the same Reference Class
    def getNamesbyUsername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            temp = Reference()

            if temp.writeUsername(strinput):
                #Username is valid
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                temp = results[0] #Username is a unique field and results contains one field
                #Searching the Names Class
                findquery = db.Query(Names).filter('indexReference =', temp.key())

                names_list = findquery.fetch(limit=self._maxQResults)
                if len(names_list) == 1:
                    temp = names_list[0]
                    self._namesPkeyvalue = temp.key()
                    return temp
                elif len(names_list) > 1:
                    logging.info('Returning more than one Names class for one Username we are returning the first occurence')
                    temp = names_list[0]
                    self._namesPkeyvalue = temp.key()
                    return temp
                else:
                    logging.info('Theres no matching names record for the supplied Username')
                    self._namesPkeyvalue = self.undefined
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError


    #get names by firstname limiting the results to xnum and xnum is not more than maxresults
    def getNamesByFirstNamesX(self, strinput, xnum):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            xnum = str(xnum)
            xnum = xnum.strip()

            temp = Names()

            if ( xnum.isdigit() and temp.writeFirstname(strinput) and (int(xnum) <= self._maxResults) and (int(xnum > 0))):
                #then Name field is valid and xnum is within one page of results
                strinput = temp.readFirstname()
                findquery = db.Query(Names).filter('strFirstname =', strinput)
                xnum = int(xnum) #truning xnum into integer
                results = findquery.fetch(limit=xnum)
                return results
            else:
                return self.undefined
        except:
            return self._generalError


    def getNamesByFirstNamesPageX(self, strinput, xpages):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            xpages = str(xpages)
            xpages = xpages.strip()

            temp = Names()

            if (xpages.isdigit() and temp.writeFirstname(strinput) and (int(xpages) <= (self._googleResultLimit/self._maxResults)) and (int(xpages) >= 0)):
                #1000 is the number of total results GoogleStore can return at one time
                #therefore the maximum number of pages is equal to 1000 divide by maxresults
                strinput = temp.readFirstname()
                findquery = db.Query(Names).filter('strFirstname =', strinput)
                xpages = int(xpages)
                results = findquery.fetch(limit=self._maxQResults, offset= (xpages * self._maxResults))
                #this calculates the offset as the maximum page length multiplied by the page number
                #the first page is zero
                return results
            else:
                return self.undefined
        except:
            return self._generalError


    def getNamesBYSurnameX(self, strinput, xnum):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            xnum = str(xnum)
            xnum = xnum.strip()

            temp = Names()

            if (xnum.isdigit() and temp.writeSurname(strinput) and (int(xnum) <= self._maxResults) and (int(xnum > 0))):
                # a single page contains _maxResults of information
                strinput = temp.readSurname()
                findquery = db.Query(Names).filter('strSurname =', strinput).order('-strSurname')
                xnum = int(xnum)
                results = findquery.fetch(limit=self._maxQResults, offset=0) #Returns the first page
                return results
            else:
                return self.undefined
        except:
            return self._generalError
    # The Xpages functions are still limited by Google one thousand result limit
    #todo-Create another functions called BookX that goes to the next thousand and so on
    #protyp of the above mentioned function is (self, strinput, xpage, xbook)
    #the function will only return full pages for each page on a certain book

    def getNamesbySurnamePage(self, strinput, xpage):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            xpage = str(xpage)
            xpage = xpage.strip()

            temp = Names()

            if (xpage.isdigit() and temp.writeSurname(strinput) and (int(xpage) <=(self._googleResultLimit /self._maxResults)) and (int(xpage) >= 0)):
                strinput = temp.readSurname()
                findquery = db.Query(Names).filter('strSurname =', strinput).order('-strSurname')
                xpage = int(xpage)
                results = findquery.fetch(limit=self._maxQResults, offset=(self._maxResults * xpage))
                return results
            else:
                return self.undefined
        except:
            return self._generalError

    #Todo-Finish up with the Names class we are not nearly done : we need remove functions also

    #The function assumes the relevant reference Pkey is stored on _pkeyvalue
    #this happens after login or after you store the Reference class datastore

    def removeNamesByRefPkey(self):

        try:

            #The ref pkey is used as a reference field on the Names Class
            #so i can search for it there and locate the relevant class

            if not(self._pkeyvalue == self.undefined):

                findquery = db.Query(Names).filter('indexReference =', self._pkeyvalue)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key() #note that i could have called the delete function on the class itself
                    db.delete(keyvalue) #Actually removing the entry using its key value
                    self._namesPkeyvalue = self.undefined
                    return True
                else:
                    return self._pkeyNotSet
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #Assuming the Names pkey value is stored on the namespkeyvalue

    def removeNamesBynamesPKey(self):

        try:

            # The Names Pkey should be stored on the namespakey value

            if not(self._namesPkeyvalue == self.undefined):
                Names.delete(self._namesPkeyvalue) #using the primary key value only we can delete the record
                self._namesPkeyvalue = self.undefined
                return True
            else:
                return False
        except:
            return self._generalError

    #Assuming the reference is passed to this function by the calling function

    def removeNamesByRefNumber(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            #todo-THE FOLLOWING TRANSACTION NEED TO BE MADE ATOMIC
            if (temp.writeReference(strinput)):
                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()
                    findquery = db.Query(Names).filter('indexReference =', keyvalue)
                    #The keyvalue from the Reference Record is the same

                    #as the indexreference value on the Names record we need to delete
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        temp = results[0]
                        keyvalue = temp.key()
                        db.delete(keyvalue) #Using the Names key value to delete the Names Record
                        self._namesPkeyvalue = self.undefined # The names pkey value points to nothing
                        return True
                    else:
                        return self._clsNamesDonotExist
                else:
                    return self._referenceDoNotExist
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError



    def removeNamesbyUserName(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if (temp.writeUsername(strinput)):
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(self._maxResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()
                    findquery = db.Query(Names).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        temp = results[0]
                        keyvalue = temp.key()
                        db.delete(keyvalue) #Using the Names Keyvalue to delete the relevant class
                        self._namesPkeyvalue = self.undefined
                        return True
                    else:
                        return self._clsNamesDonotExist
                else:
                    return self._userNameDonotExist

            else:
                return self._userNameDonotExist

        except:
            return self._generalError

    #with the pkey for the Reference Class it Obtains the Names Class Pkey
    #assumption The Reference Pkey is valid
    #Assumption The Names class for this person is already saved on the Datastore

    #todo-Note that the friend list can be implemented right on the Reference class it can have a list of friends Pkeys
    #todo-this will give the user access to such a friend classes so that they can leave each other messages
    #todo-We can still implement the friends functionality separate but the friend list inside the Reference Class
    #todo- We can also consider interfacing this list with the users Facebook Friends, twitter friends, Google+ friends, and Linkein Friends
    def getNamesPkeyByRefPkey(self):

        try:

            if (not(self._pkeyvalue == self.undefined)):

                findquery = db.Query(Names).filter('indexReference', self._pkeyvalue)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) == 1:
                    result = results[0]
                    self._namesPkeyvalue = result.key()
                return self._namesPkeyvalue
            else:
                return self.undefined
        except:
            return self._generalError


    ###################################################################################################################
        #ENDING NAMES CLASS FUNCTIONS
    ###################################################################################################################

    ###################################################################################################################
        #BEGIN THE PRIVATE INFORMATION CLASS
    ###################################################################################################################


    #Assuming the Reference Key is stored on the pkeyvalue
    #and the the private information to be stored on the datastore is on the class
    def addPrivateInfoByRefPKey(self):

        try:

            if not(self._pkeyvalue == self.undefined):# The reference key is valid
                if self.clsPrivate.readisValid(): #The private information is valid
                    self.clsPrivate.indexReference = self._pkeyvalue #Setting the index value of the Reference
                    #field to the owner Reference Class
                    self._privatePkey = self.clsPrivate.put() #Saving the class to the DataStore and storing the Reference
                    #key to the privatePkey value
                    return self._privatePkey
                else:
                    return self.undefined
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #assuming the ReferenceNum gets passed to the function
    #and the Private Info containing the relevant information.
    def addPrivateInfoByReference(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()



            if (temp.writeReference(strinput) and self.clsPrivate.readisValid()): #Reference is correct
                #Private Class is valid
                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    self.clsPrivate.indexReference = temp.key() #setting the indexReference Value to refer to the right Reference
                    #Class
                    self._privatePkey = self.clsPrivate.put() #setting the privatePkey and saving the class to the Datastore
                    return self._privatePkey
                else:
                    self._privatePkey = self.undefined
                    return self._referenceDoNotExist
            else:
                return self.undefined
        except:
            return self._generalError

    #assuming the Username gets passed to the function
    #and the private info located on the person class
    def addPrivateInfobyUsername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #NOTE USERNAME CANNOT BE TURNED INTO LOWERCASE OR UPPERCASE IT MUST REMAIN AS IT IS

            temp = Reference()

            if (temp.writeUsername(strinput) and self.clsPrivate.readisValid()):
                #Private info is valid and Username is valid
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    self.clsPrivate.indexReference = temp.key()
                    self._privatePkey = self.clsPrivate.put()
                    return self._privatePkey
                else:
                    return self._userNameDonotExist
            else:
                return self.undefined
        except:
            return self._generalError

    #Todo-create a function to get Pkeys of each class provided they already exist
    def editPrivateInfobyPkey(self):

        try:
            #todo-use this method to edit all the classes it bypasses the need to copy the private key
            if (not(self._privatePkey == self.undefined)) and self.clsPrivate.readisValid():
                temp = Private_info.get(self._privatePkey)

                temp.writeAge(self.clsPrivate.readAge())
                temp.writeCriminalRecord(self.clsPrivate.readCriminalRecord())
                temp.writeEthnicGroup(self.clsPrivate.readEthnicGroup())
                temp.writeDateofBirth(self.clsPrivate.readDateof_Birth())
                temp.writeHomeLanguage(self.clsPrivate.readHomeLanguage())
                temp.writeDependents(self.clsPrivate.readDependents())
                temp.writePreferredLanguage(self.clsPrivate.readPrefferedLanguage())
                temp.writeGender(self.clsPrivate.readGender())
                temp.writeNationality(self.clsPrivate.readNationality())
                temp.writeMarital_Status(self.clsPrivate.readMarital_Status())

                if temp.readisValid(): #Note this takes care of verifying if all the required info is included
                    return temp.put() #returning the private pkey it will be a good idea to compare it with the original
                    #to see if they match which will mean that everything was a success
                else:
                    return self.undefined
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    #assumption this function must be provided with the username
    #returns a list of private information
    def getPrivateinfoByusername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            temp = Reference()


            if (temp.writeUsername(strinput)):

                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    keyvalue = temp.key()
                    findquery = db.Query(Private_info).filter('indexReference =', keyvalue)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        temp = results[0]
                        return temp
                    else:
                        return self._clsPrivateDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return self._userNameDonotExist
        except:
            return self._generalError


    #Assumption the function must be provided with the reference number
    #the function will return a list of Private information classes
    def getPrivateinfoByRefNum(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            #todo-findout try to keep the information such as the present Reference Class details on memory for the
            #todo-present logged in user so that we do not have to search the Database everytime a request is made
            #todo-this has to be thoroughly investigated
            if temp.writeReference(strinput):
                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) == 1:
                    temp = results[0]
                    keyvalue = temp.key()
                    findquery = db.Query(Private_info).filter('indexReference =', keyvalue)
                    logging.info('Private Information found by reference')

                    results = findquery.fetch(limit=self._maxQResults)

                    if len(results) == 1:
                        result = results[0]
                        self._privatePkey = result.key()
                    else:
                        logging.info('Private information not found by Reference')
                        result = self.undefined
                        self._privatePkey = self.undefined

                else:
                    logging.info('Supplied Reference Number has no matching record')
                    result = self.undefined
                    self._privatePkey = self.undefined
                #todo-if i decided that i will allow multiple records for one reference class then i must change the
                #todo-statement below to fetch not get so it can return multiple results

                return result
            else:
                return self.undefined
        except:
            return self._generalError

    #assuming the present private key is valid and the private information record has already been saved
    #returns the private information record
    def getPrivateInfobyPKey(self):

        try:

            if not(self._privatePkey == self.undefined):
                #the private key is probable right
                result = Private_info.get(self._privatePkey)
                if result.readisValid():
                    return result
                else:
                    return self.undefined
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    #Assuming the reference pkey is valid
    #Assuming there's a presently valid class saved on teh DataStore
    def getPrivateinfobyRefPKey(self):

        try:

            if not(self._pkeyvalue == self.undefined): #testing wether the Pkey value for Reference is valid
                findquery = db.Query(Private_info).filter('indexReference =', self._pkeyvalue)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    self._privatePkey = result.key() #Setting the private pkey
                    return result
                else:
                    result = self.undefined
                    self._privatePkey = self.undefined
                    return result

            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #this function will obtain the primary key for the private class given the primary key of the Reference Class
    #Assumption person class contains a valid Reference pkey
    #Assuptiom Private Class was previously saved to the datastore

    def getPrivatePkeyByRefPkey(self):
        try:

            if (not(self._pkeyvalue == self.undefined)):
                findquery = db.Query(Private_info).filter('indexReference =', self._pkeyvalue)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    self._privatePkey = result.key()
                    return self._privatePkey
                else:
                    self._privatePkey = self.undefined
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError
    #Given the Pkey value of Reference Delete the private class from the store and set its key to none on person class
    #Assumption pkeyvalue is valid
    #assumption private info is already stored on the datastore
    def removePrivateByRefPkey(self):
        try:

            if (not(self._pkeyvalue == self.undefined)):
                findquery = db.Query(Private_info).filter('indexReference =', self._pkeyvalue)
                results = findquery.fetch(self._maxResults)
                if len(results) > 0:
                    result = results[0]
                    db.delete(result.key()) #Deleting the Private Class from the store
                    self._privatePkey = self.undefined #setting the privatePkey to None
                    return True
                else:
                    return self._clsPrivateDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError
    #given Private own pkey delete its class from the datastore and set its pkeyvalue on the person class to zero
    #Assumption privatepkey value is valid
    #assumption private info is already stored on the datastore

    def removePrivateByPkey(self):
        try:

            if (not(self._privatePkey == self.undefined)):
                db.delete(self._privatePkey)
                self._privatePkey = self.undefined
                return True
            else:
                return self._pkeyNotSet
        except:
            return self._generalError
    #give the reference number find the related private class and remove it from the store and set is pkey value to undefine
    #Assumption Reference number is valid
    #Assumption private info is already on the datastore
    def removePrivateByRefNum(self, strinput):

        try:


            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()
            if (temp.writeReference(strinput)):

                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    keyvalue = result.key()
                    findquery = db.Query(Private_info).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        db.delete(result.key())
                        self._privatePkey = self.undefined
                        return True
                    else:
                        return self._clsPrivateDonotExist

                else:
                    return self._referenceDoNotExist
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError

    def removePrivateByUserName(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #username Case cannot be changed

            temp = Reference()

            if temp.writeUsername(strinput):
                strinput = temp.readUsername()

                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    keyvalue = result.key()
                    findquery = db.Query(Private_info).filter('indexReference =', keyvalue)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        db.delete(result.key())
                        self._privatePkey = self.undefined
                        return True
                    else:
                        return self._clsPrivateDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return  self._userNameDonotExist
        except:
            return self._generalError


    #######################################################################################################################
    #todo-Create Search Classes for reference that use private information Data
    #######################################################################################################################
    #TEMPORARY END OF THE PRIVATE INFORMATION CLASS SEARCH FUNCTIONS FOR THIS CLASS MUST STILL BE IMPLEMENTED
    #######################################################################################################################

    #######################################################################################################################
    #clsContactDetails = ContactDetails()
    #BEGIN OF THE CONTACT DETAILS CLASS
    #######################################################################################################################

    #Assuming the Present value of Ref Pkey is valid
    #Assuming the Present Contact Details class contains valid data



    def addContactDetailsbyRefPkey(self):
    #todo-VERY IMPORTANT IN ORDER TO MAKE SURE THAT DATA IS NOT ADDED TWICE FOR THE SUB CLASSES FROM REFERENCE SUCH AS
    #todo-CONTACT, PRIVATE AND NAMES WE HAVE TO INCLUDE CONTROL VARIABLES FOR EACH REFERENCE CLASS INDICATING WHICH CLASS
    #todo-HAS VALID DATA AND CAN ONLY BE EDITED.
        try:

            if((not(self._pkeyvalue == self.undefined)) and (self.clsContactDetails.readIsValid())):
                #both the Reference keyvalue and the Contact details class is valid
                self.clsContactDetails.indexReference = self._pkeyvalue
                self._contactPkey = self.clsContactDetails.put()
                #We saved the contact class to the Datastore and retain the key on _contactPkey
                return self._contactPkey
            else:
                return self.undefined
        except:
            return self._generalError


    #assuming the contact pkey field contains valid data
    #the contact pkey value can be populated by any method or fuction that retrieves the class from the store
    #we also assume that the contact class data contained here are valid
    def editContactDetailsbyPkey(self):

        try:

            if ((not(self._contactPkey == self.undefined)) and (self.clsContactDetails.readIsValid())):
                #todo-Check if we have to initialize the domain store from here
                #todo-or we just have to include all the initial domains as part of the program for the time being
                #This method of editing avoids having to read the primary key of the class thats returned
                result = ContactDetails.get(self._contactPkey)
                result.writeCell(self.clsContactDetails.readCell())
                result.writeAboutMe(self.clsContactDetails.readAboutMe())
                result.writeBlog(self.clsContactDetails.readBlog())
                result.writeEmail(self.clsContactDetails.readEmail())
                result.writeFacebook(self.clsContactDetails.readFacebook())
                result.writeWhosWho(self.clsContactDetails.readWhosWho())
                result.writeFax(self.clsContactDetails.readFax())
                result.writeGooglePlus(self.clsContactDetails.readGooglePlus())
                result.writeLinkedIn(self.clsContactDetails.readLinkedIn())
                result.writePinterest(self.clsContactDetails.readPinterest())
                result.writeSkype(self.clsContactDetails.readSkype())
                result.writeTwitter(self.clsContactDetails.readTwitter())
                result.writeTel(self.clsContactDetails.readTel())
                result.writeWebsite(self.clsContactDetails.readWebsite())
                #check if data is still valid and save
                if result.readIsValid():
                    return result.put() #saving the data to the store and returning the primary key
                    #compare this key to the one stored on the self_contactPkey to see if it never changed

                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError



    #Assumption the calling function must pass the username field
    #Assumption two the contact details class is valid on the person class
    #Assumption there's no Contact Class on the datastore for this user or multi record is allowed


    def addContactDetailsByUsername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #username case cannot be changed

            temp = Reference()


            if (temp.writeUsername(strinput) and (self.clsContactDetails.readIsValid())):
                strinput = temp.readUsername()
                findQuery = db.Query(Reference).filter('strUsername =', strinput)
                results = findQuery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    keyvalue = result.key()
                    self.clsContactDetails.indexReference = keyvalue
                    self._contactPkey = self.clsContactDetails.put()
                    return self._contactPkey
                else:
                    self._contactPkey = self.undefined
                    return self._userNameDonotExist
            else:
                return self.undefined
        except:
            return self._generalError


    #Assumption the calling function must submit the reference number
    #The Person class must include valid contact data
    #The Datastore must not contain another instance of this information unless we allow multi records for each user
    def addContactDetailsByRefNum(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            temp = Reference()

            if(temp.writeReference(strinput) and self.clsContactDetails.readIsValid()):

                logging.info('Contact Details Search Reference is valid and the class to be added is valid')
                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    self.clsContactDetails.indexReference = result.key()
                    self._contactPkey = self.clsContactDetails.put()
                    logging.info('Contact Details was found matching the Reference')
                    return self._contactPkey
                else:
                    self._contactPkey = self.undefined
                    logging.info('Contact Details was not found by the supplied Reference number')
                    return self._referenceDoNotExist
            else:
                logging.info('Trace : AddContactDetailsByRefNum either reference is not valid or contact details is not valid')
                return self.undefined
        except:
            return self._generalError


    #todo this function must be implemented for all classes the ability to use the RefPkey to get their Pkeys
    #Assumption Reference pkey is valid
    #Assumption Contact Class is already saved on the datastore
    def getContactPkeyByRefPkey(self):

        try:

            if (not(self._pkeyvalue == self.undefined)):

                findquery = db.Query(ContactDetails).filter('indexReference =', self._pkeyvalue)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    self._contactPkey = result.key()
                    return self._contactPkey
                else:
                    self._contactPkey = self.undefined
                    return self._clsContactDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #given the Reference Key obtains the Contact Details class and saves its pkey
    #Assumption Reference Pkey is valid
    #Assumtion Contact Details Class is already present
    def getContactDetailsbyRefPkey(self):

        try:

            if not(self._pkeyvalue == self.undefined):

                findquery = db.Query(ContactDetails).filter('indexReference =', self._pkeyvalue)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    self._contactPkey = result.key() #Saving the key for the present contact details
                    return result  #returning the contact Details as requested
                else:
                    self._contactPkey = self.undefined # We know for sure that the contact record do not exist
                    return self._clsContactDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    #Give the Username obtain the contact details
    #assumption username is valid
    #assumption contact details class is already present on the datastore

    def getContactDetailsByUserName(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #username cannot be small letters
            temp = Reference()

            if temp.writeUsername(strinput):
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    keyvalue = result.key()
                    findquery = db.Query(ContactDetails).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]

                        self._contactPkey = result.key()
                        return result
                    else:
                        self._contactPkey = self.undefined
                        return self._clsContactDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return self._userNameDonotExist
        except:
            return self._generalError

    #Give the reference Number obtain the Contact Details class
    #Assumption The Reference Numebr is valid
    #Assumption the contact details class is already on the datastore

    def getContactDetailsByRefNum (self, strinput):


        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if temp.writeReference(strinput):

                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)

                results = findquery.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    result = results[0]

                    keyvalue = result.key()
                    findquery = db.Query(ContactDetails).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        self._contactPkey = result.key()
                        logging.info('Contact Details was found matching the Reference Key Suplied')
                    else:
                        result = self.undefined
                        self._contactPkey = self.undefined
                        logging.info('Contact Details was not found for the reference supplied')
                else:
                    result = self._referenceDoNotExist
                    self._contactPkey = self.undefined
                    logging.info('Reference Number Supplied was not found the user might not be logged in')


                return result
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError

    #Given The Private Key of the reference Class remove Contact Details and set contactpkey to undefined
    #assumption Reference PKey is valid
    #Assumption Contact Details is already on the datastore

    def removeContactDetailsByRefPkey(self):


        try:

            if (not(self._pkeyvalue == self.undefined)):

                findquery = db.Query(ContactDetails).filter('indexReference =', self._pkeyvalue)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    db.delete(result.key())
                    self._contactPkey = self.undefined
                    return True
                else:
                    return self._clsContactDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    #Given The Contact details Pkey remove it from the store and set its pkey to undefined on the person class
    #assumption pkey is valid
    #Asumption pkey is already on the store

    def removeContactDetailsbyPkey(self):

        try:

            if (not(self._contactPkey == self.undefined)):
                db.delete(self._contactPkey)
                self._contactPkey = self.undefined
                return True
            else:
                return self._pkeyNotSet
        except:
            return  self._generalError

    def removeContactDetailsByUsername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #username cannot be set to lower case

            temp = Reference()

            if (temp.writeUsername(strinput)):
                strinput = temp.readUsername()

                findquery = db.Query(Reference).filter('strUsername =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    keyvalue = result.key()
                    findquery = db.Query(ContactDetails).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]

                        db.delete(result.key())
                        self._contactPkey = self.undefined
                        return True
                    else:
                        return self._clsContactDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return self._userNameDonotExist
        except:
            return self._generalError

    #Given the refencerence number this function will delete the contact details that goes with that reference
    #Assumption The Reference Number is valid
    #Assumption the contatc details class is present on the DataStore
    def removeContactDetailsbyRefNum(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if temp.writeReference(strinput):
                strinput = temp.readReference()

                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    keyvalue = result.key()
                    findquery = db.Query(ContactDetails).filter('indexReference =', keyvalue)

                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]

                        db.delete(result.key())
                        self._contactPkey = self.undefined
                        return True
                    else:
                        return self._clsContactDonotExist
                else:
                    return self._referenceDoNotExist
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError


    #Given a Reference Class Key it returns the Physical Address class that goes with it from the store and set the key
    #Assumption The Reference Pkey is Valid
    #Assumption The Physical Address Class on the Person Class is Valid

    def addPhysicalAddressByRefPKey(self):

        try:

            if (not(self._pkeyvalue == self.undefined) and (self.clsPhysicalAddress.readIsValid())):

                self.clsPhysicalAddress.indexReference = self._pkeyvalue
                self._physicalAddressPkey = self.clsPhysicalAddress.put()
                return self._physicalAddressPkey
            else:
                return self.undefined
        except:
            return self._generalError



    def editPhysicalAddressByPkey(self):

        try:

            if (not(self._physicalAddressPkey == self.undefined) and (self.clsPhysicalAddress.readIsValid())):

                result = PhysicalAddress.get(self._physicalAddressPkey)
                result.writeCityTown(self.clsPhysicalAddress.readCityTown())
                result.writeCountry(self.clsPhysicalAddress.readCountry())
                result.writePostalZipCode(self.clsPhysicalAddress.readPostalZipCode())
                result.writeProvinceState(self.clsPhysicalAddress.readProvinceState())
                result.writeStandNumber(self.clsPhysicalAddress.readStandNumber())
                result.writeStreetName(self.clsPhysicalAddress.readStreetName())

                if result.readIsValid():
                    return result.put()
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError


    #With a certain username store the physical address retain the physicaladdresspkey
    #Assumption Username is valid
    #Assumption The Physical Address Class is at least valid on the person class

    def addPhysicalAddressByUserName(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #No Case conversion for username

            temp = Reference()

            if ((temp.writeUsername(strinput)) and (self.clsPhysicalAddress.readIsValid())):

                strinput = temp.readUsername() #Unnecessary step
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if (len(results) > 0):
                    result = results[0]
                    keyvalue = result.key()
                    self.clsPhysicalAddress.indexReference = keyvalue #Setting the Reference Field
                    self._physicalAddressPkey = self.clsPhysicalAddress.put()
                    #Saving to Datastore and returning the Pkey
                    return self._physicalAddressPkey
                else:
                    return self._userNameDonotExist
            else:
                return self.undefined
        except:
            return self._generalError



    #Given a Reference = Add the Physical Address located on the person Class and retain the physical address key
    #Assumption Reference Number if Valid
    #Assumption the Physical Address class located on the person class is valid



    def addPhysicalAddressByRefNum(self, strinput):

        try:


            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if (temp.writeReference(strinput) and self.clsPhysicalAddress.readIsValid()):

                strinput = temp.readReference()

                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)

                if (len(results) > 0):
                    result = results[0]
                    self.clsPhysicalAddress.indexReference = result.key()
                    self._physicalAddressPkey = self.clsPhysicalAddress.put()
                    return self._physicalAddressPkey
                else:
                    return self._referenceDoNotExist
            else:
                return self.undefined
        except:
            return self._generalError


    def getPhysicalAddressByRefPKey (self):

        try:

            if (not(self._pkeyvalue == self.undefined)):
                findquery = db.Query(PhysicalAddress).filter('indexReference =',self._pkeyvalue)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    self._physicalAddressPkey = result.key()
                    return result
                else:
                    self._physicalAddressPkey = self.undefined
                    return self._clsPhysicalDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    def getPhysicalAddressByRefnum(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if (temp.writeReference(strinput)):

                strinput = temp.readReference()
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if (len(results) > 0):
                    result = results[0]
                    keyvalue = result.key()
                    findquery = db.Query(PhysicalAddress).filter('indexReference =', keyvalue)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        self._physicalAddressPkey = result.key()
                        return result
                    else:
                        self._physicalAddressPkey = self.undefined
                        logging.info(self._clsPhysicalDonotExist)
                        return self._clsPhysicalDonotExist
                else:

                    return self._referenceDoNotExist

            else:
                return self._referenceDoNotExist
        except:
            return self._generalError


    def getPhysicalAddressByPkey(self):

        try:

            if not(self._physicalAddressPkey == self.undefined):
                return  self.clsPhysicalAddress.get(self._physicalAddressPkey)
            else:
                return self._pkeyNotSet
        except:
            return self._generalError



    def getPhysicalAddressByUsername(self, strinput):


        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            temp = Reference()

            if temp.writeUsername(strinput):
                strinput = temp.readUsername()

                findquery = db.Query(Reference).filter('strUsername =', strinput)

                results = findquery.fetch(limit=self._maxQResults)
                if (len(results) > 0):
                    result = results[0]
                    keyvalue = result.key()
                    findquery = db.Query(PhysicalAddress).filter('indexReference =', keyvalue)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        self._physicalAddressPkey = result.key()
                        return result
                    else:
                        self._physicalAddressPkey = self.undefined
                        return self._clsPhysicalDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return self.undefined
        except:
            return self._generalError


    def removePhysicalAddressByRefPKey (self):

        try:

            if (not(self._pkeyvalue == self.undefined)):

                findquery = db.Query(PhysicalAddress).filter('indexReference =', self._pkeyvalue)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    keyvalue = result.key
                    db.delete(keyvalue)
                    self._physicalAddressPkey = self.undefined
                    return True
                else:
                    return self._clsPhysicalDonotExist
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def removePhysicalAddressByRefNum (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            temp = Reference()

            if temp.writeReference(strinput):
                strinput = temp.readReference()

                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    keyvalue = result.key()
                    findquery = db.Query(PhysicalAddress).filter('indexReference =', strinput)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        db.delete(result.key)
                        self._physicalAddressPkey = self.undefined
                        return True
                    else:
                        return self._clsPhysicalDonotExist
                else:
                    return self._referenceDoNotExist
            else:
                return self._referenceDoNotExist

        except:
            return self._generalError

    def removePhysicalAddressByUsername(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            #No Case Change for username

            temp = Reference()

            if temp.writeUsername(strinput):
                strinput = temp.readUsername()
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    result = results[0]
                    keyvalue = result.key()
                    findquery = db.Query(PhysicalAddress).filter('indexReference =', keyvalue)
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        db.delete(result.key())
                        self._physicalAddressPkey = self.undefined
                        return True
                    else:
                        return self._clsPhysicalDonotExist
                else:
                    return self._userNameDonotExist
            else:
                return self.undefined
        except:
            return self._generalError

    def removePhysicalAddressByPKey(self):

        try:

            if not(self._physicalAddressPkey == self.undefined):
                db.delete(self._physicalAddressPkey)
                self._physicalAddressPkey = self.undefined
                return True
            else:
                return self._pkeyNotSet
        except:
            return self._generalError