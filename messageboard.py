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
import webapp2
import jinja2
from ConstantsAndErrorCodes import MyConstants, ErrorCodes
from google.appengine.ext import db


#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

_70900Advert="""
<div align="center">
<!-- Adsense Code -->
      <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- Freelancing-Solutions -->
<ins class="adsbygoogle"
     style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-7790567144101692"
     data-ad-slot="4810280165"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
<!-- Ending Adnsense -->
</div>
"""

class MessageBoard(db.Expando, MyConstants, ErrorCodes):
    MessageHeading = db.StringProperty()
    BoardMessage = db.StringProperty(multiline=True)
    SenderNames = db.StringProperty()
    SenderEmail = db.EmailProperty()
    MessageActivated = db.BooleanProperty(default=False)
    DateTimeCreated = db.DateTimeProperty(auto_now_add=True)

    #make sure to integrate the heading with the overall messageboard
    def readMessageHeading(self):
        try:
            temp = str(self.MessageHeading())
            temp = temp.strip()
            if len(temp) >= 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMessageHeading(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) >= 0:
                self.MessageHeading = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def createBoardMessage(self, inSenderNames, inSenderEmail, inBoardMessage,inMessageHeading, inMessageActivated):
        try:
            if self.writeSenderNames(strinput=inSenderNames) and self.writeSenderEmail(strinput=inSenderEmail) and self.writeBoardMessage(strinput=inBoardMessage) and self.writeMessageHeading(strinput=inMessageHeading) and self.writeMessageActivated(inCondition=inMessageActivated):
                self.put()
                return True
            else:
                return False
        except:
            return self._generalError
    def createAdvertMessage(self):
        try:
            if self.writeSenderNames(strinput='Comment Here') and self.writeSenderEmail(strinput='mobiusndou@gmail.com') and self.writeBoardMessage(strinput=_70900Advert) and self.writeMessageActivated(inCondition=True):
                self.put()

                return True
            else:
                return False
        except:
            return self._generalError

    def returnRecentBoardMessages(self):
        try:
            findquery = db.Query(MessageBoard).filter('MessageActivated =', True).order('DateTimeCreated')
            results = findquery.fetch(limit=self._maxBoardMessagesDisplay)
            if len(results) > 0:
                return results
            else:
                return self.undefined
        except:
            return self._generalErrors

    def readMessageActivated(self):
        try:
            return self.MessageActivated
        except:
            return self._generalError

    def writeMessageActivated(self, inCondition):
        try:
            if inCondition == True:
                self.MessageActivated = True
                return True
            else:
                self.MessageActivated = False
                return True
        except:
            return self._generalError

    def readBoardMessage(self):
        try:
            temp = str(self.BoardMessage)
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeBoardMessage(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0 and not(strinput == self.undefined) and not(strinput == 'None'):
                self.BoardMessage = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readSenderNames(self):
        try:
            temp = str(self.SenderNames)
            temp = temp.strip()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSenderNames(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if len(strinput) > 0:
                self.SenderNames = strinput
                return True
            else:
                return False
        except:
            return self.undefined


    def readSenderEmail(self):
        try:
            temp = str(self.SenderEmail)
            temp = temp.strip()
            if len(temp) > 0:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSenderEmail(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if len(strinput) > 0:
                self.SenderEmail = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class PublicMessageBoardHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        tMessageBoard = MessageBoard()
        tMessageBoardList = tMessageBoard.returnRecentBoardMessages()
        template = template_env.get_template('templates/messageboardlist.html')

        if tMessageBoardList == self.undefined:
            context = {}
        elif tMessageBoardList == self._generalError:
            context = {}
        else:
            context = {'MessageBoardList': tMessageBoardList }
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([('/PublicMessagingUpdates', PublicMessageBoardHandler)], debug=True)