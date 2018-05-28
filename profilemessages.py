#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2

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

#######################################################################################################################
############################### FREELANCE PROFILE #####################################################################
#######################################################################################################################
# the profile must also included banking details and internal account balances.
# a way to intergrated PayPal, BitCoin and credit card payments must eb included.
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db

class ProfileMessages(db.Expando, MyConstants, ErrorCodes):
    MessageReference = db.StringProperty()
    #Todo -- Work needs to be done to include message heading on the profile messages
    PMessageHeading = db.StringProperty()
    #Todo -- Include the relevancy field to indicate wheather the message is related to freelancing, market place, affiliates or even the job market

    PMessage = db.StringProperty(multiline=True)
    SenderReference = db.StringProperty()  # The Actual Reference Number of the Sender
    RecipientReference = db.StringProperty() # The Actual Reference Number of The Receipient
    DateTimeSent = db.DateTimeProperty(auto_now_add=True)
    IsMessageOpened = db.BooleanProperty(default=False)
    ResponseMessage = db.StringProperty(multiline=True)
    ResponseReceived = db.BooleanProperty(default=False)

    def createMessage(self, inMessage,inMessageHeader, inSenderRef, inReceipientRef):
        try:
            if self.writePMessage(strinput=inMessage) and self.writeSenderReference(strinput=inSenderRef) and \
                    self.writeReceipientReference(strinput=inReceipientRef) and self.writeMessageHeader(strinput=inMessageHeader):
                self.MessageReference = str(self.put())
                self.put()
                return True
            else:
                return False
        except:
            return self._generalError

    def createResponse(self, inResponse):
        try:
            if self.writeResponseMessage(inResponse):
                self.put()
                return True
            else:
                return False
        except:
            return self._generalError


    def findMessagesSentToMe(self, myReference):
        try:
            findquery = db.Query(ProfileMessages).filter('RecipientReference =', myReference).order('-DateTimeSent')
            results = findquery.fetch(limit=self._maxGoogleResults)
            if len(results) > 0:
                i = 0
                tres = []
                while i < len(results):
                    tmessage = results[i]
                    if not((tmessage.readMessage() == self.undefined) or (tmessage.readMessage() == 'None')):
                        tres.append(tmessage)
                    i = i + 1

                return tres
            else:
                return self.undefined
        except:
            return self._generalError

    def findMessagesISent(self, myReference):
        try:
            findquery = db.Query(ProfileMessages).filter('SenderReference =', myReference).order('-DateTimeSent')
            results = findquery.fetch(limit=self._maxGoogleResults)
            if len(results) > 0:
                return results
            else:
                return self.undefined
        except:
            return self._generalError

    def readMessageHeader(self):
        try:
            temp = str(self.PMessageHeading)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMessageHeader(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.PMessageHeading = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPMessage(self):
        try:
            temp = str(self.PMessage)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePMessage(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.PMessage = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readSenderReference(self):
        try:
            temp = str(self.SenderReference)
            temp = temp.strip()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSenderReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.SenderReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readReceipientReference(self):
        try:
            temp = str(self.RecipientReference)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeReceipientReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.RecipientReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readDateTimeSent(self):
        try:
            temp = self.DateTimeSent
            if temp:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def readIsMessageOpened(self):
        try:
            temp = self.IsMessageOpened
            return temp
        except:
            return self._generalError

    def writeIsMessageOpened(self, inCondition):
        try:
            if inCondition == True:
                self.IsMessageOpened = True
                return True
            else:
                self.IsMessageOpened = False
                return True
        except:
            return self._generalError


    def readResponseMessage(self):
        try:
            temp = str(self.ResponseMessage)
            temp = temp.strip()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeResponseMessage(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.ResponseMessage = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readResponseReceived(self):
        try:
            temp = self.ResponseReceived
            if temp == True:
                return True
            else:
                return False
        except:
            return self._generalError

    def writeResponseReceived(self, inCondition):
        try:
            if inCondition == True:
                self.ResponseReceived = True
                return True
            else:
                self.ResponseReceived = False
                return True
        except:
            return self._generalError




