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


from ConstantsAndErrorCodes import MyConstants, ErrorCodes
from google.appengine.ext import db



class ReviewBidsNotes(db.Expando, MyConstants, ErrorCodes):
    ScrapNoteHeading = db.StringProperty()
    BidScrapNotes = db.StringProperty(multiline=True)
    fReference = db.StringProperty()
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)


    def createScrapNote(self, inScrapNoteHeading, inScrapNote, inReference):
        try:
            if self.writeBidNotes(strinput=inScrapNote) and self.writeScrapNoteHeading(strinput=inScrapNoteHeading) and self.writeReference(strinput=inReference):
                self.put()
                return True
            else:
                return False
        except:
            return self._generalError

    def writeScrapNoteHeading(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.ScrapNoteHeading = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readScrapNoteHeading(self):
        try:
            temp = str(self.ScrapNoteHeading)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBidNotes(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.BidScrapNotes = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBidNotes(self):
        try:
            temp = str(self.BidScrapNotes)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeReference(self, strinput):
        try:
            strinput = str(strinput)
            if len(strinput) > 0:
                self.fReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readReference(self):
        try:
            temp = str(self.fReference)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def returnScrapNotes(self):
        pass
