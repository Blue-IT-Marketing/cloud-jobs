
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
########################################################################################################################
############################### FREELANCE JOBS BIDDING CLASSES #########################################################
########################################################################################################################
########################################################################################################################
from datatypes import Reference
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from datatypes import Reference
from jobs import Job
from companies import Company
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache




class Bids(db.Expando, MyConstants, ErrorCodes):
    _minBidNotes = 20
    _maxBidNotes = 1025

    BidNotes = db.StringProperty(multiline=True)
    BidAmount = db.StringProperty(default='0')  # Amount for the Bid in Money never to exceed The Maximum Budget can only be checked on the
    #Freelance Job Class as it has access to the interface and all the other classes
    CurrencySymbol = db.StringProperty(default='$')  # Currency for the Amount Above
    # The Currency Will Depend on the User Preferences and could be set automatically if possible
    #todo-The util module must include currency symbols for each country and timezone info
    # many bids Single Reference
    pBidder = db.StringProperty()
    cBidder = db.StringProperty()
    # Single Bid Single Job or/// Single Job One Bid
    BidonThisJob = db.StringProperty()
    BidReference = db.StringProperty()
    # Have to enforce a one to one relationship using Code between when accessing BidonThisJob
    MilestonePayment = db.StringProperty(default='0')  # Milestone amount to be paid for this freelance job
    MilestoneMarker = db.StringProperty(default='0')  # in terms of percentage define the milestone when the above amount will be paid
    MilestoneNotes = db.StringProperty(multiline=True, default='Explain in words your milestone requirements')
    BidSponsorCredit = db.StringProperty(default='0') # The Credit Amount that the freelance job has been sponsored
    isValid = db.BooleanProperty(default=False)
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    DateModified = db.DateTimeProperty(auto_now=True)


    BidPoints = db.StringProperty(default='0')  # Calculated Points for each bid calculated just before a bid is saved
    ShowBid = db.BooleanProperty(default=False)
    #Get Teh Settings for currency from preferences

    def readBidReference(self):
        try:
            temp = str(self.BidReference)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readMileStoneNotes(self):
        try:
            temp = str(self.MilestoneNotes)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readBidPoints(self):
        try:
            temp = str(self.BidPoints)
            temp = temp.strip()
            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readisValid(self):
        try:
            if self.setIsValid():
                return self.isValid
            else:
                return self.undefined
        except:
            return self._generalError


    def setIsValid(self):
        try:
            if not(self.BidNotes == self.undefined) and not(self.BidAmount == self.undefined) and (not(self.pBidder == self.undefined) or not(self.cBidder == self.undefined)) and not(self.BidonThisJob == self.undefined) and not(self.MilestonePayment == self.undefined) and not(self.MilestoneMarker == self.undefined):
                self.isValid = True
                return True
            else:
                self.isValid = False
                return True
        except:
            return False

    #TODO--- Define all teh currency within the utilities function in relation to the country, use the country currency as a default
    #TODO-- IN the preferences module create a function to associate a currency with a user
    def setCurrency(self):
        return False

    def createBid(self, inBidAmount, inBidNotes, inBidOnThisJob, inMilestone, inMilestoneMarker, inSponsorCredit):
        try:
            Guser = users.get_current_user()

            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode


                findrequest = db.Query(Job).filter('strJobReference =', inBidOnThisJob)
                results = findrequest.fetch(limit=1)
                if len(results) > 0:
                    tjob = results[0]
                    logging.info('FREELANCE JOB REFERENCE FOUND :' + inBidOnThisJob)

                    findrequest = db.Query(Reference).filter('strReferenceNum =', reference)
                    results = findrequest.fetch(limit=1)

                    if len(results) > 0:
                        UReference = results[0]
                    else:
                        UReference = Reference()
                    logging.info('UREFERENCE KEY:' + str(UReference.key()))

                    if not(reference == tjob.strOwnerReference) or (reference == self._tempCode):

                        logging.info('IN BID AMOUNT :' + inBidAmount)
                        self._bidJobPkey = inBidOnThisJob # this helps the active bids sub to show the relevant bids
                        findrequest = db.Query(Bids).filter('BidonThisJob =', inBidOnThisJob).filter('pBidder =', reference)
                        results = findrequest.fetch(limit=self._maxQResults)
                        if len(results) == 0:
                            if self.writeBidAmount(inBidAmount) and self.writeBidOnThisJob(inBidOnThisJob):
                                self.writeBidNotes(inBidNotes)
                                self.writeMilestonePayment(inMilestone)
                                self.writeMilestoneMarker(inMilestoneMarker)
                                self.writeSponsorCredit(inSponsorCredit)
                                self.writePBidder(reference)
                                logging.info('WRITE BID AMOUNT AND OTHERS SUCCEEDED')
                                self.CurrencySymbol = self._defaultCurrency
                                self._bidPkey = self.put()
                                self.BidReference = str(self._bidPkey)
                                self.put()
                                return True

                            else:
                                logging.info('FAILURE CREATING BID ++++')
                                return self._ErrorCreatingBid
                        else:
                            logging.info('BID ALREADY PLACE')
                            return results
                    else:
                        logging.info('YOU ARE THE JOB OWNER BITCH')
                        return self._CannotBidOnOwnJob
            else:
                return self._userNotLoggedin
        except:
            logging.info('EXCEPTIONS ARE BEING THROWN ON CREATING BIDS')
            return self._generalError

    def getMyBid(self):
        try:

            Guser = users.get_current_user()

            if Guser:


                findquery = db.Query(Reference).filter('strReferenceNum =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    findquery = db.Query(Bids).filter('pBidder =', result.key())
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        result = results[0]
                        return result
                    else:
                        return self._BidderNotFound
                else:
                    return self._referenceDoNotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    def GetAllMyBids(self):
        try:
            Guser = users.get_current_user()

            if Guser:


                findquery = db.Query(Reference).filter('strReferenceNum =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    findquery = db.Query(Bids).filter('pBidder =', result.key())
                    results = findquery.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        return results # Returning all teh Bids for this User
                    else:
                        return self._BidderNotFound
                else:
                    return self._referenceDoNotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError


    # The owner of the bid can remove a bid
    # The Owner of the Job can remove a bid
    # The Admin can remove a bid
    def removeBid(self, strinput):
        try:

            Guser = users.get_current_user()

            if Guser:
                BidtoRemove = Bids.get(strinput)
                BidJob = Job.get(BidtoRemove.BidonThisJob)
                if (Guser.user_id() == BidtoRemove.pBidder) or (BidJob.jobOwner() == Guser.user_id()) or (users.is_current_user_admin()):
                    BidtoRemove.delete()
                    return True
                else:
                    return False
            else:
                return self._userNotLoggedin
        except:
            return self._generalError





    def readBidNotes(self):
        try:

            if not(self.BidNotes == self.undefined):
                return self.BidNotes
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBidNotes(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if ((len(strinput) >= self._minBidNotes) and (len(strinput) <= self._maxBidNotes)):
                logging.info('WRITE BID NOTES SUCCEEDED')
                self.BidNotes = strinput
                return True
            else:
                logging.info('WRITE BID NOTES FAILED')
                return False
        except:
            return self._generalError

    def writeSponsorCredit(self, inSponsor ):

        try:
            inSponsor = str(inSponsor)
            inSponsor = inSponsor.strip()

            if inSponsor.isdigit():
                logging.info('WRITE SPONSOR CREDIT SUCCEEDED:')
                self.BidSponsorCredit = inSponsor
                return True
            else:
                logging.info('WRITE SPONSOR CREDIT FAILED:')
                return False
        except:
            return self._generalError

    def readSponsorCredit(self):

        try:
            temp = str(self.BidSponsorCredit)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def readBidAmount(self):
        try:
            temp = str(self.BidAmount)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBidAmount(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if strinput.isdigit():
                logging.info('WRITE BID AMOUNT SUCCEEDED')
                self.BidAmount = strinput
                return True
            else:
                logging.info('WRITE BID AMOUNT FAILED')
                return False
        except:
            return self._generalError

    def readPBidder(self):

        try:
            temp = str(self.pBidder)
            temp = temp.strip()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePBidder(self, strinput):
        try:
            if len(strinput) > 0:
                logging.info('THIS TELLS NEWS')
                self.pBidder = strinput
                logging.info('WRITE PBIDDER SUCCEEDED')
                return True
            else:
                logging.info('WRITE PBIDDER FAILED')
                return False
        except:
            logging.info('EXCEPTIONS THROWN WRITING PBIDDER')
            return self._generalError

    def readCBidder(self):

        try:
            temp = str(self.cBidder)
            temp = temp.strip()

            if temp.isalnum():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeCBidder(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isalnum():
                self.cBidder = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBidOnThisJob(self):
        try:
            temp = str(self.BidonThisJob)
            temp = temp.strip()

            if temp.isalnum():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBidOnThisJob(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.BidonThisJob = strinput
                logging.info('WRITE JOB REFERENCE SUCCEDED:')
                return True
            else:
                logging.info('WRITE BID JOB REFERENCE FAILED:')
                return False
        except:
            return self._generalError

    def readMilestonePayment(self):
        try:
            temp = str(self.MilestonePayment)
            temp = temp.strip()
            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMilestonePayment(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                logging.info('WRITE MILESTONE PAYMENT SUCCEEDED:')
                self.MilestonePayment = strinput
                return True
            else:
                logging.info('WRITE MILESTONE PAYMENT FAILED:')
                return False
        except:
            return self._generalError

    def readMilestoneMarker(self):
        try:
            temp = str(self.MilestoneMarker)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMilestoneMarker(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            if strinput.isdigit():
                logging.info('WRITE MILESTONE MARKER SUCCEEDED:')
                self.MilestoneMarker = strinput
                return True
            else:
                logging.info('WRITE MILESTONE MARKER FAILED:')
                return False
        except:
            return self._generalError

    def retrievePBidder(self):
        try:

            temp = self.pBidder

            if not(self.pBidder == self.undefined):
                temp = Reference.get(self.pBidder)
                if temp.readIsValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    def retrieveCBidder(self):
        try:


            if not(self.cBidder == self.undefined):
                temp = Company.get(self.cBidder)
                if temp.readisValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError

    def retrieveBidOnThisJob(self):
        try:

            if not(self.BidonThisJob == self.undefined):
                temp = Job.get(self.BidonThisJob)
                if temp.readisValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self._JobsNotFound
        except:
            return self._generalError