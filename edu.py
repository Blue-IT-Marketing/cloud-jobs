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



#The Address Records will stay by themselves on the address class that inherits from Physical Address and contact Details
#The Person Record will have private information class and address class plus Contact Details (Contact details are contained inside the address
#The Profile Record will inherit the person record and add Educational Qualifications and skills of the person
#The Portfolio Record will inherit the profile record and add the users portfolio that also links to external portfolios
#The freelancer Record will have the Portfolio record plus added functionality to submit and bid on freelance jobs
#The Jobs Record will take the Portfolio record and add functionality to submit jobs and also apply for jobs
# The jobs record can also be called the employer record.
#The complete Record will combine the freelancer record and the Jobs record.
###########END OF THE PERSON RECORD##############################################################
#################################################################################################
#################################################################################################
#To create the profile record we need to create complete educational and skills records##########
#################################################################################################
#################################################################################################

from datatypes import Reference, PhysicalAddress, ContactDetails, Names, Private_info, Address, LegalYearLimit
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from ConstantsAndErrorCodes import MyConstants, ErrorCodes
import logging


#This class defines a high school
class HighSchool (db.Expando, MyConstants, ErrorCodes):

    _minSchoolNameLen = 2
    _maxSchoolNameLen = 256
    _SchoolPhysicalAddress = PhysicalAddress()
    _SchoolContactDetails = ContactDetails()
    _contactPersonAccount = Reference()
    _contactPersonNames = Names()
    _contactPersonPrivateInfo = Private_info()
    _SchoolRecordCreator = Reference()

    # The ownership of subclasses contact details and physical address classes will be taken by contact person
    #from the reference class this Reference classes can be selected by their collection names

    strSchoolName = db.StringProperty()
    IndexSchoolRecordCreator = db.ReferenceProperty(Reference, collection_name='high_school_collection_owner')
    IndexSchoolPhysicalAddress = db.ReferenceProperty(PhysicalAddress, collection_name='high_school_collection')
    IndexSchoolContactDetails = db.ReferenceProperty(ContactDetails, collection_name='high_school_collection')
    IndexContactPersonAccount = db.ReferenceProperty(Reference, collection_name='high_school_collection')
    IndexContactPersonNames = db.ReferenceProperty(Names, collection_name='high_school_collection')
    IndexContactPersonPrivateInf = db.ReferenceProperty(Private_info, collection_name='high_school_collection')

    isValid = db.BooleanProperty(default=False)
    isVerified = db.BooleanProperty(default=False) #Verification of the School Existence, We can do from other Social Networks such as Facebook
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    DateTimeModified = db.DateTimeProperty(auto_now=True)
    DateVerified = db.DateTimeProperty()


    # Date Verified must be written in this format
    '''

    class Book(db.Model):
        title = db.StringProperty(required=True)
        author = db.StringProperty(required=True)
        copyright_year = db.IntegerProperty()
        author_birthdate = db.DateProperty()
        obj = Book(title='The Grapes of Wrath',
        author='John Steinbeck')
        obj.copyright_year = 1939
        obj.author_birthdate = datetime.date(1902, 2, 27)
    '''
    def readIsValid(self):
       try:
           if self.setIsValid():
                return self.isValid
           else:
               return self.undefined
       except:
           return self._generalError

    def setIsValid(self):
        try:
            if (self.IndexContactPersonAccount == self.undefined) and (self.IndexSchoolRecordCreator == self.undefined) and (self.IndexContactPersonNames == self.undefined) and (self.strSchoolName == self.undefined):
                self.isValid = True
                return True
            else:
                self.isValid = False
                return True
        except:
            return False

    # Read is verified must check to see if the verification process is complete once its not complete notify the
    # user and
    # check to see when was the last time the verification email or sms was sent if its more than seven days then send
    # it again by calling set is verified
    #TODO FINISH UP READ IS VERIFIED
    def readIsVerified(self):
        pass

    # set is verified must actually call initiate the verification function such as sending a verification email to the school email address
    # once this function finishes running, it must exit.
    #TODO FINISH UP SET IS VERIFIED
    def setIsVerified(self):
        pass
    #TODO FINISH UP WRITE DATE VERIFIED
    def writeDateVerified(self, strinput):
        pass


    def readSchoolRecordCreator(self):
        try:
            if not(self.IndexSchoolRecordCreator == self.undefined):
                return self.IndexSchoolRecordCreator
            else:
                return self.undefined
        except:
            return self._generalError



    def writeSchoolRecordCreator(self, strinput):
        try:

            Guser = users.get_current_user()

            if Guser:
                strinput = str(strinput)
                strinput = strinput.strip()

                if strinput.isalnum():
                    self.IndexSchoolRecordCreator = strinput
                    return True
                else:
                    self.IndexSchoolRecordCreator = self.undefined
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def retrieveRecordCreator(self):
        try:

            if not(self.IndexSchoolRecordCreator == self.undefined):
                tCreator = Reference.get(self.IndexSchoolRecordCreator())
                if tCreator.readIsValid():
                    self._SchoolRecordCreator = tCreator
                    return tCreator
                else:
                    return self.undefined
            else:
                return self._clsReferenceDonotExist
        except:
            return self._generalError


    #Save Record Creator cannot create a new record but can only update an existing one
    def saveRecordCreator(self):
        try:

            Guser = users.get_current_user()

            if Guser:
                findquery = db.Query(Reference).filter('strReference =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    dRef = Reference.get(result.key())

                    if dRef.readReference() == self._SchoolRecordCreator.readReference():

                        dRef.writeIDNumber(self._SchoolRecordCreator.readIDNumber())
                        dRef.writeDateTimeVerified(self._SchoolRecordCreator.readDatetimeVerified())
                        dRef.writeIsUserVerified(self._SchoolRecordCreator.readIsUserVerified())
                        dRef.writeLogoPhoto(self._SchoolRecordCreator.readLogoPhoto())
                        dRef.writePassword(self._SchoolRecordCreator.readPassword())
                        dRef.writeReference(self._SchoolRecordCreator.readReference())
                        dRef.writeUsername(self._SchoolRecordCreator.readUsername())
                        dRef.writeVerEmail(self._SchoolRecordCreator.readVerEmail())

                        self.clsSchoolRecordCreator = dRef.put()
                        return self.clsSchoolRecordCreator()
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError





    def readSchoolName(self):
        try:
            logging.info('READ SCHOOL NAME WAS CALLED')
            temp = str(self.strSchoolName)
            temp = temp.strip()
            temp = temp.title()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSchoolName(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:

                strinput = str(strinput)
                strinput = strinput.strip()
                strinput = strinput.lower()

                if (len(strinput) <= self._maxSchoolNameLen) and (len(strinput) >= self._minSchoolNameLen):
                    self.strSchoolName = strinput
                    return True
                else:
                    self.strSchoolName = self.undefined
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def readPhysicalAddress(self):
        try:
            temp = str(self.IndexSchoolPhysicalAddress)
            temp = temp.strip()


            if temp.isalnum():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writePhysicalAddress(self, strinput):
        try:
            temp = str(strinput)
            logging.info('WRITE PHYSICAL ADDRESS EXECUTED: ' + temp)

            if len(temp) > 0:
                self.IndexSchoolPhysicalAddress = strinput
                return True
            else:
                logging.info('SHOWING FALSE ON WRITING PHYSICAL ADRESS')
                return False
        except:
            logging.info('THROWING EXCEPTIONS')
            return self._generalError




    def retrievePhysicalAddress(self):
        try:

            if not(self.IndexSchoolPhysicalAddress() == self.undefined):
                tPhysAddress = PhysicalAddress.get(self.IndexPhysicalAddress())
                if tPhysAddress.readIsValid():
                    return tPhysAddress
                else:
                    return self.undefined
            else:
                return self._clsPhysicalDonotExist
        except:
            return self._generalError


    def savePhysicalAddress(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if self._SchoolPhysicalAddress.readIsValid():
                    if self.IndexSchoolPhysicalAddress() == self.undefined:
                        self.IndexSchoolPhysicalAddress = self._SchoolPhysicalAddress.put()
                        return self.IndexSchoolPhysicalAddress()
                    else:
                        tPhysical = PhysicalAddress.get(self.IndexSchoolPhysicalAddress())
                        if tPhysical.readIsValid():
                            tPhysical.writeCityTown(self._SchoolPhysicalAddress.readCityTown())
                            tPhysical.writeCountry(self._SchoolPhysicalAddress.readCountry())
                            tPhysical.writePostalZipCode(self._SchoolPhysicalAddress.readPostalZipCode())
                            tPhysical.writeProvinceState(self._SchoolPhysicalAddress.readProvinceState())
                            tPhysical.writeStandNumber(self._SchoolPhysicalAddress.readStandNumber())
                            tPhysical.writeStreetName(self._SchoolPhysicalAddress.readStreetName())

                            self.IndexSchoolPhysicalAddress = tPhysical.put()
                            return self.IndexSchoolPhysicalAddress()
                        else:
                            return self._PhysicalAddressINvalid
                else:
                    return self._PhysicalAddressINvalid
            else:
                return self._userNotLoggedin

        except:
            return self._generalError




    def readContactDetails(self):
        try:
            if not(self.IndexSchoolContactDetails == self.undefined):
                return self.IndexSchoolContactDetails
            else:
                return self.undefined
        except:
            return self._generalError


    def writeContactDetails(self, strinput):
        try:

            Guser = users.get_current_user()

            if Guser:

                strinput = str(strinput)
                strinput = strinput.strip()

                if strinput.isalnum():
                    self.IndexSchoolContactDetails = strinput
                    return True
                else:
                    self.IndexSchoolContactDetails = self.undefined
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def retrieveContactDetails(self):
        try:

            if not(self.IndexSchoolContactDetails == self.undefined):
                return self.IndexSchoolContactDetails
            else:
                return self.undefined
        except:
            return self._generalError



    def saveContactDetails(self):
        try:

            Guser = users.get_current_user()

            if Guser:

                if self._SchoolContactDetails.readIsValid():
                    if self.IndexSchoolContactDetails == self.undefined:
                        tempkey = self._SchoolContactDetails.put()

                        if self.writeContactDetails(tempkey):
                            return tempkey
                        else:
                            return self.undefined

                    else:
                        tSchoolContacts = ContactDetails.get(self.IndexSchoolContactDetails())
                        if tSchoolContacts.readIsValid():
                            tSchoolContacts.writeAboutMe(self._SchoolContactDetails.readAboutMe())
                            tSchoolContacts.writeBlog(self._SchoolContactDetails.readBlog())
                            tSchoolContacts.writeCell(self._SchoolContactDetails.readCell())
                            tSchoolContacts.writeEmail(self._SchoolContactDetails.readEmail())
                            tSchoolContacts.writeFacebook(self._SchoolContactDetails.readFacebook())
                            tSchoolContacts.writeFax(self._SchoolContactDetails.readFax())
                            tSchoolContacts.writeGooglePlus(self._SchoolContactDetails.readGooglePlus())
                            tSchoolContacts.writeLinkedIn(self._SchoolContactDetails.readLinkedIn())
                            tSchoolContacts.writePinterest(self._SchoolContactDetails.readPinterest())
                            tSchoolContacts.writeSkype(self._SchoolContactDetails.readSkype())
                            tSchoolContacts.writeTel(self._SchoolContactDetails.readTel())
                            tSchoolContacts.writeTwitter(self._SchoolContactDetails.readTwitter())
                            tSchoolContacts.writeWebsite(self._SchoolContactDetails.readWebsite())
                            tSchoolContacts.writeWhosWho(self._SchoolContactDetails.readWhosWho())
                            tempkey = tSchoolContacts.put()

                            if self.writeContactDetails(tempkey):
                                return tempkey
                            else:
                                return self.undefined
                        else:
                            return self._ContactDetailsInvalid

                else:
                    return self._ContactDetailsInvalid
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



    def readContactPerson(self):

        try:

            if not(self.IndexContactPersonAccount == self.undefined):
                return self.IndexContactPersonAccount
            else:
                return self._SchoolContactPersonDoNotExist
        except:
            return self._generalError


    def writeContactPerson(self, strinput):

        try:

            Guser = users.get_current_user()

            if Guser:
                strinput = str(strinput)
                strinput = strinput.strip()
                Tref = Reference.get(strinput)
                if Tref.readIsValid():
                    self.IndexContactPersonAccount = Tref.key()
                    return True
                else:
                    self.IndexContactPersonAccount = self.undefined
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def retrieveContactPerson(self):
        try:

            if not(self.IndexContactPersonAccount == self.undefined):
                tempref = Reference.get(self.IndexContactPersonAccount)
                if tempref.readIsValid():
                    return tempref
                else:
                    return self.undefined
            else:
                return self._ContactPersonDoNotExist
        except:
            return self._generalError



    # First The contact person class must already exist
    # Check to see if the person logged in is the owner of the school record for which the contact person is being
    # saved.
    #TODO-CREATE AN INTERNAL NOTIFICATION MESSAGING SYSTEM FOR SYSTEM CHANGES SUCH AS BEING MADE A CONTACT PERSON
    # FOR A SCHOOL
    def saveContactPerson(self):
        try:

            Guser = users.get_current_user()

            if Guser:
                ORef = self.retrieveRecordCreator()
                if not(ORef == self.undefined) or not(ORef == self._generalError) or not(ORef == self._clsReferenceDonotExist):
                    if ORef.readIsValid():
                        if ORef.readReference() == Guser.user_id(): # We succesfully verified record ownership
                            #Verify that the contact person already exist
                            if not(self.IndexContactPersonAccount == self.undefined):
                                CRef = self.retrieveContactPerson()
                                if not(CRef == self.undefined) or not(CRef == self._ContactPersonDoNotExist) or not(CRef == self._generalError):
                                    # Contact Person already Exist
                                    # Check if self._contactPersonAccount is Valid and the References Match
                                    if self._contactPersonAccount.readIsValid() and (self._contactPersonAccount.readReference() == CRef.readReference()):
                                        CRef.writeVerEmail(self._contactPersonAccount.readVerEmail())
                                        CRef.writeUsername(self._contactPersonAccount.readUsername())
                                        CRef.writeReference(self._contactPersonAccount.readReference())
                                        CRef.writePassword(self._contactPersonAccount.readPassword())
                                        CRef.writeDateTimeVerified(self._contactPersonAccount.readDatetimeVerified())
                                        CRef.writeIDNumber(self._contactPersonAccount.readIDNumber())
                                        CRef.writeIsUserVerified(self._contactPersonAccount.readIsUserVerified())
                                        CRef.writeLogoPhoto(self._contactPersonAccount.readLogoPhoto())

                                        if CRef.readIsValid():
                                            self.IndexContactPersonAccount = CRef.put()
                                            return self.IndexContactPersonAccount
                                        else:
                                            return self._SchoolContactPersonInvalid
                                    else:
                                        return self._ContactPersonDoNotExist
                                else:
                                    return self._ContactPersonDoNotExist
                            else:
                                return self._ContactPersonDoNotExist
                        else:
                            return self._UserNotAuthorised
                    else:
                        return self._AccountDetailsInvalid
                else:
                    return self._SchoolContactPersonDoNotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError













class Tertiary (db.Expando):
    strInstitutionName = db.StringProperty()
    clsPhysicalAddress = PhysicalAddress()
    clsContactDetails = ContactDetails()
    clsContactPerson = Names()
    isValid = db.BooleanProperty(default=False)
    isVerified = db.BooleanProperty(default=False) #Verification of the School Existence, can also be conducted through Social Networks
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    DateModified = db.DateTimeProperty(auto_now=True)



    def readInstitutionName(self):
        pass
    def writeInstitutionName(self):
        pass
    def readPhysicalAddress(self):
        pass
    def writePhysicalAddress(self):
        pass
    def readContactDetails(self):
        pass
    def writeContactDetails(self):
        pass
    def readContactPerson(self):
        pass
    def writeContactPerson(self):
        pass
    def readIsValid(self):
        pass
    def setIsValid(self):
        pass
    def readIsVerified(self):
        pass
    def setIsVerified(self):
        pass





class SubjectandMarks (MyConstants,ErrorCodes):



    _maxSubjectLen = 256
    _minSubjectLen = 1
    _maxSubjectMark = 100
    _minSubjectMark = 0
    _maxSubjectLevel = 12
    _minSubjectLevel = 0
    _maxSubjectCodeLen = 8
    _minSubjectCodeLen = 0
    _maxSubjectGrade = 12
    _minSubjectGrade = 0
    _maxNameofInstitutionLen = 256
    _minNameofInstitutionLen = 1




    strSubject = db.StringProperty()
    strTotalMark = db.StringProperty()
    strTotalLevel = db.StringProperty()
    strSubjectCode = db.StringProperty()
    strSubjectGrade = db.StringProperty()

    def readSubject (self):
        try:
            temp = str(self.strSubject)
            temp = temp.strip()
            temp = temp.title()
        except:
            return self._generalError


    def writeSubject (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.title()

            if ((strinput.isalnum()) and (len(strinput) <= self._maxSubjectLen) and (len(strinput) >= self._minSubjectLen)):
                self.strSubject = strinput
                return True
            else:
                self.strSubject = self.undefined
                return False
        except:
            return self._generalError


    def readTotalMark (self):

        try:

            temp = str(self.strTotalMark)
            temp = temp.strip()


            if ((temp.isdigit()) and (int(temp) <= self._maxSubjectMark) and (int(temp) >= self._minSubjectMark)):
                self.strTotalMark = temp
                return temp
            else:
                return self.undefined
        except:
            return  self._generalError



    def writeTotalMark (self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (int(strinput) <= self._maxSubjectMark) and (int(strinput) >= self._minSubjectMark)):
                self.strTotalMark = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readTotalLevel (self):

        try:

            temp = str(self.strTotalLevel)
            temp = temp.strip()



            if ((temp.isdigit()) and (int(temp) <= self._maxSubjectLevel) and (int(temp) >= self._minSubjectLevel)):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeTotalLevel (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (int(strinput) <= self._maxSubjectLevel) and (int(strinput) >= self._minSubjectLevel)):
                self.strTotalLevel = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    def readSubjectCode (self):

        try:

            temp = str(self.strSubjectCode)
            temp = temp.strip()

            if ((temp.isalnum()) and (len(temp) == self._maxSubjectCodeLen)):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeSubjectCode (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isalnum()) and (len(strinput) == self._maxSubjectCodeLen)):
                self.strSubjectCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readSubjectGrade (self):

        try:

            temp = str(self.strSubjectGrade)
            temp = temp.strip()

            if ((temp.isdigit()) and (int(temp) <= self._maxSubjectGrade) and (int(temp) >= self._minSubjectGrade)):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSubjectGrade (self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if ((strinput.isdigit()) and (int(strinput) <= self._maxSubjectGrade) and (int(strinput) >= self._minSubjectGrade)):
                self.strSubjectGrade = strinput
                return True
            else:
                return False
        except:
            return self._generalError




#this class defines the list of subjects
class lstSubjectsMarks (SubjectandMarks):

    # the original value on the list is undefined and a real value will be stored on the first run
    lstSubjectsAndMarks = db.ListProperty(item_type=str) #Stores all the subjects and their marks in a list of subjects



    #read a certain value on the subjects marks list
    # if this is the first read it will return undefined
    #teh read functions read values on ram and also write values on ram without worrying about where the values will be
    # stored as this decision will influence the platform such as Google App Engine or any other platform
    # for Google App Engine then the storage functions will be written on a separate module and for any other platform
    def readSubjectsMarks (self, strindex):

        try:

            strindex = str(strindex)
            strindex = strindex.strip()


            if ((strindex.isdigit()) and (int(strindex) <= (len(self.lstSubjectsAndMarks) - 1)) and (int(strindex) >= 0)):
                # we have determined that the passed value is digit and within bounds of the list
                # then we can return that value
                return self.lstSubjectsAndMarks[int(strindex)]
            else:
                return self.undefined
        except:
            return self.undefined




    #write the subjects marks on a certain index

    def writeSubjectsMarks (self, clsinput, strindex):


        try:

            strindex = str(strindex)
            strindex = strindex.strip()


            if ((strindex.isdigit()) and (int(strindex) <= (len(self.lstSubjectsAndMarks) - 1)) and (int(strindex) >= 0)):
                #now that we know the index is valid we can continue to write the SubjectMarks Class

                if (clsinput.readSubject() <> self.undefined): #testing to see if the data is valid
                    intStrindex = int(strindex)
                    self.lstSubjectsAndMarks.append(clsinput, intStrindex)
                    return True
                else:
                    return False
            else: #something is wrong with the index
                return False
        except:
            return False



    # Adding new subjects and marks at the end of the list
    def addSubjectsMarks (self, clsinput):

        try:



            #if this is the first time the following test will evaluate to true meaning the undefined field will be removed.

            if (self.lstSubjectsAndMarks[0] == self.undefined):
                self.lstSubjectsAndMarks.remove(self.undefined)


            if not(clsinput.readSubject() == self.undefined):
                self.lstSubjectsAndMarks.append(clsinput)
                self.lstSubjectsAndMarks.sort()
                return True
            else:
                return False

        except:
            return False


    def removeSubjectsMarks (self, clsinput):

        try:
            self.lstSubjectsAndMarks.remove(clsinput)
            self.lstSubjectsAndMarks.sort()

            return True
        except:
            return False





    # Searching the subjects and marks list using subject name if found return the rest of the subject



    def searchSubjectsMarksBySubjectName (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if (len(self.lstSubjectsAndMarks) > 0):
                i = 0
                while (i < (len(self.lstSubjectsAndMarks))):
                    temp = self.lstSubjectsAndMarks[i]
                    if (strinput == temp.readSubject()):
                        return temp
                    else:
                        i = i + 1
            else:
                return self.undefined
        except:
            return self.undefined

    def searchSubjectsMarksbySubjectCode (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (len(self.lstSubjectsAndMarks) > 0):
                i = 0
                while (i < (len(self.lstSubjectsAndMarks))):
                    temp = self.lstSubjectsAndMarks[i]
                    if (strinput == temp.readSubjectCode()):
                        return temp
                    else:
                        i = i + 1
            else:
                return self.undefined
        except:
            return self.undefined


    #Searches the subject marks list and return all the subjects on a specific grade and its more likely to return all
    #the subjects in the list as they could belong to the same person. and might be listed as subjects for highest grade
    # passed. so this function will return a list

    def searchSubjectsMarksBySubjectGrade (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if (len(self.lstSubjectsAndMarks) > 0 ):
                i = 0
                j = 0
                templist = lstSubjectsMarks()
                while (i < (len(self.lstSubjectsAndMarks))):
                    temp = self.lstSubjectsAndMarks[i]

                    if (strinput == temp.readSubjectGrade()):
                        templist[j] = temp
                        j = j + 1
                        i = i + 1
                    else:
                        i = i + 1
                return templist
            else:
                return self.undefined
        except:
            return self.undefined


    def searchSubjectsMarksByTotalMark (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (len(self.lstSubjectsAndMarks) > 0):
                i = 0
                j = 0
                templist = lstSubjectsMarks()
                while (i < (len(self.lstSubjectsAndMarks))):
                    temp = self.lstSubjectsAndMarks[i]

                    if (strinput == temp.readTotalMark()):
                        templist[j] = temp
                        j = j + 1
                        i = i + 1
                    else:
                        i = i + 1
                return templist
            else:
                return self.undefined
        except:
            return self.undefined


    def searchSubjectsMarksbyTotalLevel (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if (len(self.lstSubjectsAndMarks) > 0):
                i = 0
                j = 0
                templist = lstSubjectsMarks()
                while (i < (len(self.lstSubjectsAndMarks))):
                    temp = self.lstSubjectsAndMarks[i]

                    if (strinput == temp.readTotalLevel()):
                        templist[j] = temp
                        j = j + 1
                        i = i + 1
                    else:
                        i = i + 1
                return templist
            else:
                return self.undefined
        except:
            return self.undefined


####################################################################################################################
####################################################################################################################
####################################################################################################################






#This is a HighSchool Qualifications Class

class HighSchoolQualifications (db.Expando, MyConstants, ErrorCodes):
    _maxSchoolGrade = 12
    _minSchoolGrade = 0

    indexReference = db.ReferenceProperty(Reference, collection_name='high_school_qualifications')
    strHighestGradePassed = db.StringProperty()
    HighSchoolIndex = db.ReferenceProperty(HighSchool, collection_name='high_school')
    strYearPassed = db.StringProperty()
    lstSubjectsAndMarks = db.ListProperty(item_type=str) # List of reference numbers to the subject mark class

    strNotes = db.StringProperty(multiline=True)

    isvalid = db.BooleanProperty(default=False)

    DateCreated = db.DateProperty(auto_now_add=True)
    DateModified = db.DateProperty(auto_now=True)

    def readOwnerIndex(self):
        try:
            temp = str(self.indexReference)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeOwnerIndex(self, strinput):
        try:
            temp = str(strinput)


            if len(temp) > 0:
                self.indexReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readHighSchoolIndex(self):
        try:
            temp = self.HighSchoolIndex()
            temp = str(temp)
            logging.info('HIGH SCHOOL INDEX :' + temp)

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeHighSchoolIndex(self, strinput):
        try:

            temp = str(strinput)
            logging.info('TRYING TO WRITE THIS HIGH SCHOOL INDEX : ' + temp)
            if len(temp) > 0:
                self.HighSchoolIndex = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def RetrieveHighSchool(self):
        try:
            temp = self.HighSchoolIndex()
            temp = str(temp)

            if len(temp) > 0:
                tHighSchool = HighSchool.get(self.HighSchoolIndex())
                return tHighSchool
            else:
                return self.undefined
        except:
            logging.info('AN EXCEPTION OCCURED RETRIEVING HIGH SCHOOL')
            return self._generalError

    def readHighestGradePassed (self):

        try:

            temp = str(self.strHighestGradePassed)
            temp = temp.strip()


            if ((temp.isdigit()) and (int(temp) <= self._maxSchoolGrade) and (int(temp) >= self._minSchoolGrade)):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeHighestGradePassed (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()


            if ((strinput.isdigit()) and (int(strinput) <= self._maxSchoolGrade) and (int(strinput) >= self._minSchoolGrade)):
                self.strHighestGradePassed = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    def readYearPassed(self):

        try:

            temp = str(self.strYearPassed)
            temp = temp.strip()


            #calculating maxLegalYear and MinLegalYear
            today = datetime.datetime.now()
            maxLegalYear = today.year
            minLegalYear = maxLegalYear - LegalYearLimit

            if ((temp.isdigit()) and (int(temp) <= maxLegalYear) and (int(temp) >= minLegalYear)):
                self.strYearPassed = temp
                return temp
            else:
                self.strYearPassed = self.undefined
                return self.undefined
        except:
            self.strYearPassed = self.undefined
            return self.undefined


    def writeYearPassed (self, strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()


            #calculating maxLegalYear and MinLegalYear
            today = datetime.datetime.now()
            maxLegalYear = today.year
            minLegalYear = maxLegalYear - LegalYearLimit


            if ((strinput.isdigit()) and (int(strinput) <= maxLegalYear) and (int(strinput) >= minLegalYear)):
                self.strYearPassed = strinput
            else:
                self.strYearPassed = self.undefined
        except:
            self.strYearPassed = self.undefined




    def readSubjectsPassed (self):

        try:

            temp = self.lstSubjectsAndMarks


            if len(temp) >= 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSubjectsPassed (self, lstinput):

        try:
            lstinput = lstinput.sort()


            if len(lstinput) >= 0:
                self.lstSubjectsAndMarks = lstinput
                return True
            else:
                return False
        except:
            return self._generalError





    # Add a subject to subject list if success it returns 1 if fail it returns 0


    def addSubjectPassed (self,clsSubjectMark):

        try:
            if ((len(clsSubjectMark.readSubject()) > 0) and (len(clsSubjectMark.readSubjectGrade()) > 0) ):
                self.lstSubjectsAndMarks.append(clsSubjectMark)
                self.lstSubjectsAndMarks.sort()
                return True
            else:
                return False
        except:
            return self._generalError


    def removeSubjectPassed (self, clsSubjectMark):

        try:
            self.lstSubjectsAndMarks.remove(clsSubjectMark)
            self.lstSubjectsAndMarks.sort()
            return True

        except:
            return self._generalError


########################################################################################################################
########################################################################################################################
##############################  TERTIARY INSTITUTION -------------------------------------------------------------------
########################################################################################################################
########################################################################################################################


#more functionality could be added on the subject field.

class TertiaryQualifications (db.Expando):

    _minCourseLen = 2
    _maxCourseLen = 256

    _minNotesLen  = 2
    _maxNotesLen = 1056


    indexReference = db.ReferenceProperty(Reference, collection_name='tertiary_qualifications')
    #find the right values for specialization on WhosWho
    _lstSpecialization = []

    strCourseStudied = db.StringProperty()
    strSpecializaton = db.StringProperty()
    TertiaryIndex = db.ReferenceProperty(Tertiary, collection_name='tertiary')

    lstSubjectsPassedandMarks = lstSubjectsMarks()  #empty list
    strNotes = db.StringProperty(multiline=True)
    isValid = db.BooleanProperty(default=False)
    DateCreated = db.DateProperty(auto_now_add=True)
    DateModified = db.DateProperty(auto_now=True)

    def readCourseStudied (self):
        try:
            temp = str(self.strCourseStudied)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) >= self._minCourseLen) and (len(temp) <= self._maxCourseLen) and (temp.isalnum())):
                self.strCourseStudied = temp
                return temp
            else:
                self.strCourseStudied = self.undefined
                return self.undefined
        except:
            self.strCourseStudied = self.undefined
            return self.undefined


    def writeCourseStudied (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) >= self._minCourseLen) and (len(strinput) <= self._maxCourseLen) and (strinput.isalnum())):
                self.strCourseStudied = strinput
                return True
            else:
                self.strCourseStudied = self.undefined
                return False

        except:
            self.strCourseStudied = self.undefined
            return False


    def readSpecialization (self):

        try:

            temp = str(self.strSpecializaton)
            temp = temp.strip()
            temp = temp.lower()


            if (temp in self._lstSpecialization):
                self.strSpecializaton = temp
                return temp
            else:
                self.strSpecializaton = self.undefined
                return self.undefined
        except:
            self.strSpecializaton = self.undefined
            return self.undefined


    def writeSpecialization (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if (strinput in self._lstSpecialization):
                self.strSpecializaton = strinput
                return True
            else:
                self.strSpecializaton = self.undefined
                return False
        except:
            self.strSpecializaton = self.undefined
            return False


    def readNameofInstitution (self):

        try:

            temp = str(self.strNameofInstitution)
            temp = temp.strip()
            temp = temp.lower()


            if ((len(temp) <= self._maxNameofInstitutionLen) and (len(temp) >= self._minNameofInstitutionLen) and (temp.isalnum())):
                self.strNameofInstitution = temp
                return temp
            else:
                self.strNameofInstitution = self.undefined
                return self.undefined
        except:
            self.strNameofInstitution = self.undefined
            return self.undefined

    def writeNameOfInstitution (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) <= self._maxNameofInstitutionLen) and (len(strinput) >= self._minNameofInstitutionLen)):
                self.strNameofInstitution = strinput
                return strinput
            else:
                self.strNameofInstitution = self.undefined
                return self.undefined
        except:
            self.strNameofInstitution = self.undefined
            return self.undefined


    def readclsAddressofInstitution (self):

        try:
            temp = Address()
            temp.writePhysicalAddress(self.clsAddressOfInstitution.readPhysicalAddress())
            temp.writeContactDetails(self.clsAddressOfInstitution.readContactDetails())
            return temp
        except:
            return self.undefined

    def writeclsAddressofInstitution (self, clsinput):

        try:

            clsinput = Address(clsinput)


            self.clsAddressOfInstitution.writePhysicalAddress(clsinput.readPhysicalAddress())
            self.clsAddressOfInstitution.writeContactDetails(clsinput.readContactDetails())

            return True
        except:
            return False


    def readlstSubjectsPassedAndMarks (self):

        try:

            temp = self.lstvarSubjectsMarks

            if ((len(self.lstSubjectsPassedandMarks.lstSubjectsAndMarks) > 0) and (self.lstSubjectsPassedandMarks.lstSubjectsAndMarks[0] <> self.undefined )):
                return temp
            else:
                return self.undefined
        except:
            return self.undefined


    def writelstSubjectsPassedAndMarks (self, lstinput):

        try:
            lstinput = lstSubjectsMarks(lstinput)

            if ((len(lstinput.lstSubjectsAndMarks) > 0 ) and (lstinput.lstSubjectsAndMarks[0] <> self.undefined)):
                self.lstvarSubjectsMarks = lstinput
                return True
            else:
                self.lstvarSubjectsMarks = self.undefined
                return False
        except:
            self.lstvarSubjectsMarks = self.undefined
            return False


    def readstrNotes (self):

        try:

            temp = str(self.strNotes)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) >= self._minNotesLen) and (len(temp) <= self._maxNotesLen)):
                self.strNotes = temp
                return temp
            else:
                self.strNotes = self.undefined
                return self.undefined
        except:
            self.strNotes = self.undefined
            return self.undefined


    def writestrNotes (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if ((len(strinput) >= self._minNotesLen) and (len(strinput) <= self._maxNotesLen)):
                self.strNotes = strinput
                return True
            else:
                self.strNotes = self.undefined
                return False
        except:
            self.strNotes = self.undefined
            return False






























#######################################################################################################################
#################### EDUCATIONAL QUALIFICATIONS #######################################################################
#######################################################################################################################



class EducationalQualifications (db.Expando):

    clsHighSchoolQualifications = HighSchoolQualifications()
    clsTertiaryQualifications   = TertiaryQualifications()
    clsHighSchool               = HighSchool()
    clsTertiary                 = Tertiary()












