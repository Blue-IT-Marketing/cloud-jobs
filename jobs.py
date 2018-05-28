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
# JOBS CLASS
########################################################################################################################
#Administration Class it is used to insert the skills required for the system to work
#INITIALLY I CAN INPUT THIS SKILLS THROUGH THE SOURCE CODE AND THEN DEVELOP THIS CLASS FURTHER TO ALLOW ADMINISTRATORS
#TO ADD THE SKILLS LATER FROM THE SYSTEM ADMIN CONSOLE
#Class used to capture the educational qualifications required
#The Job class or entity should be stored on the datastore
from datatypes import Reference
from qualifications import RequiredEduQualifications
from skills import Skills
from companies import Company, CompanyReference
from google.appengine.ext import db
from google.appengine.api import users
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
import logging
import datetime
"""
public jobs = jobs that are available to anyone and even to search engines
private jobs = jobs that are posted to particular freelancing groups within freelancing solutions
sponsored jobs = jobs that are sponsored meaning they attract much more attention than jobs which are not sponsored
agent jobs= This jobs must be finished in a strict time scheduled and they are only able to be taken by freelancers with
enough ratings to take agent jobs (meaning freelancers that finish projects in time
premium jobs = Freelance jobs only available to premium freelancers or premium job seekers
"""





class JobKind(db.Expando, MyConstants, ErrorCodes):
    _lstJobKinds = ['public jobs', 'private jobs']
    jobkind = db.StringProperty(default='public jobs')

    def createAllJobKinds(self):
        try:

            i = 0
            key_list = []
            while i < len(self._lstJobKinds):
                findquery = db.Query(JobKind).filter('jobkind =', self._lstJobKinds[i])
                results = findquery.fetch(limit=1)
                if len(results) > 0:
                    result = results[0]
                    key_list.append(result.key())
                    i = i + 1
                else:
                    self.jobkind = self._lstJobKinds[i]
                    key_list.append(self.put())
                    i = i + 1

            return key_list
        except:
            return self._generalError




    def saveJobkind(self, clsinput):
        try:
            if clsinput.isValid():
                pkey = clsinput.put()
                self._jobkindsPkey = pkey #Making sure that pkeyvalue for jobkinds is set
                return pkey
            else:
                return self._JobKindInvalid
        except:
            return self._generalError

    # Retrieves Job Kind Using The Primary Key
    def retrieveJobKind(self):
        try:
            if not(self._jobkindsPkey == self.undefined):
                result = JobKind.get(self._jobkindsPkey)
                if result.readisValid():
                    return result
                else:
                    return self._pkeyNotSet
            else:
                return self._pkeyNotSet

        except:
            return self._generalError

    def findthisJobKinds(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._lstJobKinds:
                findquery = db.Query(JobKind).filter('jobkind = ', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobKindNotFound
            else:
                return self._JobKindNotFound
        except:
            return self._generalError


    def readjobkind(self):
        try:
            if self.jobkind in self._lstJobKinds:
                return self.jobkind
            else:
                return self._JobTypeInvalid
        except:
            return self._generalError

    def writejobkind(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._lstJobKinds:
                self.jobkind = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readisValid(self):
        try:
            if self.jobkind in self._lstJobKinds:
                return True
            else:
                return False
        except:
            return self._generalError



class JobTypes(db.Expando, MyConstants, ErrorCodes):
    _lstJobTypes = ['permanent', 'part-time', 'freelance jobs']
    jobtype = db.StringProperty(default='freelance jobs')

    def createAllJobTypes(self):
        try:
            i = 0
            while i < len(self._lstJobTypes):
                findquery = db.Query(JobTypes).filter('jobtype =', self._lstJobTypes[i])
                result = findquery.fetch(limit=1)
                if len(result) > 0:
                    i = i + 1
                else:
                    self.jobtype = self._lstJobTypes[i]
                    self.put()
                    i = i + 1
            return True
        except:
            return self._generalError



    def saveJobType(self, clsinput):
        try:

            if clsinput.isValid():
                pkey = clsinput.put()
                self._jobtypesPkey = pkey
                return pkey
            else:
                return self._JobTypeInvalid
        except:
            return self._generalError



    def retrieveJobType(self):

        try:

            if not(self._jobtypesPkey == self.undefined):
                result = JobTypes.get(self._jobtypesPkey)
                return result
            else:
                return self._JobTypeInvalid
        except:
            return self._generalError

    def findThisJobTypes(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._lstJobTypes:
                findquery = db.Query(JobTypes).filter('jobtype =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobTypesNotFound
            else:
                return self._JobTypesNotFound
        except:
            return self._generalError


    def readjobtype(self):
        try:
            if self.jobtype in self._lstJobTypes:
                return self.jobtype
            else:
                return self.undefined
        except:
            return self._generalError

    def writejobtype(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._lstJobTypes:
                self.jobtype = strinput
                return True
            else:
                self.jobtype = self.undefined
                return False
        except:
            return self._generalError

    def readisValid(self):
        try:
            if self.jobtype in self._lstJobTypes:
                return True
            else:
                return False
        except:
            return self._generalError



#TODO- Create a class to control renumeration of the jobs, or job budgets in case of freelance jobs
class JobBudgetOrSalary(db.Expando, MyConstants, ErrorCodes):
    MinBudget = db.StringProperty(default='0')
    MaxBudget = db.StringProperty(default='0')
    MinSalary = db.StringProperty(default='0')
    MaxSalary = db.StringProperty(default='0')

    def readisValid(self):
        try:
            if (((self.MinBudget == self.undefined) and (self.MaxBudget == self.undefined)) or ((self.MinSalary == self.undefined) and (self.MaxSalary == self.undefined))):
                return False
            else:
                return True
        except:
            return self._generalError



    def readminBudget(self):
        try:
            if not(self.minBudget == self.undefined) and (int(self.MinBudget) > 0):
                return self.MinBudget
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMinBudget(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isdigit()) and (int(strinput) > 0):
                self.MinBudget = strinput
                return True
            else:
                self.MinBudget = self.undefined
                return False
        except:
            return self._generalError

    def readMaxBudget(self):
        try:
            if not(self.MaxBudget == self.undefined) and (int(self.MaxBudget) > 0):
                return self.MaxBudget
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMaxBudget(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isdigit()) and (int(strinput) > 0):
                self.MaxBudget = strinput
                return True
            else:
                self.MaxBudget = self.undefined
                return False
        except:
            return self._generalError


    def readMinSalary(self):
        try:
            if not(self.MinSalary == self.undefined) and (int(self.MinSalary) > 0):
                return self.MinSalary
            else:
                return self.undefined
        except:
            return self._generalError


    def writeMinSalary(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined) and (int(strinput) > 0):
                self.MinSalary = strinput
                return True
            else:
                self.MinSalary = self.undefined
                return False
        except:
            return self._generalError

    def readMaxSalary(self):
        try:
            if not(self.MaxSalary == self.undefined) and (int(self.MaxSalary) > 0):
                return self.MaxSalary
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMaxSalary(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined) and (int(strinput) > 0):
                self.MaxSalary = strinput
                return True
            else:
                self.MaxSalary = self.undefined
                return True
        except:
            return self._generalError


class JobCosts():
  PublicJob = 2
  PrivateJob = 3
  GeneralJob = 3
  PremiumJob = 10
  UrgentJob = 8
  SponsoredJob = 5

class Job(db.Expando, MyConstants, ErrorCodes):

    # consider creating temporary variables to store the sub classes of jobs, bids company, person and wallet classes
    _jobowner = Reference()  # Use This temporary variables to read to and from the screen
    _jobtypes = JobTypes()
    _jobkind = JobKind()
    _jobbudgetsalary = JobBudgetOrSalary()
    _skillsrequired = Skills()
    _requirededuqualifications = RequiredEduQualifications()
    _companyowner = Company()
    _employercompany = Company()


    # initializaton values
    _minJobTitleLen = 2
    _maxJobTitleLen = 256
    _minJobDefinitionLen = 2
    _maxJobDefinitionLen = 16384
    _minDepartmentLen = 2
    _maxDepartmentLen = 256
    _minCompanyInstitutionLen = 2
    _maxCompanyInstitutionLen = 256
    _minDisplayDays = 1
    _maxDisplayDays = 30


    # The First Action of creating a job is write down the jobOwner Value
    # The JobOwner Key can be made compatible with the company owner field or both can be tested at the same time
    # 3. on Activate Bid Display Make Payment

    jobOwner = db.ReferenceProperty(Reference, collection_name='jobs_collection')  # The person who posted the job / One
    # Person can post many jobs

    # The Reference Number of the Job Owner
    strOwnerReference = db.StringProperty()

    # The Reference Number for this job
    strJobReference = db.StringProperty()

    strJobTitle = db.StringProperty()  # The title of the Job
    strJobDefinition = db.StringProperty(multiline=True)  # The definition of the job
    strNotes = db.StringProperty(multiline=True)  # Any Extra notes concerning the job The Company who submitted the job might indicate extra
    # info on the bidding process or the application process on the job market concerning this job

    _lstJobTypes = ['permanent', 'part-time', 'freelance jobs']
    strJobType = db.StringProperty(default='freelance jobs')

    _lstJobAttributes = ['sponsored jobs', 'urgent jobs', 'premium jobs', 'general jobs']
    strJobAttribute = db.StringProperty(default='general jobs')

    _lstJobKinds = ['public jobs', 'private jobs']
    strJobKind = db.StringProperty(default='public jobs')

    _lstFreelanceJobBudget = ['1030', '31100', '101300', '301600', '6012000', '200015000']
    strFreelanceJobBudget = db.StringProperty(default='1030')
    _clsJobCosts = JobCosts()

    strJobCost = db.StringProperty(default='0')  # The cost paid to post this job in credits
    # of skills required for this job
    strBiddingCredit = db.StringProperty(default='1')  # The Default number of credits to subtract for every bid
    _lstSkills = ['portuguese', 'englishus', 'englishuk', 'spanish', 'french', 'afrikaans', 'html', 'css3', 'xml', 'java', 'java script', 'php', 'python', 'perl', 'wordpress',
                           'joomla', 'csharp', 'gae', 'jinja2', 'django', 'cplusplus', 'c', 'visualbasic', 'net', 'pascal', 'freepascal',
                           'delphi', 'go', 'seo', 'article writing', 'proof reading', 'copy writing', 'website development', 'landing page development', 'android', 'webapp', 'jquery']
    StrSkillsRequired = db.StringListProperty(default='englishus')

    clsRequiredEduQualifications = db.ReferenceProperty(RequiredEduQualifications, collection_name='job_collection')  # The requiredEduQualifications class will link to many
    # Qualifications that are required for this job

    # Relationship type one Company many Jobs Placed

    clsCompanyOwner = db.ReferenceProperty(CompanyReference, collection_name='company_owner_jobs_collection') # Details of the
    # company tha posted this job.
    clsEmployerCompany = db.ReferenceProperty(CompanyReference, collection_name='company_Employer_jobs_collection')  # Details of
    # The Company Hiring or of the Employer Company (Note This company might not be the same as the company posting the
    # job)

    DateTimeSubmitted = db.DateTimeProperty(auto_now_add=True)  # The Date the job was submitted
    DateTimeModified = db.DateTimeProperty(auto_now=True)  # If Modified The Date The Job is modified

    DateTimeofBidDisplay = db.DateTimeProperty(auto_now_add=True)  # If Freelance Job the date the bid will start if normal jobs then the
    # date displaying will commence

    DateTimeEndBidorRemove = db.DateTimeProperty()  # The date the job will be removed from display or
    # the bidding process.

    BidsActivated =db.BooleanProperty(default=False)# In Order to activate Bids payment must be made
    BidActivationAmount = db.StringProperty(default='0')

    AwardedTo = db.StringProperty()  # Reference Number of the freelancer the job is awarded to:
    DateTimeAwarded = db.DateTimeProperty()  # The date and time the job was awarded.



    def readAwardedTo(self):
        try:
            temp = str(self.AwardedTo)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAwardedTo(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.AwardedTo = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readDateTimeAwarded(self):
        try:
            if not(self.DateTimeAwarded == self.undefined):
                return self.DateTimeAwarded
            else:
                return self.undefined
        except:
            return self._generalError

    def setDateTimeAwarded(self):
        try:

            Today = datetime.datetime.now()
            self.DateTimeAwarded = Today
            return True
        except:
            return False






    ## _lstFreelanceJobBudget = ['1030', '31100', '101300', '301600', '6012000', '200015000']
    def translateJobBudget(self):
        try:
            temp = str(self.strFreelanceJobBudget)
            temp = temp.strip()
            retlist = []
            if temp.isdigit():
                if temp == '1030':
                    retlist = ['10','30']
                    return retlist
                elif temp == '31100':
                    retlist = ['31', '100']
                    return retlist
                elif temp == '101300':
                    retlist = ['101', '300']
                    return retlist
                elif temp == '301600':
                    retlist = ['301', '600']
                    return retlist
                elif temp == '6012000':
                    retlist = ['601', '2000']
                    return retlist
                elif temp == '200015000':
                    retlist = ['2001', '5000']
                    return retlist
                else:
                    retlist = ['10', '30']
                    return retlist
            else:
                retlist = ['10', '30']
                return retlist
        except:
            return self._generalError

    def readPlaceBidCredit(self):
        try:
            return self.strBiddingCredit
        except:
            return self._generalError

    def calcJobCost(self, inJobKind, inJobAttribute):
        try:
            logging.info('JOB KINDS : ' + inJobKind)
            logging.info('JOB ATTRIBUTES : ' + inJobAttribute)

            if (inJobKind in self._lstJobKinds) and (inJobAttribute in self._lstJobAttributes):
                if inJobKind == self._lstJobKinds[0]: # Public Job
                    if inJobAttribute == self._lstJobAttributes[0]: # Sponsored Job
                        self.strJobCost = '7'
                        logging.info('7 FOR PUBLIC SPONSORED')
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[1]: # urgent jobs
                        self.strJobCost = '10'
                        logging.info('10 FOR URGENT PUBLIC')
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[2]: # premium jobs
                        self.strJobCost = '12'
                        logging.info('12 PREMIUM PUBLIC')
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[3]: # general jobs
                        self.strJobCost = '5'
                        return self.strJobCost
                else: # Private Job
                    if inJobAttribute == self._lstJobAttributes[0]:  # Sponsored Job
                        self.strJobCost = '8'
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[1]:  # urgent jobs
                        self.strJobCost = '11'
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[2]:  # premium jobs
                        self.strJobCost = '13'
                        return self.strJobCost
                    elif inJobAttribute == self._lstJobAttributes[3]:  # general jobs
                        self.strJobCost = '6'
                        return self.strJobCost
            else:
                self.strJobCost = '0'
                return self.strJobCost
        except:
            return self._generalError



    def readOwnerReference(self):
        try:

            temp = str(self.strOwnerReference)
            temp = temp.strip()

            if temp.isalnum() or temp.isalpha():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeOwnerReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalpha() or strinput.isalnum():
                self.strOwnerReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError



    def calcBidEnd(self): # Use This Function to calculate Bid End Date by Incrementing Days by 30
        pass





    def readJobCost(self):
        try:

            temp = str(self.strJobCost)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readBidsActivated(self):
        try:
            return self.BidsActivated
        except:
            return self._generalError

    def toggleBidsActivated(self):
        try:
            if self.BidsActivated:
                self.BidsActivated = False
                return True
            else:
                self.BidsActivated = True
                return True
        except:
            return self._generalError


    def readisValid(self):
        try:

            if (not(self.jobOwner == self.undefined) or not(self.clsCompanyOwner == self.undefined)) \
               and not(self.strJobTitle == self.undefined) and not(self.strJobDefinition == self.undefined) \
               and not(self.clsJobType == self.undefined) and not(self.strJobKind == self.undefined) \
               and not(self.strFreelanceJobBudget == self.undefined) and not(self.clsSkillsRequired == self.undefined):

                return True
            else:
                return False
        except:
            return self._generalError


    def readDateTimeSubmitted(self):
        try:
            return self.DateTimeSubmitted
        except:
            return self._generalError

    def readDateTimeModified(self):
        try:
            return self.DateTimeModified
        except:
            return self._generalError

    def readDateTimeOfBidsDisplay(self):
        try:
            return self.DateTimeofBidDisplay()
        except:
            return self._generalError
    # clsinput must already contain a valid DateTime Class
    def writeDateTimeOfBidsDisplay(self, clsinput):
        try:

            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                if (reference == self.jobOwner()) or (users.is_current_user_admin()): # Testing weather the
                # present loggedin User is the owner of the job or an admin
                    self.DateTimeofBidDisplay = clsinput
                    return True
                else:
                    return self._UserNotAuthorised

            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def readDateTimeEndBidorRemove(self):
        try:
            return self.DateTimeEndBidorRemove
        except:
            return self._generalError

    def writeDateTimeEndBidorRemove(self, clsinput):
        try:
            self.DateTimeEndBidorRemove = clsinput
        except:
            return self._generalError




    # This Function actually returns a Reference Key to the owner of the Job on the present class
    def readJobOwner(self):
        try:
            temp = str(self.jobOwner)
            temp = temp.strip()

            if temp.isalnum():
                logging.info('job owner was read. this instance : ' + temp)
                return temp
            else:
                return self.undefined
        except:
            logging.info('EXCEPTIONS OCCURED IN READ JOB OWNER')
            return self._generalError

    # This function writes down the Job owner Reference Key to the present key it only works for the
    # present loggedin user
    #Steps


    def writeJobOwner(self):


        try:

            Guser = users.get_current_user()
            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if (len(results) > 0):
                    temp = results[0]
                    self.jobOwner = temp.key()
                    logging.info('SUCCESSFULLY WROTE THE JOB OWNER')
                    return True
                else:
                    logging.info('FAILED TO WRITE THE JOB OWNER :' + self._clsReferenceDonotExist)
                    return self._clsReferenceDonotExist
            else:
                logging.info('WriteJobOwner :' + self._userNotLoggedin  )
                return self._userNotLoggedin
        except:
            return self._generalError

    # This Function retrieves the Job Owner class from the store Using the JobOwner Reference on the present class

    def retrieveJobOwner(self):
        try:
            Guser = users.get_current_user()

            if Guser:

                # Making sure the Jobowner does not refer to an empty class and also that the job owner is the present
                # logged in user
                if not(self.jobOwner == self.undefined):

                    findquery = db.Query(Reference).filter('strReferenceNum =', self.strOwnerReference)
                    results = findquery.fetch(limit=self._maxQResults)

                    if len(results) > 0:
                        temp = results[0]

                        if temp.readIsValid():
                            return temp
                        else:
                            return self._JobOwnerInvalid
                else:
                    return self._UserNotAuthorised
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    # This Function saves the JobOwner Class Information to the Datastore
    # The Owner of the Job is The Present Loggedin User and the key of such a user is normally stored on the _pkeyvalue
    # from the contants class
    # retrieve JobOwner and saveJobOwner allows the owner of the job to modify their own Reference class



#TODO FUNCTION IS IRRELEVANT
    def saveJobOwner(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if result.readIsValid():  # The Loggedin User Reference Class is valid

                        if self._jobowner.readIsValid() and ((self._jobowner.readJobOwner() == result.key()) or (users.is_current_user_admin())):

                            if self.jobOwner == self.undefined:
                                self.jobOwner = self._jobowner.put()
                                # This Stores the reference Class to the store and then saves the key
                                # to the jobOwner reference field
                                return True
                            else:
                                # Job Owner already exist
                                TJobOwner = Reference.get(self.jobOwner)
                                if TJobOwner.readIsValid():
                                    TJobOwner.writeDateTimeVerified(self._jobowner.readDatetimeVerified())
                                    TJobOwner.writeIDNumber(self._jobowner.readIDNumber())
                                    TJobOwner.writeIsUserVerified(self._jobowner.readIsUserVerified())
                                    TJobOwner.writeLogoPhoto(self._jobowner.readLogoPhoto())
                                    TJobOwner.writePassword(self._jobowner.readPassword())
                                    TJobOwner.writeReference(self._jobowner.readReference())
                                    TJobOwner.writeUsername(self._jobowner.readUsername())
                                    TJobOwner.writeVerEmail(self._jobowner.readVerEmail())

                                    self.jobOwner = TJobOwner.put()
                                    return True
                                else:
                                    return self._JobOwnerInvalid
                        else:
                            return self._JobOwnerInvalid
                    else:
                        return self._ReferenceInvalid
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



    def readstrJobTitle(self):
        try:
            temp = str(self.strJobTitle)
            temp = temp.strip()


            if (len(temp) >= self._minJobTitleLen) and (len(temp) <= self._maxJobTitleLen):
                self.strJobTitle = temp
                return temp.title()
            else:
                self.strJobTitle = self.undefined
                return self._JobTitleDoNotExist
        except:
            return self._generalError

    def writestrJobTitle(self, strinput):

        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if not(result.key() == self.undefined) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()
                        strinput = strinput.lower()

                        if ((len(strinput) >= self._minJobTitleLen) and (len(strinput) <= self._maxJobTitleLen)):
                            self.strJobTitle = strinput
                            return True
                        else:
                            self.strJobTitle = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist

            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def readJobDefinition(self):
        try:

            temp = str(self.strJobDefinition)
            temp = temp.strip()
            temp = temp.lower()

            if ((len(temp) <= self._maxJobDefinitionLen) and (len(temp) >= self._minJobDefinitionLen)):
                self.strJobDefinition = temp
                return temp
            else:
                self.strJobDefinition = self.undefined
                return self._JobDefinitionDoNotExist
        except:
            return self._generalError


    def writeJobDefinition(self, strinput):

        try:
            logging.info('THE JOB DEFINITION WE HAD :' + strinput)
            Guser = users.get_current_user()
            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'
                logging.info('PLEASE')
                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                logging.info(str(len(results)))
                if len(results) > 0:
                    result = results[0]


                    if not(result.key() == self.undefined) or (users.is_current_user_admin()):
                        logging.info('WE MADE IT NIGGER')

                        if ((len(strinput) <= self._maxJobDefinitionLen) and (len(strinput) >= self._minJobDefinitionLen)):
                            self.strJobDefinition = strinput
                            logging.info('WRITE JOB DEFINITION : ' + strinput)
                            return True
                        else:
                            self.strJobDefinition = self.undefined
                            return False
                    else:
                        logging.info(self._UserNotAuthorised)
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            logging.info('exception occurs')
            return self._generalError



    def readNotes(self):
        try:
            temp = str(self.strNotes)

            if not(temp == self.undefined):
                return temp
            else:
                return self._JobNotesDoNotExist
        except:
            return self._generalError


    def writeNotes(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (result.readIsValid()) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()
                        strinput = strinput.lower()

                        if not(strinput == self.undefined):
                            self.strNotes = strinput
                            return True
                        else:
                            self.strNotes = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def readJobKind(self):
        try:
            if self.strJobKind in self._lstJobKinds :
                return self.strJobKind
            else:
                return self._JobKindNotFound
        except:
            return self._generalError


    def writeJobKind(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or users.is_current_user_admin():
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput in self._lstJobKinds:
                            self.strJobKind = strinput
                            return True
                        else:
                            self.strJobKind = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin

        except:
            return self._generalError






    def readJobType(self):
        try:
            if self.strJobType in self._lstJobTypes:
                return self.strJobType
            else:
                return self._JobTypesNotFound
        except:
            return self._generalError


    def writeJobType(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput in self._lstJobTypes:
                            self.strJobType = strinput
                            return True
                        else:
                            self.strJobType = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



    def readFreelanceJobBudget(self):
        try:
            if self.strFreelanceJobBudget in self._lstFreelanceJobBudget:
                return self.strFreelanceJobBudget
            else:
                return self._JobBudgetSalaryDoNotExist
        except:
            return self._generalError


    def writeJobBudgetSalary(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput in self._lstFreelanceJobBudget:
                            self.strFreelanceJobBudget = strinput
                            return True
                        else:
                            self.strFreelanceJobBudget = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



    def readSkillsRequired(self):
        try:
            if len(self.StrSkillsRequired) > 0:
                i = 0
                tSkillList = []
                while i < len(self.StrSkillsRequired):
                    tSkill = self.StrSkillsRequired[i]
                    if tSkill == 'englishus':
                        tSkillList.append('English US')
                    elif tSkill == 'englishuk':
                        tSkillList.append('English UK')
                    elif tSkill == 'css3':
                        tSkillList.append('CSS3')
                    elif tSkill == 'html':
                        tSkillList.append('HTML')
                    elif tSkill == 'xml':
                        tSkillList.append('XML')
                    elif tSkill == 'php':
                        tSkillList.append('PHP')
                    elif tSkill == 'cplusplus':
                        tSkillList.append('C++')
                    elif tSkill == 'gae':
                        tSkillList.append('GAE')
                    elif tSkill == 'visualbasic':
                        tSkillList.append('Visual Basic')
                    elif tSkill == 'freepascal':
                        tSkillList.append('Free Pascal')
                    elif tSkill == 'seo':
                        tSkillList.append('SEO')
                    elif tSkill == 'webapp':
                        tSkillList.append('WebApp')
                    elif tSkill == 'jquery':
                        tSkillList.append('JQuery')
                    else:
                        tSkillList.append(tSkill.title())
                    i = i + 1
                return tSkillList
            else:
                return self._RequiredSkillsDoNotExist
        except:
            return self._generalError


    def writeSkillRequired(self, strinput):
        try:

            if strinput in self._lstSkills:
                self.StrSkillsRequired = strinput
                return True
            else:
                self.StrSkillsRequired = self._lstSkills[1] # Default Skill
                return False
        except:
            return self._generalError



    def readRequiredEduQualifications(self):
        try:
            if not(self.clsRequiredEduQualifications == self.undefined):
                return self.clsRequiredEduQualifications()
            else:
                return self._RequiredQualificationsDoNotExist
        except:
            return self._generalError


    def writeRequiredEduQualifications(self, strinput):
        try:

            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]


                    if (reference == self.strOwnerReference) or users.is_current_user_admin():
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput.isalnum():
                            self.clsRequiredEduQualifications = strinput
                            return True
                        else:
                            self.clsRequiredEduQualifications = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def retrieveRequiredEduQualifications(self):
        try:

            if not(self.clsRequiredEduQualifications == self.undefined):
                temp = RequiredEduQualifications.get(self.clsRequiredEduQualifications())
                if temp.readIsValid():
                    return temp
                else:
                    return self._RequiredQualificationsInvalid
            else:
                return self._RequiredQualificationsDoNotExist
        except:
            return self._generalError


    def saveRequiredEduQualifications(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        if self._requirededuqualifications.readisValid():
                            if self.clsRequiredEduQualifications == self.undefined:
                                self.clsRequiredEduQualifications = self._requirededuqualifications.put()
                                return True
                            else:
                                REdu = RequiredEduQualifications.get(self.clsRequiredEduQualifications())
                                if REdu.readIsValid():
                                    REdu.writeisCompulsory(self._requirededuqualifications.readisCompulsory())
                                    REdu.writeQualification(self._requirededuqualifications.readQualification())

                                    # TODO -- Finish up Required Edu Qualifications and also finish up here
                                    return True
                                else:
                                    return self._RequiredQualificationsInvalid
                        else:
                            return self._RequiredQualificationsInvalid

                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def readCompanyOwner(self):
        try:
            if not(self.clsCompanyOwner == self.undefined):
                return self.clsCompanyOwner()
            else:
                return self._OwnerCompanyInvalid
        except:
            return self._generalError

# This Procedures must be fixed we need to have a clear understanding of who can aquere ownership or change owner of company jobs
    def writeCompanyOwner(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'

                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput.isalnum():
                            self.clsCompanyOwner = strinput
                            return True
                        else:
                            self.clsCompanyOwner = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def retrieveCompanyOwner(self):
        try:
            if not(self.clsCompanyOwner == self.undefined):
                temp = Company.get(self.clsCompanyOwner())
                if temp.readisValid():
                    return temp
                else:
                    return self._OwnerCompanyInvalid
            else:
                return self._OwnerCompanyInvalid
        except:
            return self._generalError

    # The Present Loggedin User will always be the JobOwner no matter if the user is a company owner

    def saveCompanyOwner(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (result.key() == self.strOwnerReference) or (users.is_current_user_admin()):
                        if self._companyowner.readisValid():
                            if self.clsCompanyOwner == self.undefined:
                                self.clsCompanyOwner = self._companyowner.put()
                                return True
                            else:
                                # There's a previous company owner
                                OCompany = Company.get(self.clsCompanyOwner)
                                if OCompany.readisValid():
                                    OCompany.writePhysicalAddress(self._companyowner.readPhysicalAddress())
                                    OCompany.writeDepartmentName(self._companyowner.readDepartmentName())
                                    OCompany.writeContactPersonPrivateInf(self._companyowner.readContactPersonPrivateInfo())
                                    OCompany.writeContactPersonNames(self._companyowner.readContactPersonNames())
                                    OCompany.writeAccountDetails(self._companyowner.readAccountDetails())
                                    OCompany.writeBranchName(self._companyowner.readBranchName())
                                    OCompany.writeCompanyContacts(self._companyowner.readCompanyContacts())
                                    OCompany.writeCompanyName(self._companyowner.readCompanyName())

                                    self.clsCompanyOwner = OCompany.put()

                                    return True
                                else:
                                    return self._OwnerCompanyInvalid

                        else:
                            return self._OwnerCompanyInvalid
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def readEmployerCompany(self):
        try:
            if not(self.clsEmployerCompany == self.undefined):
                return self.clsEmployerCompany()
            else:
                return self._EmployerCompanyInvalid
        except:
            return self._generalError



# THE EMPLOYER COMPANY VALUE MUST BE THE REFERENCE FIELD OF THE REFERENCE CLASS FOR THE COMPANY
    def writeEmployerCompany(self, strinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        strinput = str(strinput)
                        strinput = strinput.strip()

                        if strinput.isalnum() or strinput.isalpha():
                            self.clsEmployerCompany = strinput
                            return True
                        else:
                            self.clsEmployerCompany = self.undefined
                            return False
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



    def retrieveEmployerCompany(self):
        try:
            if not(self.clsCompanyOwner == self.undefined):
                temp = Company.get(self.clsCompanyOwner())
                findquery = db.Query(CompanyReference).filter('strReference =', self.readEmployerCompany())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    temp = results[0]
                    if temp.readisValid():
                        return temp
                    else:
                        return self._OwnerCompanyInvalid
            else:
                return self._OwnerCompanyInvalid
        except:
            return self._generalError


    # Employer Company must already be created or a new company will be created
    # The Owner class must be pre existing
    # The Employer Compnay Details must already be stored on _employercompany Details field
    #This function cannot create a new employer company


#Questionable function
    def saveEmployerCompany(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = 'abc05529818'


                findquery = db.Query(Reference).filter('strReferenceNum =', reference)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if (reference == self.strOwnerReference) or (users.is_current_user_admin()):
                        if self._employercompany.readisValid():
                            if (self.clsEmployerCompany == self.undefined):
                                self.clsEmployerCompany = self._employercompany.put()
                                return True
                            else:
                                # There's a pre existing employer company
                                PEmployer = Company.get(self.clsEmployerCompany)
                                if PEmployer.readisValid():
                                    PEmployer.writeAccountDetails(self._employercompany.readAccountDetails())
                                    PEmployer.writeBranchName(self._employercompany.readBranchName())
                                    PEmployer.writeCompanyContacts(self._employercompany.readCompanyContacts())
                                    PEmployer.writeCompanyName(self._employercompany.readCompanyName())
                                    PEmployer.writeContactPersonNames(self._employercompany.readContactPersonNames())
                                    PEmployer.writeContactPersonPrivateInf(self._employercompany.readContactPersonPrivateInfo())
                                    PEmployer.writeDepartmentName(self._employercompany.readDepartmentName())
                                    PEmployer.writePhysicalAddress(self._employercompany.readPhysicalAddress())

                                    self.clsEmployerCompany = PEmployer.put()
                                    return True
                                else:
                                    return self._EmployerCompanyInvalid
                        else:
                            return self._EmployerCompanyInvalid
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError



