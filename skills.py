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


from datatypes import Reference
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import logging




"""
CREATE A WAY TO SHOW EXPERIENCE RELATED TO A CERTAIN SKILL WITHIN THE SYSTEM THAT IS EITHER WORKING AS A FREELANCER,
ON THE MARKET PLACE, AND EVEN OFFLINE.
7
ALSO CREATE A MEANS ON SHOWING TEST RESULTS FROM THE TESTING CENTER.
"""

class Skills(db.Expando, MyConstants, ErrorCodes):
    _lstSkillsAvailable = ['portuguese', 'englishus', 'englishuk', 'spanish', 'french', 'afrikaans', 'html', 'css3', 'xml', 'java',
                           'java script', 'php', 'python', 'perl', 'wordpress','joomla', 'csharp', 'gae', 'jinja2', 'django',
                           'cplusplus', 'c', 'visualbasic', 'net', 'pascal', 'freepascal','delphi', 'go', 'seo', 'article writing',
                           'proof reading', 'copy writing', 'website development', 'landing page development', 'android', 'webapp', 'jquery']
    _minSkillLen = 2
    _maxSkillLen = 120
    skills = db.StringListProperty() #Every Skills class will contain a list of skills required for each job
    #The List of skills will be populate from the lstSkillsAvailable variable

    #create functions to save the available skills to file
    #and also the function to retrieve available skills from file
    # the function to save and load must be triggered automatically and manually
    # add a specific skill to the available skills

    #TODO- MAKE SURE THE SKILLS CLASS IS FUNCTIONING SIMILARLY WITH OTHER CLASSES
    def readSkills(self):
        try:

            if len(self.skills) > 0:
                return self.skills
            else:
                return self.undefined
        except:
            return self._generalError

    def writeSkills(self, skillslist):
        try:
            if len(skillslist) > 0:
                self.skills = skillslist
                return True
            else:
                return False
        except:
            return self._generalError


    def readisValid(self):
        try:
            if len(self.skills) > 0:
                i = 0
                valid = True
                while i < len(self.skills):
                    if not(self.skills[i] in self._lstSkillsAvailable):
                        valid = False
                        return valid
                    else:
                        i = i + 1
                return valid
            else:
                return False
        except:
            return False


    def AddSkill(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self._lstSkillsAvailable:
                self.skills.append(strinput)
                return True
            else:
                return False
        except:
            return False

    #remove a specific skill
    def removeSkill(self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.lstSkillsAvailable:
                self.skills.remove(strinput)
                return True
            else:
                return False
        except:
            return False

    # remove a skill at a certain position
    def removeSkillX(self,x):

        try:

            if ((len(self.lstSkillsAvailable) < x ) and (x >= 0)):
                self.skills.pop(x)
                return True
            else:
                return False
        except:
            return False

    #show all the available skills on the table
    def readSkillsAvailable(self):

        try:

            if len(self._lstSkillsAvailable) > 0:
                return self._lstSkillsAvailable
            else:
                return self.undefined
        except:
            return self._generalError

    #sort the available skills
    def sortSkills(self):


        try:

            if (len(self.lstSkillsAvailable) > 0):
                self.skills.sort()
                return True
            else:
                return False
        except:
            return False

    #edits a skill at a specific position it will overwrite the skill there with the incoming value
    def editSkillX(self, strinput, x):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if ((strinput in self.lstSkillsAvailable) and (x < len(self.lstSkillsAvailable)) and (x >= 0)):
               if (self.lstSkillsAvailable[x] == strinput):
                    self.skills.insert(strinput,x)
                    return True
               else:
                   return False
            else:
                return False
        except:
            return False


    #read teh skill at a specific position and return it
    def readSkillX(self,x):

        try:

            if ((len(self.lstSkillsAvailable) < x) and (x >= 0)):
                temp = self.skills[x]
                return temp
            else:
                return self.undefined
        except:
            return self._generalError