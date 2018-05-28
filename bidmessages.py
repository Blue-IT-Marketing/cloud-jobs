#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'

# Copyright 2014 Freelancing Solutions.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datatypes import Reference
import datetime
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from datatypes import Reference
import logging

class BidMessages(db.Expando, MyConstants, ErrorCodes):
    MessageHeading = db.StringProperty()
    Message = db.StringProperty() # Actual Message Sent
    BidReference = db.StringProperty()
    MessageSender = db.StringProperty() # Name or username of the sender
    DateCreated = db.DateProperty(auto_now_add=True)

    def readMessageHeading(self):
        pass

    def writeMessageHeading(self, strinput):
        pass

    #input the BidReference Number
    #Returns all the messages for the BID
    def DelBidMessages(self, inBidReference):
        try:
            BidMessagesList = self.getBidMessages(strinput=inBidReference)
            if len(BidMessagesList) > 0:
                i = 0
                while i < len(BidMessagesList):
                    BidMessage = BidMessagesList[i]
                    tKey = BidMessage.key()
                    db.delete(tKey)
                    i = i + 1
            return True
        except:
            return self._generalError


    def getBidMessages(self, strinput):
        try:
            strinput = str(strinput)
            findrequest = db.Query(BidMessages).filter('BidReference =', strinput).order('-DateCreated')
            results = findrequest.fetch(limit=self._maxGoogleResults)
            if len(results) > 0:
                return results
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBidMessage(self,inBidRef, inMessage, inMessageSender):
        try:
            if self.writeBidReference(inBidRef) and self.writeMessage(inMessage) and self.writeMessageSender(inMessageSender):
                tkey = self.put()
                logging.info(msg='WRITE BID MESSAGES CALLED AND SAVED :')
                return True
            else:
                return False
        except:
            return self._generalError

    def readMessage(self):
        try:
            temp = str(self.Message)
            temp = temp.strip()
            return temp
        except:
            return self._generalError

    def writeMessage(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.Message = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBidReference(self):
        try:
            temp = str(self.BidReference)
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError


    def writeBidReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.BidReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readMessageSender(self):
        try:
            temp = self.MessageSender
            temp = temp.strip()

            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMessageSender(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()


            if len(strinput) > 0:
                self.MessageSender = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def deleteMessage(selfself, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.lower()

            if len(strinput) > 0:
                if self.Message.lower() == strinput.lower():
                    self.Message = ""
        except:
            return self._generalError

