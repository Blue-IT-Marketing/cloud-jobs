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


# A Company can also function as a normal user with login credentials and an ability to post jobs as a freelancer,
# and also on the job market


from datatypes import Reference, Person, PhysicalAddress, Private_info, ContactDetails, Names
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
# Procedure to save the company class
# first save the collections starting by the Reference Collection , Names Collection, Contact Details, then Physical
# Address Collection then lastly save The Company class with all the ReferenceProperty and other details
# The company class will be controlled by the FreelanceJob, JobMarket, Affiliates, or The Market Place Class
'''
New Desing

Company Reference (Reference for Company
Company Names
Company Contact Person (Reference Class)
Company Contact Details
Company Physical Details



NOTE THE COMPANY
'''


class CompanyReference(db.Expando):

    strReference = db.StringProperty()  # Store The Primary Key in turn it will be used to link every related class
    strUserName = db.StringProperty()
    strPassword = db.StringProperty()
    isCompanyVerified = False
    strCompanyVerEmail = db.EmailProperty()
    CompanyLogo = db.BlobProperty()


    def readReference(self):
        try:
            if not(self.strReference == self.undefined):
                return self.strReference
            else:
                return self.undefined
        except:
            return self.undefined

    def writeReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined) and (strinput.isalpha() or strinput.isalnum()):
                self.strReference = strinput
                return True
            else:
                self.strReference = self.undefined
                return False
        except:
            return False


    def readUserName(self):
        try:
            if not(self.strUserName == self.undefined):
                return self.strUserName
            else:
                return self.undefined
        except:
            return self.undefined


    def writeUserName(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined) and (strinput.isalpha() or strinput.isalnum()):
                self.strUserName = strinput
                return True
            else:
                self.strUserName = self.undefined
                return False
        except:
            return False



    def readPassword(self):
        try:

            if not(self.strPassword == self.undefined):
                return self.strPassword
            else:
                return self.undefined
        except:
            return self.undefined


class CompanyNames(db.Expando):
    indexReference = db.ReferenceProperty(CompanyReference, collection_name='company_names')
    strCompanyName = db.StringProperty()
    strCompanyDescription = db.StringProperty(multiline=True)
    strBranchName = db.StringProperty()
    strBranchDescription = db.StringProperty(multiline=True)
    strNotes = db.StringProperty(multiline=True)


#This class is the link between the person class and the company class thereby linking people with companies


class CompanyContactPerson(db.Expando):
    pindexReference = db.ReferenceProperty(Reference, collection_name='company_contact_person')
    cIndexReference = db.ReferenceProperty(CompanyReference, collection_name='company_contact_person')


class CompanyContactDetails(db.Expando):
    indexReference = db.ReferenceProperty(CompanyReference, collection_name='company_contact_details')



class CompanyPhysicalAddress(db.Expando):
    indexReference = db.ReferenceProperty(CompanyReference, collection_name='company_physical_address')



#Use The company Class exactly like the person class


class Company(db.Expando):

    _minCompanyNameLen = 2
    _maxCompanyNameLen = 256
    _minDepartmentNameLen = 2
    _maxDepartmentNameLen = 256
    _minBranchNameLen = 2
    _maxBranchNameLen = 256


    #System Constants

    _maxQResults = 50
    _UserNameDonotExist = 10001
    _generalError = 10002
    _ReferenceDonotExist = 10003


    #Temporary variables to hold each instance present values
    _account_details = Reference()
    _company_contacts = ContactDetails()
    _physical_address = PhysicalAddress()
    _contact_person_names = Names()
    _contact_person_private_inf = Private_info
    # include the preferences class here



    account_details = db.ReferenceProperty(Reference, collection_name='company_collection')  # Reference Class for login details of the company
    company_name = db.StringProperty()
    company_contacts = db.ReferenceProperty(ContactDetails, collection_name='company_collection')
    physical_address = db.ReferenceProperty(PhysicalAddress, collection_name='company_collection') #  The Physical Address used for Company must be linked to the relevant
    # Reference Class
    department_name = db.StringProperty()
    branch_name = db.StringProperty()  # The Name of the branch the specified company address is for.
    contact_person_names = db.ReferenceProperty(Names, collection_name='company_collection')  # This Class contains the names of the person who is a contact person for this company
    #This names class should also be linked to the Reference Class for Company Login
    contact_person_private_inf = db.ReferenceProperty(Private_info, collection_name='company_collection')
    isValid = False

    #This function returns the reference for the Reference Class the calling function should then create a temporary
    #Reference Class to be able to read the actual Reference Class Details.

    def returnAccoutDetailsByUsername(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            temp = Reference()

            if temp.writeUsername(strinput):
                findquery = db.Query(Reference).filter('strUsername =', strinput)
                results = findquery.fetch(self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    if temp.isValid():
                        return temp
                    else:
                        return self.undefined
                else:
                    return self._UserNameDonotExist
            else:
                return self._UserNameDonotExist
        except:
            return self._generalError

    def returnAccountDetailsByReference(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            temp = Reference()

            if temp.writeReference(strinput):
                findquery = db.Query(Reference).filter('strReferenceNum =', strinput)
                results = findquery.fetch(self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    if temp.isValid():
                        return temp
                    else:
                        return self.undefined
                else:
                    return self._ReferenceDonotExist
            else:
                return self._ReferenceDonotExist
        except:
            return self._generalError





    def readAccountDetails(self):
        try:
            if not(self.account_details == self.undefined):
                return self.account_details
            else:
                return self.undefined
        except:
            return self.undefined

    # This class actually writes the referenceproperty to the Reference Class teh actuall Reference Class must have been
    # already written using a temporary Reference Class variable
    def writeAccountDetails(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined):
                self.account_details = strinput
                return True
            else:
                self.account_details = self.undefined
                return False
        except:
            return False

    def readCompanyName(self):
        try:
            if not(self.company_name == self.undefined):
                return self.company_name
            else:
                return self.undefined
        except:
            return self.undefined

    def writeCompanyName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isalnum() or strinput.isalpha()) and (len(strinput) <= self._minCompanyNameLen) and (len(strinput) >= self._maxCompanyNameLen):
                self.company_name = strinput
                return True
            else:
                self.company_name = self.undefined
                return False
        except:
            return False

    def readCompanyContacts(self):
        try:
            if not(self.company_contacts == self.undefined):
                return self.company_contacts()
            else:
                return self.undefined
        except:
            return self.undefined

    def writeCompanyContacts(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined):
                self.company_contacts = strinput
                return True
            else:
                self.company_contacts = self.undefined
                return False
        except:
            return False

    def readPhysicalAddress(self):
        try:

            if not(self.physical_address == self.undefined):
                return self.physical_address()
            else:
                return self.undefined
        except:
            return self.undefined

    def writePhysicalAddress(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.physical_address = strinput
                return True
            else:
                self.physical_address = self.undefined
                return False
        except:
            return False

    def readDepartmentName(self):
        try:
            if not(self.department_name == self.undefined):
                return self.department_name
            else:
                return self.undefined
        except:
            return self.undefined

    def writeDepartmentName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isalnum() or strinput.isalpha()) and (len(strinput) <= self._minDepartmentNameLen) and (len(strinput) >= self._maxDepartmentNameLen):
                self.department_name = strinput
                return True
            else:
                self.department_name = self.undefined
                return False
        except:
            return False

    def readBranchName(self):
        try:
            if not(self.branch_name == self.undefined):
                return self.branch_name
            else:
                return self.undefined
        except:
            return self.undefined

    def writeBranchName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isalnum() or strinput.isalpha()) and (len(strinput) <= self._minBranchNameLen) and (len(strinput) >= self._maxBranchNameLen):
                self.branch_name = strinput
                return True
            else:
                self.branch_name = self.undefined
                return False
        except:
            return False

    def readContactPersonNames(self):
        try:
            if not(self.contact_person_names == self.undefined):
                return self.contact_person_names()
            else:
                return self.undefined
        except:
            return self.undefined

    def writeContactPersonNames(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.contact_person_names = strinput
                return True
            else:
                self.contact_person_names = self.undefined
                return False
        except:
            return False

    def readContactPersonPrivateInfo(self):
        try:
            if not(self.contact_person_private_inf == self.undefined):
                return self.contact_person_private_inf
            else:
                return self.undefined
        except:
            return self.undefined


    def writeContactPersonPrivateInf(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self._contact_person_private_inf = strinput
                return True
            else:
                self._contact_person_private_inf = self.undefined
                return False
        except:
            return False


    def retrieveAccountDetails(self):
        try:
            temp = Reference()  # Temporary field to store Account Details
            if not(self.account_details == self.undefined):
                temp = Reference.get(self.account_details)
                if temp.isValid:
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self.undefined


    def retrieveCompanyContacts(self):
        try:
            temp = ContactDetails()
            if not(self.company_contacts == self.undefined):
                temp = ContactDetails.get(self.company_contacts)
                if temp.isValid:
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self.undefined

    def retrievePhysicalAddress(self):
        try:
            temp = PhysicalAddress()
            if not(self.physical_address == self.undefined):
                temp = PhysicalAddress.get(self.physical_address)
                if temp.isValid:
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self.undefined


    def retrieveContactPersonNames(self):
        try:
            temp = Names()
            if not(self.contact_person_names == self.undefined):
                temp = Names.get(self.contact_person_names)
                if temp.isValid:
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self.undefined

    def retrieveContactPersonPrivateinf(self):
        try:
            temp = Private_info()
            if not(self._contact_person_private_inf == self.undefined):
                temp = Private_info.get(self._contact_person_private_inf())
                if temp.isValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self.undefined


    def setIsValid(self):
        pass
    def readisValid(self):
        try:
            if self.setIsValid():
                return True
            else:
                return False
        except:
            return False