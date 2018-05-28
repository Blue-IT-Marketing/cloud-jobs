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
########################### CLIENT & FREELANCER BANKING DETAILS ########################################################
################################### FIND OUT THE DIFFERENT COMMANDS FOR INTERFACING WITH THIS INSTITUTIONS #############

from datatypes import Reference
from utilities import CustomEmail
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

class BankingDetails(db.Expando, MyConstants, ErrorCodes):
    _maxNameOfInstitutionLen = 256
    _minNameOfInstitutionLen = 2
    _maxAccountNumberLen = 20
    _minAccountNumberLen = 4
    _AccountTypes = ['savings', 'cheque', 'transmission']
    _minBranchCodeLen = 4
    _maxBranchCodeLen = 8

    strNameofInstitution = db.StringProperty()
    strAccountNumber = db.StringProperty()
    strAccountType = db.StringProperty()
    strBranchCode = db.StringProperty()

    def createBankAccount(self):
        pass


    def removeBankAccount(self):
        pass


    def readNameOfInstitution(self):
        try:
            if not(self.strNameofInstitution == self.undefined):
                return self.strNameofInstitution
            else:
                return self.undefined
        except:
            return self._generalError

    def writeNameOfInstitution(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput.isalpha() or strinput.isalnum()) and (len(strinput) <= self._maxNameOfInstitutionLen) and (len(strinput) >= self._minNameOfInstitutionLen):
                self.strNameofInstitution = strinput
                return True
            else:
                self.strNameofInstitution = self.undefined
                return False
        except:
            return self._generalError

    def readAccountNumber(self):
        try:
            if not(self.strAccountNumber == self.undefined):
                return self.strAccountNumber
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAccountNumber(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput.isdigit() and (len(strinput) <= self._maxAccountNumberLen) and (len(strinput) >= self._minAccountNumberLen):
                self.strAccountNumber = strinput
                return True
            else:
                self.strAccountNumber = self.undefined
                return False
        except:
            return self._generalError

    def readAccountType(self):
        try:
            if not(self.strAccountType == self.undefined):
                return self.strAccountType
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAccountType(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._AccountTypes:
                self.strAccountType = strinput
                return True
            else:
                self.strAccountType = self.undefined
                return False
        except:
            return self._generalError


    def readBranchCode(self):
        try:

            if not(self.strBranchCode == self.undefined):
                return self.strBranchCode
            else:
                return self.undefined
        except:
            return self._generalError


    def writeBrachCode(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput.isdigit() and (len(strinput) <= self._maxBranchCodeLen) and (len(strinput) >= self._minBranchCodeLen):
                self.strBranchCode = strinput
                return True
            else:
                self.strBranchCode = self.undefined
                return False
        except:
            return self._generalError

class PayPalAccount(db.Expando, MyConstants, ErrorCodes):
    _testEmail = CustomEmail
    strEmailAddress = db.EmailProperty()
    # input all the information needed to perform a transaction on behalf of the client.

    # this class will hold the details of transactions between the freelancers and also with freelancing solutions.

    def createPayPalAccount(self):
        pass

    def RemovePayPalAccount(self):
        pass


    def readPayPalEmail(self):
        try:
            if not(self.strEmailAddress == self.undefined):
                return self.strEmailAddress
            else:
                return self.undefined
        except:
            return self._generalError

    def writePayPalEmail(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.strEmailAddress = strinput
                return True
            else:
                self.strEmailAddress = self.undefined
                return False
        except:
            return self._generalError

class AccountDetails(BankingDetails, PayPalAccount, MyConstants, ErrorCodes):
    strInternalBalance = db.StringProperty(default='0')  # This balance includes the money deposited and made on this website
    # account history class must be created
    IndexReference = db.StringProperty()


    def setIsValid(self):
        try:
            if (not(self.strEmailAddress == self.undefined)) or (not(self.strAccountNumber == self.undefined) and not(self.strNameofInstitution == self.undefined) and not(self.strBranchCode == self.undefined) and not(self.strAccountType == self.undefined)):
                return True
            else:
                return False
        except:
            return self._generalError

    def isValid(self):
        try:
            if self.setIsValid():
                return True
            else:
                return False
        except:
            return self._generalError

    def readInternalBalance(self):
        try:
            if not(self.strInternalBalance == self.undefined):
                return self.strInternalBalance
            else:
                return self.undefined
        except:
            return self._generalError

    def writeInternalBalance(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()


            if strinput.isdigit():
                self.strInternalBalance = strinput
                return True
            else:
                self.strInternalBalance = self.undefined
                return False
        except:
            return self._generalError

    def TopupFromPayPal(self, TopAmount):
        pass

    def TopUpFromDirectDeposit(self):
        pass

# This class contains control information for the users wallet how much money it contains when to withdraw and how
#We must be able to store the wallet to our Datastore
#The Wallet class must include the logic to deposit and withdraw money
#Be able to show the present Balance on Screen
#Be able to show account details on screen and enable users to edit them
#Be able to verify PayPal Account Details9999
#The Wallet class must call the classes to save the Transaction Details for each user
#The Wallet class must be able to show transaction details on screen for each user.

class Wallet(db.Expando, MyConstants, ErrorCodes):

    clsAccount = db.ReferenceProperty(AccountDetails, collection_name='wallet_collection')
    clsAccountHolder = db.ReferenceProperty(Reference, collection_name='wallet_collection')
    DateCreated = db.DateTimeProperty(auto_now_add=True)  # The Date this Account was created
    DateEdited = db.DateTimeProperty(auto_now=True)  # The Date The Account Details where modified

    #   Take in the Amount to be paid, and the account to pay to
    #   inPayment is the amount to pay from the present account
    #   toAccount is the Reference to the account to be credited with the payment
    #   toAccount Contains the Reference to Account Details this transaction will to up the internal account balance

    def ProcessPayment(self, InPaymentAmount, toAccount):
        pass
    # Transfer funds will transfer funds from the present account to another account for a different user, thereby
    # This function can be used by the system to create payments for specific services
    def TransferFunds(self, transferAmount):
        pass

    def readDateCreated(self):
        try:
            return self.DateCreated
        except:
            return self._generalError

    def readDateEdited(self):
        try:
            return self.DateEdited
        except:
            return self._generalError

    def readAccountHolder(self):
        try:
            if not(self.clsAccountHolder == self.undefined):
                return self.clsAccountHolder()
            else:
                return self.undefined
        except:
            return self._generalError
    def writeAccountHolder(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.clsAccountHolder = strinput
                return True
            else:
                self.clsAccountHolder = self.undefined
                return False
        except:
            return self._generalError

    def retrieveAccountHolder(self):
        try:

            if not(self.clsAccountHolder == self.undefined):
                temp = Reference.get(self.clsAccountHolder)
                if temp.isValid():
                    return temp
                else:
                    return self.undefined
            else:
                return self.undefined
        except:
            return self._generalError


    def readAccountDetails(self):
        try:
            if not(self.clsAccount == self.undefined):
                return self.clsAccount()
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAccountDetails(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.clsAccount = strinput
                return True
            else:
                self.clsAccount = self.undefined
                return False
        except:
            return self._generalError
    # Account Details must only be retrievable by the adminstrator and also the owner of the account
    def retrieveAccountDetails(self):
        try:
            Guser = users.get_current_user()

            if Guser:

                findquery = db.Query(Reference).filter('strReference =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if self.clsAccountHolder() == result.key():  # If The reference Matches then the user is authorised
                        if not(self.clsAccount == self.undefined):
                            temp = AccountDetails.get(self.clsAccount)
                            if temp.isValid():
                                return temp
                            else:
                                return self.undefined
                        else:
                            return self.undefined
                    else:
                        return self._UserNotAuthorised
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    # Save Account Details can save to an exisiting class or create a new class.
    # we must check the identity of the user saving the Account Details

    def saveAccountDetails(self, clsinput):
        try:

            Guser = users.get_current_user()
            if Guser:
                findquery = db.Query(Reference).filter('strReference =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]

                    if self.clsAccountHolder() == result.key():
                        if clsinput.IsValid():
                            if self.clsAccount == self.undefined:
                                self.clsAccount = clsinput.put() # This Will create a new account Details Class
                                if not(self.clsAccount == self.undefined):
                                    return True
                                else:
                                    return False
                            else:
                                # Theres an existing account and we must save on top of it
                                eAccount = AccountDetails.get(self.clsAccount)
                                if eAccount.isValid():
                                    eAccount.writeAccountNumber(clsinput.readAccountNumber())
                                    eAccount.writeAccountType(clsinput.readAccountType())
                                    eAccount.writeBrachCode(clsinput.readBranchCode())
                                    eAccount.writeInternalBalance(clsinput.readInternalBalance())
                                    eAccount.writeNameOfInstitution(clsinput.readNameOfInstitution())
                                    eAccount.writePayPalEmail(clsinput.readPayPalEmail())

                                    self.clsAccount = eAccount.put() # Finally saving back the changes
                                    return True
                                else:
                                    return False

                        else:
                            return self._AccountDetailsInvalid
                    else:
                        return self._UserNotAuthorised
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    # Save Account Holder Details cannot create a new Reference Class but rather can update an existing class
    def saveAccountHolder(self, clsinput):
        try:
            Guser = users.get_current_user()

            if Guser:
                if Guser.user_id() == clsinput.strReference(): # If the Current User ID is equal to the reference
                    # of the class being saved then the save will succeed as the user is the owner of the class
                    if clsinput.IsValid():
                        # Avoid using a primary key since the assembled Reference Class might not possess it
                        findquery = db.Query(Reference).filter('strReference =', clsinput.strReference())
                        results = findquery.fetch(limit=self._maxQResults)
                        if len(results) > 0:
                            result = results[0]
                            result.writeLogoPhoto(clsinput.readLogoPhoto())
                            result.writeDateTimeVerified(clsinput.readDatetimeVerified())
                            result.writeIsUserVerified(clsinput.readIsUserVerified())
                            result.writeVerEmail(clsinput.readVerEmail())
                            result.writeUsername(clsinput.readUsername())
                            result.writePassword(clsinput.readPassword())
                            result.writeReference(clsinput.readReference())
                            result.writeIDNumber(clsinput.readIDNumber())

                            if result.readIsValid():
                                self.clsAccountHolder = result.put()
                                if not(self.clsAccountHolder == self.undefined):
                                    return True
                                else:
                                    return False
                            else:
                                return self._InvalidAccountHolder
                        else:
                            return self._clsReferenceDonotExist
                    else:
                        return self._InvalidAccountHolder
                else:
                    return self._UserNotAuthorised
            else:
                return self._userNotLoggedin
        except:
            return self._generalError

    # This function saves the current wallet to the datastore
    # it only works if the account holder, and account details has already been saved to the data store
    def saveWallet(self):
        try:
            Guser = users.get_current_user()

            if Guser:
                findquery = db.Query(Reference).filter('strReference =', Guser.user_id())
                results = findquery.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    result = results[0]
                    if self.clsAccountHolder() == result.key():
                        # Get Account Details.
                        taccountDetails = AccountDetails.get(self.clsAccount())
                        if taccountDetails.isValid():
                            self._walletPKey = self.put() # Saving The Current Wallet Class to the data store and
                            # returning the primary key, The Key must be used to create a relation between a person and
                            # his/her wallet, or maybe used on the accounting class for the overall application
                            return self._walletPKey
                        else:
                            return self._AccountDetailsInvalid
                    else:
                        return self._UserNotAuthorised
                        # User Do Not Exist
                else:
                    return self._clsReferenceDonotExist
            else:
                return self._userNotLoggedin
        except:
            return self._generalError
    # Creating a wallet will work like this, first a user must posses a Reference Class.
    # Then the account details class must be created and saved.
    # Then The Wallet Details can then be saved, and the key be saved on the main accounting class.
