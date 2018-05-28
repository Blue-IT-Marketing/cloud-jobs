__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'

import os
import webapp2
import jinja2
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from google.appengine.ext import db
from datatypes import Reference, Person
from google.appengine.api import mail
import logging
from google.appengine.api import users
User = Person()
# Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

scripts = '''
        <link href="http://freelancing-solutions.freelancing-seo.com/jQueryAssets/jquery.ui.core.min.css" rel="stylesheet" type="text/css">
        <link href="http://freelancing-solutions.freelancing-seo.com/jQueryAssets/jquery.ui.theme.min.css" rel="stylesheet" type="text/css">
        <link href="http://freelancing-solutions.freelancing-seo.com/jQueryAssets/jquery.ui.tabs.min.css" rel="stylesheet" type="text/css">


		<script src="http://freelancing-solutions.freelancing-seo.com/js/jquery.min.js"></script>
		<script src="http://freelancing-solutions.freelancing-seo.com/js/config.js"></script>
		<script src="http://freelancing-solutions.freelancing-seo.com/js/skel.min.js"></script>
		<script src="http://freelancing-solutions.freelancing-seo.com/js/skel-panels.min.js"></script>
	<noscript>
			<link rel="stylesheet" href="http://freelancing-solutions.freelancing-seo.com/css/skel-noscript.css" />
			<link rel="stylesheet" href="http://freelancing-solutions.freelancing-seo.com/css/style.css" />
			<link rel="stylesheet" href="http://freelancing-solutions.freelancing-seo.com/css/style-desktop.css" />
	</noscript>
'''

news1 = '''

<h1>Welcome to Freelancing Solutions NewsLetters</h1>
<p>This news letters are designed to introduce you to Freelancing Solutions several Services and products
 Designed to allow you to make use of the Internet to make money Actively and Passively depending on
  your Skills and Preferences</p>
<a href="http://jobcloud.freelancing-seo.com/NewsletterIntroduction">This is an introduction to our NewsLetters for more information please click here</a>
'''
sub1 = 'Introduces you to Freelancing Solutions NewsLetters'
news2 = ""
news3 = ""
news4 = ""

_newsLetterBodies = [news1, news2, news3, news4]
class Newsletter(db.Expando, MyConstants, ErrorCodes):
    _confirmCodes = ['a', 's', 'd', 'r', '5', '6', '4', '8', '9', 'w', 'k,', 'j', 'h', 'U', 'U', 'H', 'L', '6', 's', 'd',
                      'a', 'o', 's', 'i',
                     'j', 'n', 'n', 'f', 'k', 'g', 'd', 'n', 'f', 'k', 'i', '8', '0', 'n', 'j', 'n', 'd', 'f', 's', 'o', 'd', '2', 'f', 'i', 'r',
                     'n', 'g', 'n', 'r', 'e', 's', '1', 'n', 'g', 'f', 'd', 'm', 's', 'n', 'g', 'f', 'd', 's', 'e', 'r', '9', '8', '9', '8', '7',
                     '9', '8', '7', '9', 's', '8', 'd', 'f', 's', 'd', 'j', 'f', 'h', 'k', 's', 'j', 'e', 'h', 'r', 'w', 'i', 'u', 'h', '3', 'i',
                     '4', '5', '3', '7', '4', '6', '8', '7', '4', '6', '8', '5', '3', 'y', 's', 'b', 'd', 'b', 's', 'd', 'b']
    _maxConfirmCodeLen = 12
    EmailAddress = db.EmailProperty(indexed=True)
    Firstname = db.StringProperty()
    ConfirmCode = db.StringProperty()
    Confirmed = db.BooleanProperty(default=False)
    NewsletterNumber = db.IntegerProperty(default=0)
    NewsletterSent = db.BooleanProperty(default=False)


    def SetNewsletterSent(self):
        self.NewsletterSent = True
        return True
    def ResetNewsletterSent(self):
        self.NewsletterSent = False
        return True

    def readNewsletterNumber(self):
        temp = int(self.NewsletterNumber)
        return temp


    def getSubject(self):
        tSubject = self.Firstname + sub1
        return tSubject

    def getBody(self):
        tBody = _newsLetterBodies[self.readNewsletterNumber()]
        self.NewsletterNumber = self.NewsletterNumber + 1
        return tBody


    def sendNewsLetter(self):
        try:
            message = mail.EmailMessage()
            message.sender = self._AppEmail
            message.to = self.EmailAddress
            message.subject = self.getSubject()
            message.body = self.getBody()
            message.send()
            return True
        except:
            return self._generalError


    def writeEmail(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.EmailAddress = strinput
                return True
            else:
                self.EmailAddress = self.undefined
                return False
        except:
            return self._generalError

    def readEmail(self):
        try:
            temp = str(self.EmailAddress)
            temp = temp.strip()

            if not(temp == self.undefined):
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeFirstname(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput.isalpha():
                self.Firstname = strinput
                return True
            else:
                self.Firstname = self.undefined
                return False
        except:
            return self._generalError



    def readFirstname(self):
        try:
            temp = str(self.Firstname)
            temp = temp.strip()
            temp = temp.lower()

            if temp.isalpha():
                return temp
            else:
                return self.undefined
        except:
            return self._generalError

    # First Create Confirmation Code and store it on the class
    # then send it with the email to the user
    def readCofirmCode(self):
        try:
            return self.ConfirmCode
        except:
            return self._generalError

    def writeConfirmCode(self, strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if (strinput.isalpha() or strinput.isalnum()):
                self.ConfirmCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def CreateConfirmCode(self):
        try:
            tkey = self.put()
            tkey = str(tkey)
            self.ConfirmCode = tkey[(len(tkey) - self._maxConfirmCodeLen): (len(tkey) - 1) ]
            return self.ConfirmCode
        except:
            return self._generalError




    def sendConfirmation(self):
        try:

            self.writeConfirmCode(self.CreateConfirmCode())
            ConfirmCode = self.readCofirmCode()
            self.put() # Saving back teh confirm code to the datastore


            message = mail.EmailMessage()
            message.sender = self._AppEmail
            message.to = self.readEmail()
            message.subject = 'Activate your Freelancing Solutions Newsletter Subscriptions'
            message.body = 'Dear ' + self.readFirstname() + """
            Your Newsletter Subscription request was received and you only need to copy and paste the verification
            code below on our website,
            The Activation Code is: """ + ConfirmCode + """
            Thank you
            Freelancing Solutions Team"""

            message.send()
            return True
        except:
            return self._generalError




    def writeConfirm(self, bolinput):
        try:
            if bolinput == True:
                self.Confirmed = True
                return True
            elif bolinput == False:
                self.Confirmed = False
                return True
        except:
            return self._generalError

    def readConfirm(self):
        try:
            return self.Confirmed
        except:
            return self._generalError

class UserNewsLetter(Newsletter):
    indexReference = db.ReferenceProperty(Reference, collection_name='newsletter')


class NewsletterHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def post(self):

        try:
            NewsL = Newsletter()
            Firstname = self.request.get('vFirstname')
            NEmail = self.request.get('VerEmail')

            if NewsL.writeFirstname(Firstname) and NewsL.writeEmail(NEmail):
                findrequest = db.Query(Newsletter).filter('EmailAddress =', NEmail)
                results = findrequest.fetch(limit=1)
                if len(results) == 0:
                    if not(NewsL.sendConfirmation() == self._generalError):
                        NewsL.put()
                    else:  # i have to repeat the sending of confirmation and saving if the process failed
                        NewsL.sendConfirmation()
                        NewsL.put()


                    Guser = users.get_current_user()

                    if Guser:
                        reference = Guser.user_id()
                    else:
                        reference = self._tempCode


                    UReference = User.GetReferenceByRefNum(reference)

                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    if not(User._pkeyvalue == self.undefined):
                        template = template_env.get_template('/templates/NewsletterVer.html')
                        context = {'vUsername': UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'Success': 'Yes',
                                   'vEmail': NewsL.readEmail(),
                                   'Verified': 'No'}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/NewsletterVer.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'Success': 'Yes',
                                   'vEmail': NewsL.readEmail(), 'Verified': 'No'}
                        self.response.write(template.render(context))


                else:
                    Guser = users.get_current_user()

                    if Guser:
                        reference = Guser.user_id()
                    else:
                        reference = self._tempCode


                    UReference = User.GetReferenceByRefNum(reference)

                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    Newsl = results[0]
                    tVerified = Newsl.readConfirm()

                    if not(tVerified == self._generalError):
                        Verified = tVerified
                    else:
                        tVerified = Newsl.readConfirm()
                        if not(tVerified == self._generalError):
                            Verified = tVerified
                        else:
                            Verified = False

                    if Verified == True:
                        Verified = 'Yes'
                    else:
                        Verified = 'No'

                    if not(User._pkeyvalue == self.undefined):
                        template = template_env.get_template('/templates/NewsletterVer.html')
                        context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'vEmail': Newsl.readEmail(),'Verified': Verified}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/NewsletterVer.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url,'vEmail': Newsl.readEmail(),
                                   'Verified': Verified}
                        self.response.write(template.render(context))
        except:
            pass

class NewsLetterVerHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def post(self):
        try:
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            UrefOk = False
            UseNick = False
            Notloggedon = False
            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    UrefOk = True

                else:

                    UseNick = True


            else:

                Notloggedon = True




            tNewsL = Newsletter()
            tNewsL.writeEmail(self.request.get('vEmailr'))

            findreqest = db.Query(Newsletter).filter('EmailAddress =', tNewsL.readEmail())
            results = findreqest.fetch(limit=self._maxQResults)

            template = template_env.get_template('/templates/NewsletterVer.html')

            if len(results) > 0:
                Newsl = results[0]

                if Newsl.readCofirmCode() == self.request.get('vVerificationCoder'):
                    Confirmed = True
                    rConfirm = Newsl.writeConfirm(Confirmed)
                    if not(rConfirm == self._generalError):
                        Newsl.put()
                    else:
                        Newsl.writeConfirm(Confirmed)
                        Newsl.put()

                    if UrefOk:
                        context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'Yes', 'vEmail': Newsl.readEmail(), 'vFirstname': Newsl.readFirstname()}
                    elif UseNick:
                        context = {'vUsername': Guser.nickname(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'Yes',  'vEmail': Newsl.readEmail(), 'vFirstname': Newsl.readFirstname()}
                    elif Notloggedon:
                        context = {'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'Yes',  'vEmail': Newsl.readEmail(), 'vFirstname': Newsl.readFirstname()}
                else:
                    if UrefOk:
                        context = {'vUsername': UReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'No'}
                    elif UseNick:
                        context = {'vUsername': Guser.nickname(), 'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'No'}
                    elif Notloggedon:
                        context = {'loginURL': login_url, 'logoutURL': logout_url,
                                   'Verified': 'No'}
                self.response.write(template.render(context))

            else:
                pass
        except:
            pass
class NewsLetterImport(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        pass

app = webapp2.WSGIApplication([('/newsletter', NewsletterHandler),
                               ('/NewsletterVer', NewsLetterVerHandler),
                               ('/NewsletterImport', NewsLetterImport)], debug=True)
