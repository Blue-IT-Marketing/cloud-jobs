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
##################################### FREELANCE JOBS ###################################################################
########################################################################################################################

import os
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
from jobs import Job
from jobs import JobTypes
from jobs import JobKind
from jobs import JobBudgetOrSalary
from bids import Bids
from companies import Company
from skills import Skills
from datatypes import Reference
from accounts import Wallet
from qualifications import RequiredEduQualifications
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from ConstantsAndErrorCodes import MyConstants, ErrorCodes
import logging


#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

# Control Class for freelance jobs this class is used to save and read freelance jobs from the store
# and also to organize the freelance jobs section of the website
# also to enable the search functions necessary for the freelance jobs section of the website
# Control functions such as The Bidding Process will also be controlled in this class
# Control functions such as the milestone payments will also be controlled in this class
# must be able to track who is working on which freelance job
# must enable communication between freelance friends, freelancer and employer.

#TODO- CREATE AN ABILITY TO CREATE FREELANCE JOBS WITHIN THIS CLASS
#TODO- CREATE A FUNCTION TO CREATE BIDS WITHIN THIS CLASS
#TODO- CREATE SEARCH FUNCTIONS FOR BIDS, AND WALLET WITHIN THIS CLASS



#TODO-NEED TO CREATE A FREELANCER CLASS TO TAKE CARE OF THE FUNCTIONALITY RELATED TO FREELANCERS
#THE FREELANCEJOBS CLASS IS RELATED TO A FREELANCE JOB NOT A FREELANCER.
class FreelanceJobs(db.Expando, MyConstants, ErrorCodes):

    clsJob = Job()  # Class to read and store freelance jobs to the data store and also to perform related tasks on the
    # Job
    clsBid = Bids()  # Class to read and store freelance jobs Bids to the data store
    # The Person Class will be accessed using the DataType module
    clsWallet = Wallet()  # Class to read and store Account Information for freelancers
    # All the temporary variables must be holding the correct values
    # All The variables within clsjob must be holding correct values also

    def createFreelanceJob(self):
        pass


    def readJob(self):
        try:
            if self.clsJob.isValid():
                return self.clsJob
            else:
                return self._JobIsInvalid
        except:
            return self._generalError

    #write job will write all the temporary values back to datastore

    #TODO - CREATE FUNCTIONS TO ACCEPT INPUT FOR SUB CLASSES SUCH AS OWNER COMPANIES AND OWNER FREELANCERS
    #TODO-  FOR JOBS THE FUNC
    #TODO- WILL BE CALLED BY WRITE JOB IN ORDER TO COMPLETE THE OVERALL OPERATION FOR WRITING A JOB
    #TODO- NOTE THAT THE SUBFUNCTIONS TO WRITE DATA WITHIN A SUBCLASS ARE CONTAINED WITHIN SUCH A SUB CLASS
    def writeJob(self, clsinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if (Guser.user_id() == clsinput.jobOwner()) or (users.is_current_user_admin()):
                    if clsinput.isValid():
                        self.clsJob.writeJobOwner(clsinput.readJobOwner())
                        self.clsJob.writeEmployerCompany(clsinput.readEmployerCompany())
                        self.clsJob.writeCompanyOwner(clsinput.readCompanyOwner())
                        self.clsJob.writeDateTimeEndBidorRemove(clsinput.readDateTimeEndBidorRemove())
                        self.clsJob.writeDateTimeOfBidsDisplay(clsinput.readDateTimeOfBidsDisplay())
                        self.clsJob.writeJobBudgetSalary(clsinput.readJobBudgetSalary())
                        self.clsJob.writeJobDefinition(clsinput.readJobDefinition())
                        self.clsJob.writeJobKind(clsinput.readJobKind())
                        self.clsJob.writeJobType(clsinput.readJobType())
                        self.clsJob.writeNotes(clsinput.readNotes())
                        self.clsJob.writeRequiredEduQualifications(clsinput.readRequiredEduQualifications())
                        self.clsJob.writeSkillRequired(clsinput.readSkillsRequired())
                        self.clsJob.writestrJobTitle(clsinput.readstrJobTitle())
                        if not(self.clsJob.readBidsActivated() == self._generalError):
                            self.clsjob.BidsActivated = clsinput.readBidsActivated()
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return self._UserNotAuthorised
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def saveJob(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                if (Guser.user_id() == self.clsJob.strOwnerReference) or (users.is_current_user_admin()):
                    if self.clsJob.isValid():
                        self.clsJob._jobPkey = self.clsJob.put()
                        return self.clsJob._jobPkey
                    else:
                        return self.undefined
                else:
                    return self._UserNotAuthorised
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    def retrieveJobByPkey(self):
        try:
            if not(self.clsJob._jobPkey == self.undefined):
                temp = Job.get(self.clsJob._jobPkey)
                if temp.isValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    def retrieveJobsByJobOwner(self, strinput):
        try:

            if strinput.isalnum():
                findquery = db.Query(Job).filter('strOwnerReference = ', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    logging.info('FOUND JOBS')
                    return results

                else:
                    logging.info('FOUND JOBS')
                    return self._JobsNotFound
            else:
                logging.info('NOT FOUND JOBS')
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsByCompanyOwner(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalnum():
                findquery = db.Query(Job).filter('clsCompanyOwner =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsByEmployerCompany(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalnum():

                findquery = db.Query(Job).filter('clsEmployerCompany =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsByJobTitle(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if strinput.isalnum() or strinput.isalpha():
                findquery = db.Query(Job).filter('strJobTitle =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self.undefined
        except:
            return self._generalError


    def retrieveJobsByJobType(self, strinput):

        try:
            logging.info('RETIRVE FREELANCE JOBS CALLED')
            strinput = str(strinput)
            strinput = strinput.strip()
            if strinput in self.clsJob._lstJobTypes:
                findquery = db.Query(Job).filter('strJobType =', strinput).order('-BidsActivated').order('-DateTimeSubmitted')
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError


    def retrieveJobsByJobKind(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput in self.clsJob._lstJobKinds:
                findquery = db.Query(Job).filter('strJobKind =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsByJobBudget(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput in self.clsJob._lstFreelanceJobBudget:
                findquery = db.Query(Job).filter('strFreelanceJobBudget =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsBySkillsPkey(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalnum():
                findquery = db.Query(Job).filter('clsSkillsRequired =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError

    def retrieveJobsByEduQualificationsPkey(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalnum():
                findquery = db.Query(Job).filter('clsRequiredEduQualifications =', strinput)
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._pkeyNotSet
        except:
            return self._generalError



    def getJobByBid(self):
        pass


        # Given The reference Number of the freelance job search for all the jobs and return only those jobs which are
    # freelance jobs and owned by a certain user

    def GetFreelanceJobsByReference(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalpha() or strinput.isalnum():
                findrequest = db.Query(Job).filter('strOwnerReference =', strinput)
                findrequest = findrequest.filter('strJobType =', self.clsJob._lstJobTypes[2]).order('DateTimeSubmitted')
                results = findrequest.fetch(limit=self._maxQResults)
                logging.info('NUMBER OF PERSONAL JOBS RETURNED :' + str(len(results)))
                if len(results) > 0: # All the jobs are returned
                    # find freelance jobs from the list and return only freelance jobs
                    return results
                else:
                    return self._JobsNotFound
            else:
                return self._referenceDoNotExist
        except:
            return self._generalError



class submitJobsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        template = template_env.get_template('templates/submit-jobs.html')
        context = {}
        self.response.write(template.render(context))



app = webapp2.WSGIApplication([('/employer-submitjobs', submitJobsHandler)
                               ], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()