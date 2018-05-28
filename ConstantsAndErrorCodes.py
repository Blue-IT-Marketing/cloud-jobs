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
import os
import logging

tEnviron = os.environ.copy()
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    isGoogleServer = False
    logging.info('THIS IS A DEVELOPMENT SERVER')
else:
    logging.info('THIS IS A GOOGLE SERVER')
    isGoogleServer = True


from utilities import Util
class MyConstants(Util):
    undefined = None  # meaning no value and does not infer any type

    Guser = None # A Google User Object
    _maxQResults = 50  # Maximum Query Results
    _maxGoogleResults = 1000
    _maxBoardMessagesDisplay = 50
    _maxHomeProfileList = 15
    _maxInboxMessages = 10
    _maxExams = _maxGoogleResults
    _CreditExchangeRatio = 100
    _pkeyvalue = undefined  # pkeyvalue holds the reference key value of the present user
    _namesPkeyvalue = undefined  # namesPkeyValue holds the reference key value of the present Names Class
    _privatePkey = undefined  #privatePkeyValue holds the reference key value of the present private class
    _contactPkey = undefined
    _physicalAddressPkey = undefined
    _tempCodeO = 'ahlkZXZ-ZnJlZWxhbmNpbmctc29sdXRpb25zchYLEglSZWZlcmVuY2UYgICAgICAgAkM'
    _tempCode = 'abc05529818'
    _ReferenceLen = 21
    _jobkindsPkey = undefined
    _jobtypesPkey = undefined
    _jobPkey = undefined
    _jobBudgetPkey = undefined

    _googleResultLimit = 1000  # Maximum possible results that could be returned on one page
    _featuredProfilesLimit = 15

    _defaultCurrency = '$'
    _bidPkey = undefined

    _walletPKey = undefined

    _employerPKey = undefined
    _maxResults = _maxQResults
    _AppEmail = 'freelancing-solutions@appspot.gserviceaccount.com'
    _MobyMail = 'mobiusndou@gmail.com'
    _bidJobPkey = undefined
    showloginNotice = True

    _FreelanceJobsListMemCacheKey = 'FreelanceJobsListOnSendFreelanceJobs'
    _AwardedComMessages = 'AwardedCommMessages1'
    _LoadedProfile = 'loadedprofile'
    _loadUserOnlineCache = 'UserOnlineCache'


    _TotalUsersKey = os.environ['APPLICATION_ID'] + 'TotalUsersKey'
    _UsersListKey = os.environ['APPLICATION_ID'] + 'UsersListKey'

'''
#Constantss

_maxResults = 50 #Max Query results for results pages
_pkeyvalue = undefined #pkeyvalue holds the reference key value of the present user
_namesPkeyvalue = undefined #namesPkeyValue holds the reference key value of the present Names Class
_privatePkey = undefined #privatePkeyValue holds the reference key value of the present private class
_contactPkey = undefined
_physicalAddressPkey = undefined
_googleResultLimit = 1000 #Maximum possible results that could be returned on one page
'''


class ErrorCodes():
        #Error Messages
    _userNotLoggedin = 'User Not Logged in, You have to Login to Fully Participate'
    _UserNotAuthorised = 'You are not authorised to perform this action'

    _userNameConflict = 'User Name Conflict'
    _referenceNumConflict = 'Reference Number Do not Exist'
    _IDNumConflict = 'ID Number Conflict'
    _IDNumDonotExist = 'ID Number Do Not Exist'

    _clsNamesDonotExist = 'Names Class Do Not Exist or not Found'
    _clsReferenceDonotExist = 'Notice in order to be able to fully participate you must fully subscribe in our system'
    _clsPhysicalDonotExist = 'Physical Address Class Do not Exist or not Found'
    _clsContactDonotExist = 'Contact Class Do not Exist or not Found'
    _clsPrivateDonotExist = 'Private Class Do not Exist or not Found'
    _clsAccountDetailsDoNotExist = 'Bank Account Details do not exist please create a new account'

    _referenceDoNotExist = 'Reference Number Do Not Exist'
    _userNameDonotExist = 'UserName Do not Exist' # if a username is not available on the datastore the this error is returned
    _generalError = 'General System Error' # an application returns this general error message for everything we cannot resolve
    _JobKindNotFound = 'Job Kind not Found'
    _JobTypesNotFound = 'Job Types not Found'
    _JobsNotFound = 'Jobs Not Found'

    _pkeyNotSet = 'Primary Key not set' #returning this error when we try to save another class by making use of the _pkeyvalue to set
    #a relationship to the reference class and the _pkeyvalue is not set
    _ErrorCreatingBid = 'Error Creating Bid'
    _CannotBidOnOwnJob = 'Cannot Bid on Own Job'
    _BidderNotFound = 'Bidder not Found'

    _AccountDetailsInvalid = 'Account Details Not Valid'
    _PhysicalAddressINvalid = 'Invalid Physical Address'
    _ContactDetailsInvalid = 'Invalid Contact Details'
    _SchoolContactPersonDoNotExist = 'School Contact Person Do not Exist'
    _ContactPersonDoNotExist    = 'Contact Person Do Not Exist'
    _SchoolContactPersonInvalid = 'School Contact Person is Invalid'
    _ReferenceInvalid = 'Notice in order to be able to fully participate you must create a user account in our system'
    _EmployerCompanyInvalid = 'Invalid Employer Company'
    _OwnerCompanyInvalid = 'Invalid Company Job Owner'
    _QualificationsInvalid = 'Invalid Qualifications'
    _QualificationsDoNotExist = 'Qualifications Class Do Not Exists'
    _RequiredQualificationsInvalid = 'Required Qualifications Invalid'
    _RequiredQualificationsDoNotExist = 'Required Qualifications Invalid'
    _RequiredSkillsInvalid = 'Required Skills Invalid'
    _RequiredSkillsDoNotExist = 'Required Skills Do Not Exist'
    _SkillsInvalid = 'Skills Invalid'
    _JobBudgetSalaryInvalid = 'Job Budget or Salary Invalid'
    _JobBudgetSalaryDoNotExist = 'Job Budget Salary Do Not Exist'
    _JobTypeInvalid = 'Job Type Invalid'
    _JobKindInvalid = 'Job Kind Invalid'
    _JobOwnerInvalid = 'Job Owner Invalid'
    _JobNotesDoNotExist = 'Job Notes Do Not Exist'
    _JobDefinitionDoNotExist = 'Job Definition Do Not Exist'
    _JobTitleDoNotExist = 'Job Title Do Not Exist'
    _JobIsInvalid = 'Job is Invalid'



    _BiddingClosedOn = 'Bidding Closed'
    _FreelanceJobNoLongerExist = 'The Freelance Job you are bidding on is no longer open for bidding'
    _UserNotVerified = 'User Account Not Verified'
    _CompleteSubscriptionForm = 'In Order to succesfully work within our website please complete the subscription Form'
    _EmailSuccesfullyVerified = 'Account Email is succesfully Verified'
    _CellNumberSuccesfullyVerified = 'Account Cell Number is successfully verified'
    _VerificationCodeIncorrect = 'Verification Code is Incorrect'
    _InsufficientFunds = 'Insufficient funds to perform transactions please TopUp your account'
    _NotEnoughCreditToSponsorBid = 'Not Enough Credit to Sponsor your Bid'
    _FeedbackCreatedSuccesfully = 'Feedback Message Sent Succesfully, Your response will be sent through to your email address'
    _FeedbackNotCreatedSuccesfully = 'Feedback Message was Not Succesfully Created'


'''
        #Error Messages
_userNameConflict = 10001
_referenceNumConflict = 10002
_IDNumConflict = 10003
_IDNumDonotExist = 10008
_clsNamesDonotExist = 10009
_clsReferenceDonotExist = 10010
_clsPhysicalDonotExist = 10011
_clsContactDonotExist = 10012
_clsPrivateDonotExist = 10013

_referenceDoNotExist = 10004
_userNameDonotExist = 10005 # if a username is not available on the datastore the this error is returned
_generalError = 10006 # an application returns this general error message for everything we cannot resolve

_pkeyNotSet = 10007 #returning this error when we try to save another class by making use of the _pkeyvalue to set
#a relationship to the reference class and the _pkeyvalue is not set
'''


