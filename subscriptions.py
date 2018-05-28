__author__ = 'freelancing'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'



from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from datatypes import Reference
''' Bid Packs
50" selected>Free Bundle 50 ($ 0.00)</option>
75">Starter Bundle 75 ($ 2.00)</option>
100">Medium Bundle 100 ($ 3.50)</option>
150">Large Bundle 150 ($ 5.00)</option>
200">Premium Small 200 ($ 6.50)</option>
250">Premium Medium 250 ($ 8.00)</option>
300">Premium Large 300 ($ 9.50)</option>
500">Ultimate 500 ($ 14.00)</option>
'''
class FreelanceJobsBidsSub (db.Expando, MyConstants, ErrorCodes):
    fBidSubValues = ['50', '75', '100', '150', '200', '250', '300', '500']
    fBidSubDescr = ['Free Bundle 50', 'Starter Bundle 75', 'Medium Bundle 100', 'Large Bundle 150', 'Premium Small 200',
                     'Premium Medium 250', 'Premium Large 300', 'Ultimate 500']
    fBidSubAmount = ['0', '2', '3', '4', '5', '6', '7', '8']


'''
Profile Promo
<option value="50" selected>Free Points 50 ($ 0.00)</option>
<option value="75">Starter Points Pack 75 ($ 2.00)</option>
<option value="100">Medium Points Pack 100 ($ 3.50)</option>
<option value="150">Large Points Pack 150 ($ 5.00)</option>
<option value="200">Premium Points Pack Small 200 ($ 6.50)</option>
<option value="250">Premium Points Pack Medium 250 ($ 8.00)</option>
<option value="300">Premium Points Pack Large 300 ($ 9.50)</option>
<option value="500">Ultimate Points Pack 500 ($ 15.00)</option>
'''
class ProfileSub(db.Expando, MyConstants, ErrorCodes):
    fProfileValues = ['50', '75', '100', '150', '200', '250', '300', '500']
    fProfileDescr = ['Free Points 50', 'Starter Points Pack 75', 'Medium Points Pack 100', 'Large Points Pack 150',
                     'Premium Points Pack Small 200', 'Premium Points Pack Medium 250', 'Premium Points Pack Large 300',
                     'Ultimate Points Pack 500']
    fProfileAmount = ['0', '2', '4', '5', '7', '8', '10', '15']
'''Freelance Jobs Submission Pack
<option value="25" selected>Free Pack 25 ($ 0.00)</option>
<option value="50">Starter Pack 50 ($ 5.00)</option>
<option value="75">Medium Pack 75 ($ 7.50)</option>
<option value="100">Large Pack 100 ($ 10.00)</option>
<option value="150">Premium Pack Small 150 ($ 15.00)</option>
<option value="200">Premium Pack Medium 200 ($ 20.00)</option>
<option value="250">Premium Pack Large 250 ($ 25.00)</option>
<option value="500">Ultimate Pack 500 ($ 50.00)</option>
'''
class JobSubmissionSub(db.Expando, MyConstants, ErrorCodes):
    fJobSubmissionsValues = ['25', '50', '75', '100', '150', '200', '250', '500']
    fJobSubmissionsDescr = ['Free Pack 25', 'Starter Pack 50', 'Medium Pack 75', 'Large Pack 100', 'Premium Pack Small 150',
                            'Premium Pack Medium 200', 'Premium Pack Large 250', 'Ultimate Pack 500']
    fJobSubmissionsAmount = ['0', '5', '8', '10', '15', '20', '25', '50']
'''
value
Descr
Amount
'''



class Subscriptions(db.Expando, MyConstants, ErrorCodes):
    indexReference = db.ReferenceProperty(Reference, collection_name='subscriptions')
    # Freelance Jobs Subscriptions
    fBidSubIndex = db.StringProperty(default='0')  #  The Current Subscription to replenish the TotalBidsCredit every 30 days
    TotalBidsCredit = db.StringProperty(default=FreelanceJobsBidsSub.fBidSubValues[0])  #  Total Bids Credit on Hand everytime the user makes a bid they spend
    # their bid credit and can be repleted by buying more Bid Credits

    fProfileIndex = db.StringProperty(default='0')  # The Current Subscription value to replenish the
    # Total Profile Promotion Credit
    TotalProfileCredit = db.StringProperty(default=ProfileSub.fProfileValues[0])  #

    fJobSubmissionIndex = db.StringProperty(default='0')
    TotalJobSubmissionCredit = db.StringProperty(default=JobSubmissionSub.fJobSubmissionsValues[0])
    DateCreated = db.DateTimeProperty(auto_now_add=True)
    DateModified = db.DateTimeProperty(auto_now=True)



    # Market Place Subscriptions

    # Affiliates Subscriptions

    # Job Market Subscriptions

    SubBalance = db.StringProperty(default='0')  # The Current Value of all Subscriptions
    SubDateOFExecution = db.DateProperty()  # The Date of the next Execution of Subscriptions # date ine ha tea u
    # minusiwa tshelede ya subscription nga system

    def addJobSubmissionCredit(self, inJobSubCredit):
        try:
            inJobSubCredit = str(inJobSubCredit)
            inJobSubCredit = inJobSubCredit.strip()

            if inJobSubCredit.isdigit():
                self.TotalJobSubmissionCredit = str(int(self.TotalJobSubmissionCredit) + int(inJobSubCredit))
                return True
            else:
                return False
        except:
            return self._generalError


    def addBiddingCredit(self, inBidCredit):
        try:
            inBidCredit = str(inBidCredit)
            inBidCredit = inBidCredit.strip()

            if inBidCredit.isdigit():
                self.TotalBidsCredit = str(int(self.TotalBidsCredit) + int(inBidCredit))
                return True
            else:
                return False
        except:
            return self._generalError


    def addProfileCredit(self, inProfileCredit):
        try:
            inProfileCredit = str(inProfileCredit)
            inProfileCredit = inProfileCredit.strip()

            if inProfileCredit.isdigit():
                self.TotalProfileCredit = str(int(self.TotalProfileCredit) + int(self.TotalProfileCredit))
                return True
            else:
                return False
        except:
            return self._generalError

    def writeIndexReference(self):
        pass
    def readIndexReference(self):
        pass

    def readJobSubmissionCredit(self):
        try:
            temp = str(self.TotalJobSubmissionCredit)


            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeJobSubmissionCredit(self, inCredit):
        try:
            inCredit = str(inCredit)
            inCredit = inCredit.strip()

            if inCredit.isdigit():
                self.TotalJobSubmissionCredit = inCredit
                return True
            else:
                return False
        except:
            return self._generalError

    def readBiddingCredit(self):
        try:
            temp = str(self.TotalBidsCredit)
            temp = temp.strip()
            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBiddingCredit(self, inCredit):
        try:
            inCredit = str(inCredit)
            inCredit = inCredit.strip()

            if inCredit.isdigit():
                self.TotalBidsCredit = inCredit
                return True
            else:
                return False
        except:
            return self._generalError

    def readProfilePromoCredit(self):
        try:

            temp = str(self.TotalProfileCredit)
            temp = temp.strip()

            if temp.isdigit():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeProfilePromoCredit(self, inCredit):
        try:
            inCredit = str(inCredit)
            inCredit = inCredit.strip()

            if inCredit.isdigit():
                self.TotalProfileCredit = inCredit
                return True
            else:
                return False
        except:
            return self._generalError



    def assignOwner(self, indexref):
        try:
            self.indexReference = indexref
            return True
        except:
            return self._generalError
    # Returns Actual Bids Credit
    def readTotalBidsCredit(self):
        try:
            return self.TotalBidsCredit
        except:
            return self._generalError

    # Accept Actual Bid values
    def addTotalBidsCredit(self, invalue):
        try:
            invalue = str(invalue)
            invalue = invalue.strip()

            if invalue.isdigit():
                self.TotalBidsCredit = self.TotalBidsCredit + invalue
                return True
            else:
                return False
        except:
            return self._generalError


    def CalculateTotalSubAmount(self, inBidCredit, inProfileCredit, inJobSubCredit):
        try:
            inBidCredit = str(inBidCredit)
            inBidCredit = inBidCredit.strip()
            tempSubAmount = 0
            if inBidCredit.isdigit():
                if int(inBidCredit) > int(FreelanceJobsBidsSub.fBidSubValues[0]):
                    i = 1
                    while i < len(FreelanceJobsBidsSub.fBidSubValues):
                        if int(inBidCredit) == int(FreelanceJobsBidsSub.fBidSubValues[i]):
                            tempSubAmount = tempSubAmount + int(FreelanceJobsBidsSub.fBidSubAmount[i])
                            self.addBiddingCredit(FreelanceJobsBidsSub.fBidSubValues[i])
                            i = i + len(FreelanceJobsBidsSub.fBidSubValues)

                        else:
                            i = i + 1

            inProfileCredit = str(inProfileCredit)
            inProfileCredit = inProfileCredit.strip()

            if inProfileCredit.isdigit():
                if int(inProfileCredit) > int(ProfileSub.fProfileValues[0]):
                    i = 1
                    while i < len(ProfileSub.fProfileValues):
                        if int(inProfileCredit) == int(ProfileSub.fProfileValues[i]):
                            tempSubAmount = tempSubAmount + int(ProfileSub.fProfileAmount[i])
                            self.addProfileCredit(ProfileSub.fProfileValues[i])
                            i = i + len(ProfileSub.fProfileValues)
                        else:
                            i = i + 1

            inJobSubCredit = str(inJobSubCredit)
            inJobSubCredit = inJobSubCredit.strip()

            if inJobSubCredit.isdigit():
                if int(inJobSubCredit) > int(JobSubmissionSub.fJobSubmissionsValues[0]):
                    i = 1
                    while i < len(JobSubmissionSub.fJobSubmissionsValues):
                        if int(inJobSubCredit) == int(JobSubmissionSub.fJobSubmissionsValues[i]):
                            tempSubAmount = tempSubAmount + int(JobSubmissionSub.fJobSubmissionsAmount[i])
                            self.addJobSubmissionCredit(JobSubmissionSub.fJobSubmissionsValues[i])
                            i = i + len(JobSubmissionSub.fJobSubmissionsValues)
                        else:
                            i = i + 1

            return tempSubAmount
        except:
            return self._generalError





    #todo- consider checking weather the current user is the owner of the current subscription class
    def readIsValid(self):
        try:
            return True
        except:
            return self._generalError

    def recalcfBids(self, BidValue):
        pass
    def recalcfProfile(self):
        pass

    def recalcfJobSubmission(self):
        pass

    def writefBids(self):
        pass
    def writefProfile(self):
        pass
    def writefJobSub(self):
        pass












