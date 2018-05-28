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
################################################## FUNCTIONS AND UNIT FOR TESTING USERS  ###############################
########################################################################################################################
########################################################################################################################

from ConstantsAndErrorCodes import MyConstants, ErrorCodes
from google.appengine.ext import db

"""
FORMAT FOR TESTCENTRE

QUESTION
ANSWER1
ANSWER2
ANSWER3
ANSWER4

[RIGHT ANSWER] [ 1 --> 4]
YOUR ANSWER (MUST MATCH RIGHT ANSWER)


We can load the test questions by making use of the blostore to upload a file with the questions and answers ub the
format above once verified the test will then be offered online.

"""
# Used for exam logic and courses and tests for different subjects
# The Question and Answers Actual questions will be checked by the administrators once uploaded to make sure that they
# are correct.
class MultiChoice(db.Expando, MyConstants, ErrorCodes):
    _answersChoice = [1, 2, 3, 4]
    question = db.StringProperty(multiline=True)
    answer1 = db.StringProperty(multiline=True)
    answer2 = db.StringProperty(multiline=True)
    answer3 = db.StringProperty(multiline=True)
    answer4 = db.StringProperty(multiline=True)
    rightanswer = db.StringProperty(default=_answersChoice[0])  # The choices will be selected from the _answersChoice constant.
    youranswer = db.StringProperty(default='5')  # The answer the person taking the exam choosed 5 means not answered.

    def readQuestion(self):
        try:
            if not(self.question == self.undefined):
                return self.question
            else:
                return self.undefined
        except:
            return self._generalError


    def writeQuestion(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.question = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readAnswer1(self):
        try:
            if not(self.answer1 == self.undefined):
                return self.answer1
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAnswer1(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.answer1 = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readAnswer2(self):
        try:
            if not(self.answer2 == self.undefined):
                return self.answer2
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAnswer2(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.answer2 = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readAnswer3(self):
        try:
            if not(self.answer3 == self.undefined):
                return self.answer3
            else:
                return self.undefined
        except:
            return self._generalError


    def writeAnswer3(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.answer3 = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readAnswer4(self):
        try:
            if not(self.answer4 == self.undefined):
                return self.answer4
            else:
                return self.undefined
        except:
            return self._generalError


    def writeAnswer4(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.answer4 = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readRightAnswer(self):
        try:
            if not(self.rightanswer == self.undefined):
                return self.rightanswer
            else:
                return self.undefined
        except:
            return self._generalError

    def writeRightAnswer(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.rightanswer = strinput
                return True
            else:
                return False
        except:
            return self._generalError


    def readYourAnswer(self):
        try:
            if not(self.youranswer == self.undefined):
                return self.youranswer
            else:
                return self.undefined
        except:
            return self._generalError

    def writeYourAnswer(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput == self.undefined):
                self.youranswer = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def checkAnswer(self):
        try:
            if self.readYourAnswer() == self.readRightAnswer():
                return True
            else:
                return False
        except:
            return self._generalError

class Exam(db.Expando, MyConstants, ErrorCodes):
    Testname = db.StringProperty()
    TestLevel = db.StringProperty()
    TestCode = db.StringProperty(indexed=True)
    _TestKind = ['interview', 'freelancer']
    strTestKind = db.StringProperty(default=_TestKind[1])  # freelancer
    Questions = db.ListProperty(item_type=str)  # This string list stores the indexes of the multiple choice questions and answers
    def writeTestName(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.Testname = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readTestName(self):
        try:
            temp = str(self.Testname)
            temp = temp.strip()

            if not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError
    def readTestKind(self):
        try:
            temp = str(self.strTestKind)
            temp = temp.strip()

            if temp in self._TestKind:
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeTestKind(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput in self._TestKind:
                self.strTestKind = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def writeTestLevel(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.TestLevel = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readTestLevel(self):
        try:
            temp = str(self.TestLevel)
            temp = temp.strip()

            if not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeTestCode(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.TestCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readTestCode(self):
        try:
            temp = str(self.TestCode)
            temp = temp.strip()

            if not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def CreateTestCode(self):
        pass

    def CreateQuestion(self, inQuestion, inAnswer1, inAnswer2, inAnswer3, inAnswer4, inRightAnswer):
        try:
            TempMulti = MultiChoice()
            if TempMulti.writeQuestion(inQuestion) and TempMulti.writeAnswer1(inAnswer1) and \
            TempMulti.writeAnswer2(inAnswer2) and TempMulti.writeAnswer3(inAnswer3) and \
            TempMulti.writeAnswer4(inAnswer4) and TempMulti.writeRightAnswer(inRightAnswer):
                tempKey = TempMulti.put()
                self.Questions.append(tempKey)
                return True
            else:
                return False
        except:
            return self._generalError


    def CreateExam(self, inTestName, inTestLevel, inTestCode, inTestKind):
        try:
            if self.writeTestName(inTestName) and self.writeTestLevel(inTestLevel) and self.writeTestCode(inTestCode) and self.writeTestKind(inTestKind):
                return True
            else:
                return False
        except:
            return self._generalError





#Todo- Create procedures to deal with Exams and Exam Creation

class TestCentre(db.Expando, MyConstants, ErrorCodes):
    Tests = Exam()


# Used to store User Marks on each course and test
class TestResults(db.Expando, MyConstants, ErrorCodes):
    pass

