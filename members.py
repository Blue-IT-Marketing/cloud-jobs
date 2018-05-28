

import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from datatypes import Person, Reference, ContactDetails, PhysicalAddress
from ConstantsAndErrorCodes import MyConstants, ErrorCodes, isGoogleServer
from edu import EducationalQualifications, TertiaryQualifications, HighSchoolQualifications, HighSchool
from testcentre import Exam
from accounts import AccountDetails
import logging
from feedback import Feedback
from google.appengine.ext import db
import datetime
from google.appengine.api import users
from google.appengine.api import memcache
import logging

User = Person()
# Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

#WebApp Loader
def doRender(handler, tname='index.html', values={}):
    temp = os.path.join(os.path.dirname(__file__),'templates/' + tname)

    if not os.path.isfile(temp):
        return False

    #make copy of the dictionary and add path
    newval = dict(values)
    newval['path'] = handler.request.path

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True


class MembersAreaHandler (webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        try:


            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    User.clsReference.writeUsername(result.readUsername())
                    User.clsReference.writeReference(result.readReference())
                    User.clsReference.writeIDNumber(result.readIDNumber())
                    User.clsReference.writePassword(result.readPassword())
                    User.clsReference.writeVerEmail(result.readVerEmail())
                    logging.info('Reference Field was Refreshed from DataStore')

                elif result == User._referenceDoNotExist:
                    logging.info('Bad User Account please try login in again if this error persist create a new account')
                    referencemessage = 'Bad User Account please try login in again if this error persist create a new account'
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())

                else:
                    logging.info('Error Loading Account Details user might be logged off')
                    referencemessage = 'Error Loading Account Details user might be logged off'
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())




                result = User.getNamesbyRefNum(reference)

                if not(User._namesPkeyvalue == self.undefined):
                    logging.info('Names Class was Refreshed from Datastore')
                    User.clsNames.writeFirstname(result.readFirstname())
                    User.clsNames.writeSecondname(result.readSecondname())
                    User.clsNames.writeSurname(result.readSurname())
                elif result == self.undefined:
                    logging.info('Names class was not refreshed from datastore')
                    namesmessage ='Names class was not refreshed from datastore'
                else:
                    logging.info('Error Loading Names Details from Datastore')
                    namesmessage = 'Error Loading Names Details from Datastore'


                result = User.getPrivateinfoByRefNum(reference)

                if not(User._privatePkey == self.undefined):
                    logging.info('Private Class was refreshed from Datastore')
                    User.clsPrivate.writeAge(result.readAge())
                    User.clsPrivate.writeCriminalRecord(result.readCriminalRecord())
                    User.clsPrivate.writeDateofBirth(result.readDateof_Birth())
                    User.clsPrivate.writeDependents(result.readDependents())
                    User.clsPrivate.writeEthnicGroup(result.readEthnicGroup())
                    User.clsPrivate.writeGender(result.readGender())
                    User.clsPrivate.writeHomeLanguage(result.readHomeLanguage())
                    User.clsPrivate.writeMarital_Status(result.readMarital_Status())
                    User.clsPrivate.writeNationality(result.readNationality())
                    User.clsPrivate.writePreferredLanguage(result.readPrefferedLanguage())
                elif result == self.undefined:
                    logging.info('Private information was not Refreshed from Datastore')
                    privatemessage=('Private information was not Refreshed from Datastore')
                else:
                    logging.info('Error Loading Private information from datastore')
                    privatemessage=('Error Loading Private information from datastore')



                result = User.getContactDetailsByRefNum(reference)

                if not(User._contactPkey == self.undefined):
                    logging.info('Contact Details was Refreshed from Datastore')
                    User.clsContactDetails.writeBlog(result.readBlog())
                    User.clsContactDetails.writeCell(result.readCell())
                    User.clsContactDetails.writeAboutMe(result.readAboutMe())
                    User.clsContactDetails.writeEmail(result.readEmail())
                    User.clsContactDetails.writeFacebook(result.readFacebook())
                    User.clsContactDetails.writeFax(result.readFax())
                    User.clsContactDetails.writeGooglePlus(result.readGooglePlus())
                    User.clsContactDetails.writeLinkedIn(result.readLinkedIn())
                    User.clsContactDetails.writePinterest(result.readPinterest())
                    User.clsContactDetails.writeSkype(result.readSkype())
                    User.clsContactDetails.writeTel(result.readTel())
                    User.clsContactDetails.writeTwitter(result.readTwitter())
                    User.clsContactDetails.writeWebsite(result.readWebsite())
                    User.clsContactDetails.writeWhosWho(result.readWhosWho())
                elif result == User._referenceDoNotExist:
                    contactmessage = 'The login details supplied might be invalid or you simply need to create a new account'
                    logging.info('Reference Do not Exist')
                else:
                    contactmessage = 'Error Loading Contact Details'
                    logging.info('Error Loading Contact Details from store')


                result = User.getPhysicalAddressByRefnum(reference)

                if not(User._physicalAddressPkey == self.undefined):
                    logging.info('Physical Details was Refreshed from Datastore')
                    User.clsPhysicalAddress.writeCityTown(result.readCityTown())
                    User.clsPhysicalAddress.writeCountry(result.readCountry())
                    User.clsPhysicalAddress.writeStreetName(result.readStreetName())
                    User.clsPhysicalAddress.writePostalZipCode(result.readPostalZipCode())
                    User.clsPhysicalAddress.writeProvinceState(result.readProvinceState())
                    User.clsPhysicalAddress.writeStandNumber(result.readStandNumber())
                elif result == User._referenceDoNotExist:
                    physicalmessage = 'The Login details supplied might be invalid or you simply need to create a new account'
                    logging.info('Reference Do not Exist')
                else:
                    physicalmessage = 'Error loading physical address Details'
                    logging.info('Error loading physical address Details')


                vUsernamed = User.clsReference.readUsername()

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/members.html')

                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                      'vReference': User.clsReference.readReference(),
                                                                      'vEmailAddress': User.clsReference.readVerEmail(),
                                                                      'vFirstname': User.clsNames.readFirstname(),
                                                                      'vSecondname': User.clsNames.readSecondname(),
                                                                      'vSurname': User.clsNames.readSurname(),
                                                                      'vIDNumber': User.clsReference.readIDNumber(),
                                                                      'vNationality': User.clsPrivate.readNationality(),
                                                                      'vCell': User.clsContactDetails.readCell(),
                                                                      'vEmail': User.clsContactDetails.readEmail(),
                                                                      'vFax': User.clsContactDetails.readFax(),
                                                                      'vTel': User.clsContactDetails.readTel(),
                                                                      'vFacebook': User.clsContactDetails.readFacebook(),
                                                                      'vTwitter': User.clsContactDetails.readTwitter(),
                                                                      'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                      'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                      'vPinterest': User.clsContactDetails.readPinterest(),
                                                                      'vSkype': User.clsContactDetails.readSkype(),
                                                                      'vBlog': User.clsContactDetails.readBlog(),
                                                                      'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                      'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                      'vWebsite': User.clsContactDetails.readWebsite(),
                                                                      'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                      'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                      'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                      'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                      'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                      'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                      'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                      'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                      'vGender': User.clsPrivate.readGender(),
                                                                      'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                      'vAge': User.clsPrivate.readAge(),
                                                                      'vDependents': User.clsPrivate.readDependents()}
                self.response.write(template.render(context))
                logging.info('Members Area Render Complete')

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/members.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': 'Please login to access the members Area'}
                self.response.write(template.render(context))


        except:
            doRender(self,'members.html',{'MemberMessage': 'There was an Error accessing your records please try again in a minute'})







    def post(self):

        try:

            Guser = users.get_current_user()

            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode



                if reference == self.request.get('vReferencer'):
                    User.clsReference.writeUsername(self.request.get('vUsernamer'))
                    User.clsReference.writeReference(self.request.get('vReferencer'))
                    User.clsReference.writePassword(self.request.get('vPasswordr'))
                    User.clsReference.writeIDNumber(self.request.get('vIDNumberr'))
                    User.clsReference.writeVerEmail(self.request.get('vEmailAddressr'))

                    result = User.AddReferenceclasstoStore()
                    if result == User._referenceNumConflict:
                        result = User.GetReferenceByRefNum(User.clsReference.readReference()) #looking for the existing reference number in order to obtain teh pkeyvalue
                        if not(User._pkeyvalue == self.undefined):
                            result = User.editReferenceByPkey() #Editing the Reference Class its already on the Store
                            if (result == User._pkeyvalue):
                                refmessage = 'Account Details Updated'
                                logging.info('Account Details Updated')
                            else:
                                refmessage = 'Fail to Update Account Details'
                                logging.info('Fail to Update Account Details')
                        else:
                            refmessage = 'Catastrophic Error trying to update Account Details'
                            logging.info('Catastrophic Error trying to update Account Details')
                    elif result == User._userNameConflict:
                        refmessage = 'Your Username or nickname already exist please create a unique name'
                        logging.info('Your Username or nickname already exist please create a unique name')
                    elif result == False:
                        refmessage = 'Your Account Details are not complete please fill in all the required fields'
                        logging.info('Your Account Details are not complete please fill in all the required fields')
                    else:
                        #The reference Class is successfully created
                        refmessage ='Account Details Created'
                        logging.info('Account Details Created')



                    #We must update vRefMessage to reflect The Message Related to Reference

                    User.clsNames.writeFirstname(self.request.get('vFirstnamer'))
                    User.clsNames.writeSecondname(self.request.get('vSecondnamer'))
                    User.clsNames.writeSurname(self.request.get('vSurnamer'))

                    result = User.getNamesbyRefNum(reference)

                    if result == self.undefined: #names not found meaning i can add new names
                        result = User.addNamesByRefNum(reference)
                        if not(User._namesPkeyvalue == self.undefined):
                            namesmessage ='Your Personal Details have been added'
                            logging.info('Your Personal Details have been added')
                        elif result == self.undefined:
                            namesmessage = 'The login Details supplied might be invalid please create a new account'
                            logging.info('Your Personal Details have been added')
                        else:
                            namesmessage = 'Error Creating a new Personal information record try again in a minute'
                            logging.info('Error Creating a new Personal information record try again in a minute')

                    elif result == User._generalError:
                        namesmessage ='Catastrophic Error Updating Names Details'
                        logging.info('Catastrophic Error Updating Names Details')
                    else:
                        #names have been found meaning they exist then edit them
                        result = User.editNamesbyNamesPkey()
                        namesmessage = 'Your Names record has been Succesfully Updated'
                        logging.info('Your Names record has been Succesfully Updated')




                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to Reference

                    User.clsContactDetails.writeCell(self.request.get('vCellr'))
                    User.clsContactDetails.writeEmail(self.request.get('vEmailr'))
                    User.clsContactDetails.writeFax(self.request.get('vFaxr'))
                    User.clsContactDetails.writeTel(self.request.get('vTelr'))
                    User.clsContactDetails.writeFacebook(self.request.get('vFacebookr'))
                    User.clsContactDetails.writeTwitter(self.request.get('vTwitterr'))
                    User.clsContactDetails.writeLinkedIn(self.request.get('vLinkedinr'))
                    User.clsContactDetails.writeGooglePlus(self.request.get('vGooglePlusr'))
                    User.clsContactDetails.writePinterest(self.request.get('vPinterestr'))
                    User.clsContactDetails.writeSkype(self.request.get(('vSkyper')))
                    User.clsContactDetails.writeBlog(self.request.get('vBlogr'))
                    User.clsContactDetails.writeWhosWho(self.request.get('vWhosWhor'))
                    User.clsContactDetails.writeAboutMe(self.request.get('vAboutMer'))
                    User.clsContactDetails.writeWebsite(self.request.get('vWebsiter'))


                    result = User.getContactDetailsByRefNum(reference)

                    if result == User._referenceDoNotExist:
                        #There's no contact details record for this user a new one must be added from the form
                        contactmessage = 'Catastrophic Error Adding Contact Details'
                        logging.info('Catastrophic Error Adding Contact Details')

                    elif result == self.undefined: #empty list
                        result = User.addContactDetailsByRefNum(reference)
                        if result == self.undefined:
                            contactmessage = 'Error Adding New Contact Details Record'
                            logging.info('Error Adding New Contact Details Record')
                        elif result == User._generalError:
                            contactmessage = 'Catastrophic Error Adding Contact Details'
                            logging.info('Catastrophic Error Adding Contact Details')
                        else:
                            contactmessage = 'Contact Details Record was succesfully Added'
                            logging.info('Contact Details Record was succesfully Added')

                    elif not(User._contactPkey == self.undefined):
                        result = User.editContactDetailsbyPkey()

                        if result == self.undefined:
                            contactmessage = 'Error Editing your Contact Details Record'
                            logging.info('Error Editing your Contact Details Record')
                        elif result == User._generalError:
                            contactmessage = 'Catastrophic Error Editing Contact Details Record'
                            logging.info('Catastrophic Error Editing Contact Details Record')
                        else:
                            contactmessage = 'Contact Details Record Succesfully Edited'
                            logging.info('Contact Details Record Succesfully Edited')
                    else:
                        contactmessage = 'Catastrophic Error Updating Contact Details Record'
                        logging.info('Catastrophic Error Updating Contact Details Record')

                    #We Must Update the vContactMessage to reflect the value of the contactmessage variable
                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to refmessage

                    User.clsPhysicalAddress.writeStandNumber(self.request.get('vStandNumberr'))
                    User.clsPhysicalAddress.writeStreetName(self.request.get('vStreetnamer'))
                    User.clsPhysicalAddress.writeCityTown(self.request.get('vCityTownr'))
                    User.clsPhysicalAddress.writeProvinceState(self.request.get('vProvinceStater'))
                    User.clsPhysicalAddress.writeCountry(self.request.get('vCountryr'))
                    User.clsPhysicalAddress.writePostalZipCode(self.request.get('vPostalZipCoder'))

                    result = User.getPhysicalAddressByRefnum(reference)

                    if result == User._referenceDoNotExist:
                        #User not loggedin or the reference number is not valid logging the info and exit
                        physicalmessage ='Physical Address Record cannot be added you might not be loggedin'
                        logging.info('Physical Address Record cannot be added you might not be loggedin')


                    elif result == self._clsPhysicalDonotExist:
                        result = User.addPhysicalAddressByRefNum(reference)

                        if User._physicalAddressPkey == self.undefined:
                            physicalmessage = 'Error Adding Physical Address Record'
                            logging.info('Error Adding Physical Address Record')
                        else:
                            physicalmessage = 'Physical Address Record has been succesfully added'
                            logging.info('Physical Address Record has been succesfully added')

                    elif result == User._generalError:
                        #Catastrophic Error
                        physicalmessage = 'Catastrophic Error Updating your Physical Address Record'
                        logging.info('Catastrophic Error Updating your Physical Address Record')
                    else:
                        result = User.editPhysicalAddressByPkey()

                        if result == self.undefined:
                            physicalmessage = 'Error Editing your Physical Address Record'
                            logging.info('Error Editing your Physical Address Record')
                        elif result == User._generalError:
                            physicalmessage = 'Catastrophic Error Editing your Physical Address Record'
                            logging.info('Catastrophic Error Editing your Physical Address Record')
                        else:
                            physicalmessage = 'Your Physical Address Record has been edited'
                            logging.info('Your Physical Address Record has been edited')



                    #Update teh vPhysicalMessage to reflecr physicalmessage
                    #We Must Update the vContactMessage to reflect the value of the contactmessage variable
                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to refmessage

                    User.clsPrivate.writePreferredLanguage(self.request.get('vPreferredLanguager'))
                    User.clsPrivate.writeMarital_Status(self.request.get('vMaritalStatusr'))
                    User.clsPrivate.writeGender(self.request.get('vGenderr'))
                    User.clsPrivate.writeDateofBirth(self.request.get('vBirthDater'))
                    User.clsPrivate.writeAge(self.request.get('vAger'))
                    User.clsPrivate.writeDependents(self.request.get('vDependentsr'))
                    User.clsPrivate.writeNationality(self.request.get('vNationalityr'))


                    result = User.getPrivateinfoByRefNum(reference)

                    if User._privatePkey == self.undefined:
                        #Record not found add a new one
                        result = User.addPrivateInfoByReference(reference)
                        if User._privatePkey == self.undefined:
                            privatemessage = 'Error Adding Private Record'
                            logging.info('Error Adding Private Record')
                        elif result == User._generalError:
                            privatemessage = 'Catastrophic Error Adding Private Record'
                            logging.info('Catastrophic Error Adding Private Record')
                        else:
                            privatemessage = 'Private Record Succesfully Added'
                            logging.info('Private Record Succesfully Added')
                    elif result == User._generalError:
                        #Catastrophic Error
                        privatemessage = 'Catastrophic Error with Private Information Record'
                        logging.info('Catastrophic Error with Private Information Record')
                    else:
                        #Record Found Edit it.
                        result = User.editPrivateInfobyPkey()

                        if (result == self.undefined):
                            privatemessage = 'Private Record NOT Succesfully Edited'
                            logging.info('Private Record NOT Succesfully Edited')
                        elif result == User._pkeyNotSet:
                            privatemessage = 'Bad Private Record cannot be edited'
                            logging.info('Bad Private Record cannot be edite')
                        elif result == User._generalError:
                            privatemessage = 'Error Editing Private Information try Again in 1 minute'
                            logging.info('Error Editing Private Information try Again in 1 minute')
                        else:
                            privatemessage = 'Private Information Record Edited Succesfully'
                            logging.info('Private Information Record Edited succesfully')



                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/membersArea.html')

                    context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                      'vPrivateMessage': privatemessage,
                                                                      'vReference': User.clsReference.readReference(),
                                                                      'vEmailAddress': User.clsReference.readVerEmail(),
                                                                      'vFirstname': User.clsNames.readFirstname(),
                                                                      'vSecondname': User.clsNames.readSecondname(),
                                                                      'vSurname': User.clsNames.readSurname(),
                                                                      'vIDNumber': User.clsReference.readIDNumber(),
                                                                      'vNationality': User.clsPrivate.readNationality(),
                                                                      'vCell': User.clsContactDetails.readCell(),
                                                                      'vEmail': User.clsContactDetails.readEmail(),
                                                                      'vFax': User.clsContactDetails.readFax(),
                                                                      'vTel': User.clsContactDetails.readTel(),
                                                                      'vFacebook': User.clsContactDetails.readFacebook(),
                                                                      'vTwitter': User.clsContactDetails.readTwitter(),
                                                                      'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                      'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                      'vPinterest': User.clsContactDetails.readPinterest(),
                                                                      'vSkype': User.clsContactDetails.readSkype(),
                                                                      'vBlog': User.clsContactDetails.readBlog(),
                                                                      'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                      'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                      'vWebsite': User.clsContactDetails.readWebsite(),
                                                                      'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                      'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                      'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                      'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                      'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                      'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                      'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                      'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                      'vGender': User.clsPrivate.readGender(),
                                                                      'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                      'vAge': User.clsPrivate.readAge(),
                                                                      'vDependents': User.clsPrivate.readDependents()}
                    self.response.write(template.render(context))
                    logging.info('Members Area Render Complete')


        except:
            doRender(self,'membersArea.html',{'MemberMessage': 'Error Accessing the Database try again in a minute'})

class ProfilesMainHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        try:


            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    User.clsReference.writeUsername(result.readUsername())
                    User.clsReference.writeReference(result.readReference())
                    User.clsReference.writeIDNumber(result.readIDNumber())
                    User.clsReference.writePassword(result.readPassword())
                    User.clsReference.writeVerEmail(result.readVerEmail())
                    logging.info('Reference Field was Refreshed from DataStore')

                elif result == User._referenceDoNotExist:
                    logging.info('Bad User Account please try login in again if this error persist create a new account')
                    referencemessage = 'Bad User Account please try login in again if this error persist create a new account'
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())

                else:
                    logging.info('Error Loading Account Details user might be logged off')
                    referencemessage = 'Error Loading Account Details user might be logged off'
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())




                result = User.getNamesbyRefNum(reference)

                if not(User._namesPkeyvalue == self.undefined):
                    logging.info('Names Class was Refreshed from Datastore')
                    User.clsNames.writeFirstname(result.readFirstname())
                    User.clsNames.writeSecondname(result.readSecondname())
                    User.clsNames.writeSurname(result.readSurname())
                elif result == self.undefined:
                    logging.info('Names class was not refreshed from datastore')
                    namesmessage ='Names class was not refreshed from datastore'
                else:
                    logging.info('Error Loading Names Details from Datastore')
                    namesmessage = 'Error Loading Names Details from Datastore'




                vUsernamed = User.clsReference.readUsername()

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/MembersProfiles.html')

                #Capitalize Surname
                cSurname = User.clsNames.readSurname()
                cSurname = cSurname.upper()

                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                                                      'vFirstname': User.clsNames.readFirstname(),
                                                                      'vSecondname': User.clsNames.readSecondname(),
                                                                      'vSurname': cSurname}
                self.response.write(template.render(context))
                logging.info('Members Area Render Complete')

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/MembersProfiles.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
                self.response.write(template.render(context))


        except:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/MembersProfiles.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._generalError}
                self.response.write(template.render(context))

    def post(self):


        Guser = users.get_current_user()
        #Complete the profile class in order to write the handler for profiles
        if Guser:
            pass

            # Determine at any time which screen was rendered and get the relevant variables from that screen.
            # process the variables and render the results.
            # if the screen changed also change the display settings class and save to memstore.
class MembersAccountHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/MembersAccount.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/MembersAccount.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/MembersAccount.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))



class MembersAccountSettingsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = str(User._pkeyvalue)

                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]

                    tAccountDetails = AccountDetails.get(tAccountDetails.key())

                    if tAccountDetails.isValid():

                        template = template_env.get_template('/templates/AccountSettings.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vBalance': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/AccountSettings.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/AccountSettings.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/AccountSettings.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/AccountSettings.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))


class MemberVerificationsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                User.clsReference.writeIsUserVerified(result.readIsUserVerified())
                User.clsReference.writeDateTimeVerified(result.readDatetimeVerified())
                User.clsReference.writeLogoPhoto(result.readLogoPhoto())
                User.clsReference.writeIDNumber(result.readIDNumber())
                User.clsReference.writePassword(result.readPassword())
                User.clsReference.writeReference(result.readReference())
                User.clsReference.writeUsername(result.readUsername())
                User.clsReference.writeVerEmail(result.readVerEmail())

                if User.clsReference.readIsUserVerified():
                    EmailNotVerified = 'No'
                else:
                    EmailNotVerified = 'Yes'

                if User.clsReference.readIsCellVerified():
                    SMSNotVerified = 'No'
                else:
                    SMSNotVerified = 'Yes'


                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = User._pkeyvalue
                logging.info(ref)


                findrequest = db.Query(ContactDetails).filter('indexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)
                logging.info('NUMBER OF CONTACTS FOUND:' + str(len(results)))
                if len(results) > 0:
                    tContactDetails = results[0]
                    logging.info('CONTACT DETAILS IS VALID TO CHECK')
                    if tContactDetails.readIsValid():

                        template = template_env.get_template('/templates/verifications.html')
                        logging.info('WE ARE RENDERING THE RIGHT TEMPLATE')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vVerificationTel': tContactDetails.readCell(), 'vVerificationEmail': User.clsReference.readVerEmail(),
                                   'EmailNotVerified': EmailNotVerified, 'SMSNotVerified': SMSNotVerified}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/verifications.html')
                        logging.info('WE ARE RENDERING THE RIGHT TEMPLATE')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vVerificationTel': tContactDetails.readCell(), 'vVerificationEmail': User.clsReference.readVerEmail(),
                                   'SMSNotVerified': SMSNotVerified, 'EmailNotVerified': EmailNotVerified}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/verifications.html')
                    logging.info('WE ARE RENDERING THE RIGHT TEMPLATE')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                               'vVerificationEmail': User.clsReference.readVerEmail(),
                               'SMSNotVerified': SMSNotVerified, 'EmailNotVerified': EmailNotVerified}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/verifications.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/verifications.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))

class MemberServicesSubscriptionsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = str(User._pkeyvalue)

                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]

                    tAccountDetails = AccountDetails.get(tAccountDetails.key())

                    if tAccountDetails.isValid():

                        template = template_env.get_template('/templates/Services.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vBalance': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/Services.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/Services.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/Services.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/Services.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))


class MembersAccountTopUpHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                ref = str(User._pkeyvalue)
                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]
                    if tAccountDetails.isValid():

                        template = template_env.get_template('/templates/TopUp.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vBalance': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/TopUp.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/TopUp.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/TopUp.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/TopUp.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))





    def post(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = str(User._pkeyvalue)

                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]

                    if tAccountDetails.isValid():
                        DepositAmount = self.request.get('vDepositAmountr')
                        PaymentMethod = self.request.get('vPaymentMethodr')

                        if DepositAmount.isdigit():
                            logging.info('DEPOSIT AMOUNT WAS READ: ' + DepositAmount)
                            DepositAmount = int(DepositAmount)
                        else:
                            DepositAmount = 0

                        if PaymentMethod == 'PayPal':
                            logging.info('PAYMENT METHOD PAYPAL')

                        elif PaymentMethod == 'CreditCard':
                            pass
                        else:
                            pass

                        # Payment Method is Direct Deposit
                        # Read The Amount to be deposited
                        # Read the Method to be used
                        # Launch a form with the method
                        # on the form procedurer accept the deposit if its from paypal
                        # and add the deposit to the current balance.
                        # If the method is Direct Deposit (launch a form with the Statement and Reference number to be used
                        # Create an Email Send it to the verified email address with the link to be used to submit the deposit slip.
                        # find out how you can verify deposits. (Suggestions if a deposit slip is sent check the account for the
                        # Current Deposit and see if it was made and then add the amount.)

                        template = template_env.get_template('/templates/TopUp.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vBalance': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/TopUp.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/TopUp.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/TopUp.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/TopUp.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))
class EditAccountDetailsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()
        logging.info('Edit Account Details Called')
        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = str(User._pkeyvalue)
                logging.info('Reference Value found in Edit Account Details. now seacrhing for account details')
                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]

                    tAccountDetails = AccountDetails.get(tAccountDetails.key())

                    if tAccountDetails.isValid():

                        template = template_env.get_template('/templates/EditAccountDetails.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vAccountRef': tAccountDetails.key()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/EditAccountDetails.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/EditAccountDetails.html')
                    logging.info('Launching the default edit account details form to create a new bank account detail')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/EditAccountDetails.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/EditAccountDetails.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))

    def post(self):

        Guser = users.get_current_user()
        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            if not(User._pkeyvalue == self.undefined):
                tAccountDetails = AccountDetails()
                tAccountDetails.writePayPalEmail(self.request.get('vPayPalEmailr'))
                tAccountDetails.writeAccountType(self.request.get('vAccountTyper'))
                tAccountDetails.writeBrachCode(self.request.get('vBranchCoder'))
                tAccountDetails.writeAccountNumber(self.request.get('vAccountNumberr'))
                tAccountDetails.writeNameOfInstitution(self.request.get('vBankNamer'))


                findrequest = db.Query(AccountDetails).filter('IndexReference =', value=str(User._pkeyvalue))
                results = findrequest.fetch(limit=self._maxQResults)
                if len(results) > 0:
                    stAccountDetails = results[0]


                    if stAccountDetails.isValid():
                        stAccountDetails.writeNameOfInstitution(tAccountDetails.readNameOfInstitution())
                        stAccountDetails.writeAccountNumber(tAccountDetails.readAccountNumber())
                        stAccountDetails.writeBrachCode(tAccountDetails.readBranchCode())
                        stAccountDetails.writeAccountType(tAccountDetails.readAccountType())
                        stAccountDetails.writePayPalEmail(tAccountDetails.readPayPalEmail())
                        db.put(stAccountDetails)

                        template = template_env.get_template('/templates/ViewAccountDetails.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': stAccountDetails.readNameOfInstitution(), 'vAccountType': stAccountDetails.readAccountType(),
                                   'vAccountNumber': stAccountDetails.readAccountNumber(), 'vBranchCode': stAccountDetails.readBranchCode(),
                                   'vPayPalEmail': stAccountDetails.readPayPalEmail(), 'vBalance': stAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))

                    else:
                        stAccountDetails.writeInternalBalance('0')
                        stAccountDetails.IndexReference = str(User._pkeyvalue)
                        stAccountDetails.writeNameOfInstitution(tAccountDetails.readNameOfInstitution())
                        stAccountDetails.writeAccountNumber(tAccountDetails.readAccountNumber())
                        stAccountDetails.writeBrachCode(tAccountDetails.readBranchCode())
                        stAccountDetails.writeAccountType(tAccountDetails.readAccountType())
                        stAccountDetails.writePayPalEmail(tAccountDetails.readPayPalEmail())
                        stAccountDetails.put()
                        #Show View Account Details with the Account balance
                        template = template_env.get_template('/templates/ViewAccountDetails.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': stAccountDetails.readNameOfInstitution(), 'vAccountType': stAccountDetails.readAccountType(),
                                   'vAccountNumber': stAccountDetails.readAccountNumber(), 'vBranchCode': stAccountDetails.readBranchCode(),
                                   'vPayPalEmail': stAccountDetails.readPayPalEmail(), 'vBalance': stAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                else:
                        stAccountDetails = AccountDetails()
                        stAccountDetails.writeInternalBalance('0')
                        stAccountDetails.IndexReference = str(User._pkeyvalue)
                        stAccountDetails.writeNameOfInstitution(tAccountDetails.readNameOfInstitution())
                        stAccountDetails.writeAccountNumber(tAccountDetails.readAccountNumber())
                        stAccountDetails.writeBrachCode(tAccountDetails.readBranchCode())
                        stAccountDetails.writeAccountType(tAccountDetails.readAccountType())
                        stAccountDetails.writePayPalEmail(tAccountDetails.readPayPalEmail())
                        stAccountDetails.put()
                        #Show View Account Details with the Account balance
                        template = template_env.get_template('/templates/ViewAccountDetails.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': stAccountDetails.readNameOfInstitution(), 'vAccountType': stAccountDetails.readAccountType(),
                                   'vAccountNumber': stAccountDetails.readAccountNumber(), 'vBranchCode': stAccountDetails.readBranchCode(),
                                   'vPayPalEmail': stAccountDetails.readPayPalEmail(), 'vBalance': stAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
            else:
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/EditAccountDetails.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/EditAccountDetails.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
            self.response.write(template.render(context))


class ViewAccountDetailsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            if not(User._pkeyvalue == self.undefined):
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                ref = str(User._pkeyvalue)

                findrequest = db.Query(AccountDetails).filter('IndexReference =', ref)
                results = findrequest.fetch(limit=self._maxQResults)

                if len(results) > 0:
                    tAccountDetails = results[0]

                    tAccountDetails = AccountDetails.get(tAccountDetails.key())

                    if tAccountDetails.isValid():

                        template = template_env.get_template('/templates/ViewAccountDetails.html')

                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                   'vBankName': tAccountDetails.readNameOfInstitution(), 'vAccountType': tAccountDetails.readAccountType(),
                                   'vAccountNumber': tAccountDetails.readAccountNumber(), 'vBranchCode': tAccountDetails.readBranchCode(),
                                   'vPayPalEmail': tAccountDetails.readPayPalEmail(),
                                   'vBalance': tAccountDetails.readInternalBalance()}
                        self.response.write(template.render(context))
                    else:
                        template = template_env.get_template('/templates/ViewAccountDetails.html')
                        context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                        self.response.write(template.render(context))
                else:
                    template = template_env.get_template('/templates/ViewAccountDetails.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername()}
                    self.response.write(template.render(context))

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')
                User.clsReference.writeUsername(Guser.nickname())
                User.clsReference.writeVerEmail(Guser.email())

                template = template_env.get_template('/templates/ViewAccountDetails.html')

                context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/ViewAccountDetails.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
            self.response.write(template.render(context))


class EditPersonalHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):

        try:


            Guser = users.get_current_user()

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    User.clsReference.writeUsername(result.readUsername())
                    User.clsReference.writeReference(result.readReference())
                    User.clsReference.writeIDNumber(result.readIDNumber())
                    User.clsReference.writePassword(result.readPassword())
                    User.clsReference.writeVerEmail(result.readVerEmail())
                    User.clsReference.writeLogoPhoto(result.readLogoPhoto())
                    User.clsReference.writeIsUserVerified(result.readIsUserVerified())
                    logging.info('Reference Field was Refreshed from DataStore')


                elif result == User._referenceDoNotExist:
                    logging.info(User._referenceDoNotExist)
                    referencemessage = User._referenceDoNotExist
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())


                else:
                    logging.info('Error Loading Account Details user might be logged off')
                    referencemessage = 'Error Loading Account Details user might be logged off'
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())





                result = User.getNamesbyRefNum(reference)

                if not(User._namesPkeyvalue == self.undefined):
                    logging.info('Names Class was Refreshed from Datastore')
                    User.clsNames.writeFirstname(result.readFirstname())
                    User.clsNames.writeSecondname(result.readSecondname())
                    User.clsNames.writeSurname(result.readSurname())
                elif result == self.undefined:
                    logging.info('Names class was not refreshed from datastore')
                    namesmessage ='Names class was not refreshed from datastore'
                else:
                    logging.info('Error Loading Names Details from Datastore')
                    namesmessage = 'Error Loading Names Details from Datastore'


                result = User.getPrivateinfoByRefNum(reference)

                if not(User._privatePkey == self.undefined):
                    logging.info('Private Class was refreshed from Datastore')
                    User.clsPrivate.writeAge(result.readAge())
                    User.clsPrivate.writeCriminalRecord(result.readCriminalRecord())
                    User.clsPrivate.writeDateofBirth(result.readDateof_Birth())
                    User.clsPrivate.writeDependents(result.readDependents())
                    User.clsPrivate.writeEthnicGroup(result.readEthnicGroup())
                    User.clsPrivate.writeGender(result.readGender())
                    User.clsPrivate.writeHomeLanguage(result.readHomeLanguage())
                    User.clsPrivate.writeMarital_Status(result.readMarital_Status())
                    User.clsPrivate.writeNationality(result.readNationality())
                    User.clsPrivate.writePreferredLanguage(result.readPrefferedLanguage())
                elif result == self.undefined:
                    logging.info('Private information was not Refreshed from Datastore')
                    privatemessage=('Private information was not Refreshed from Datastore')
                else:
                    logging.info('Error Loading Private information from datastore')
                    privatemessage=('Error Loading Private information from datastore')



                result = User.getContactDetailsByRefNum(reference)

                if not(User._contactPkey == self.undefined):
                    logging.info('Contact Details was Refreshed from Datastore')
                    User.clsContactDetails.writeBlog(result.readBlog())
                    User.clsContactDetails.writeCell(result.readCell())
                    User.clsContactDetails.writeAboutMe(result.readAboutMe())
                    User.clsContactDetails.writeEmail(result.readEmail())
                    User.clsContactDetails.writeFacebook(result.readFacebook())
                    User.clsContactDetails.writeFax(result.readFax())
                    User.clsContactDetails.writeGooglePlus(result.readGooglePlus())
                    User.clsContactDetails.writeLinkedIn(result.readLinkedIn())
                    User.clsContactDetails.writePinterest(result.readPinterest())
                    User.clsContactDetails.writeSkype(result.readSkype())
                    User.clsContactDetails.writeTel(result.readTel())
                    User.clsContactDetails.writeTwitter(result.readTwitter())
                    User.clsContactDetails.writeWebsite(result.readWebsite())
                    User.clsContactDetails.writeWhosWho(result.readWhosWho())
                elif result == User._referenceDoNotExist:
                    contactmessage = 'The login details supplied might be invalid or you simply need to create a new account'
                    logging.info('Reference Do not Exist')
                else:
                    contactmessage = 'Error Loading Contact Details'
                    logging.info('Error Loading Contact Details from store')


                result = User.getPhysicalAddressByRefnum(reference)

                if not(User._physicalAddressPkey == self.undefined):
                    logging.info('Physical Details was Refreshed from Datastore')
                    User.clsPhysicalAddress.writeCityTown(result.readCityTown())
                    User.clsPhysicalAddress.writeCountry(result.readCountry())
                    User.clsPhysicalAddress.writeStreetName(result.readStreetName())
                    User.clsPhysicalAddress.writePostalZipCode(result.readPostalZipCode())
                    User.clsPhysicalAddress.writeProvinceState(result.readProvinceState())
                    User.clsPhysicalAddress.writeStandNumber(result.readStandNumber())
                elif result == User._referenceDoNotExist:
                    physicalmessage = 'The Login details supplied might be invalid or you simply need to create a new account'
                    logging.info('Reference Do not Exist')
                else:
                    physicalmessage = 'Error loading physical address Details'
                    logging.info('Error loading physical address Details')


                vUsernamed = User.clsReference.readUsername()

                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/EditPersonalDetails.html')
                self.Country_list.sort()
                i = 0
                while i < len(self.Country_list):
                    Country = self.Country_list[i]
                    Country = Country.title()
                    self.Country_list[i] = Country
                    i = i + 1




                context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                      'vReference': User.clsReference.readReference(),
                                                                      'vEmailAddress': User.clsReference.readVerEmail(),
                                                                      'vFirstname': User.clsNames.readFirstname(),
                                                                      'vSecondname': User.clsNames.readSecondname(),
                                                                      'vSurname': User.clsNames.readSurname(),
                                                                      'vIDNumber': User.clsReference.readIDNumber(),
                                                                      'vNationality': User.clsPrivate.readNationality(),
                                                                      'vCell': User.clsContactDetails.readCell(),
                                                                      'vEmail': User.clsContactDetails.readEmail(),
                                                                      'vFax': User.clsContactDetails.readFax(),
                                                                      'vTel': User.clsContactDetails.readTel(),
                                                                      'vFacebook': User.clsContactDetails.readFacebook(),
                                                                      'vTwitter': User.clsContactDetails.readTwitter(),
                                                                      'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                      'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                      'vPinterest': User.clsContactDetails.readPinterest(),
                                                                      'vSkype': User.clsContactDetails.readSkype(),
                                                                      'vBlog': User.clsContactDetails.readBlog(),
                                                                      'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                      'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                      'vWebsite': User.clsContactDetails.readWebsite(),
                                                                      'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                      'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                      'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                      'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                      'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                      'CountryList': self.Country_list,
                                                                      'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                      'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                      'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                      'vGender': User.clsPrivate.readGender(),
                                                                      'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                      'vAge': User.clsPrivate.readAge(),
                                                                      'vDependents': User.clsPrivate.readDependents()}
                self.response.write(template.render(context))
                logging.info('Members Area Render Complete')

            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/EditPersonalDetails.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': 'Please login to access the members Area'}
                self.response.write(template.render(context))


        except:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('/templates/EditPersonalDetails.html')

            context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': 'There was an Error accessing your records please try again in a minute'}
            self.response.write(template.render(context))


    def post(self):

        try:

            Guser = users.get_current_user()

            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode



                if reference == self.request.get('vReferencer'):
                    User.clsReference.writeUsername(self.request.get('vUsernamer'))
                    User.clsReference.writeReference(self.request.get('vReferencer'))
                    User.clsReference.writePassword(self.request.get('vPasswordr'))
                    User.clsReference.writeIDNumber(self.request.get('vIDNumberr'))
                    User.clsReference.writeVerEmail(self.request.get('vEmailAddressr'))

                    result = User.AddReferenceclasstoStore()
                    if result == User._referenceNumConflict:
                        result = User.GetReferenceByRefNum(User.clsReference.readReference()) #looking for the existing reference number in order to obtain teh pkeyvalue
                        if not(User._pkeyvalue == self.undefined):
                            result = User.editReferenceByPkey() #Editing the Reference Class its already on the Store
                            if (result == User._pkeyvalue):
                                refmessage = 'Account Details Updated'
                                logging.info('Account Details Updated')
                            else:
                                refmessage = 'Fail to Update Account Details'
                                logging.info('Fail to Update Account Details')
                        else:
                            refmessage = 'Catastrophic Error trying to update Account Details'
                            logging.info('Catastrophic Error trying to update Account Details')
                    elif result == User._userNameConflict:
                        refmessage = 'Your Username or nickname already exist please create a unique name'
                        logging.info('Your Username or nickname already exist please create a unique name')
                    elif result == False:
                        refmessage = 'Your Account Details are not complete please fill in all the required fields'
                        logging.info('Your Account Details are not complete please fill in all the required fields')
                    else:
                        #The reference Class is succesfully created
                        refmessage ='Account Details Created'
                        logging.info('Account Details Created')



                    #We must update vRefMessage to reflect The Message Related to Reference

                    User.clsNames.writeFirstname(self.request.get('vFirstnamer'))
                    User.clsNames.writeSecondname(self.request.get('vSecondnamer'))
                    User.clsNames.writeSurname(self.request.get('vSurnamer'))

                    result = User.getNamesbyRefNum(reference)

                    if result == self.undefined: #names not found meaning i can add new names
                        result = User.addNamesByRefNum(reference)
                        if not(User._namesPkeyvalue == self.undefined):
                            namesmessage ='Your Personal Details have been added'
                            logging.info('Your Personal Details have been added')
                        elif result == self.undefined:
                            namesmessage = 'The login Details supplied might be invalid please create a new account'
                            logging.info('Your Personal Details have been added')
                        else:
                            namesmessage = 'Error Creating a new Personal information record try again in a minute'
                            logging.info('Error Creating a new Personal information record try again in a minute')

                    elif result == User._generalError:
                        namesmessage ='Catastrophic Error Updating Names Details'
                        logging.info('Catastrophic Error Updating Names Details')
                    else:
                        #names have been found meaning they exist then edit them
                        result = User.editNamesbyNamesPkey()
                        namesmessage = 'Your Names record has been Succesfully Updated'
                        logging.info('Your Names record has been Succesfully Updated')




                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to Reference

                    User.clsContactDetails.writeCell(self.request.get('vCellr'))
                    User.clsContactDetails.writeEmail(self.request.get('vEmailr'))
                    User.clsContactDetails.writeFax(self.request.get('vFaxr'))
                    User.clsContactDetails.writeTel(self.request.get('vTelr'))
                    User.clsContactDetails.writeFacebook(self.request.get('vFacebookr'))
                    User.clsContactDetails.writeTwitter(self.request.get('vTwitterr'))
                    User.clsContactDetails.writeLinkedIn(self.request.get('vLinkedinr'))
                    User.clsContactDetails.writeGooglePlus(self.request.get('vGooglePlusr'))
                    User.clsContactDetails.writePinterest(self.request.get('vPinterestr'))
                    User.clsContactDetails.writeSkype(self.request.get(('vSkyper')))
                    User.clsContactDetails.writeBlog(self.request.get('vBlogr'))
                    User.clsContactDetails.writeWhosWho(self.request.get('vWhosWhor'))
                    User.clsContactDetails.writeAboutMe(self.request.get('vAboutMer'))
                    User.clsContactDetails.writeWebsite(self.request.get('vWebsiter'))


                    result = User.getContactDetailsByRefNum(reference)

                    if result == User._referenceDoNotExist:
                        #There's no contact details record for this user a new one must be added from the form
                        contactmessage = 'Catastrophic Error Adding Contact Details'
                        logging.info('Catastrophic Error Adding Contact Details')

                    elif result == self.undefined: #empty list
                        result = User.addContactDetailsByRefNum(reference)
                        if result == self.undefined:
                            contactmessage = 'Error Adding New Contact Details Record'
                            logging.info('Error Adding New Contact Details Record')
                        elif result == User._generalError:
                            contactmessage = 'Catastrophic Error Adding Contact Details'
                            logging.info('Catastrophic Error Adding Contact Details')
                        else:
                            contactmessage = 'Contact Details Record was succesfully Added'
                            logging.info('Contact Details Record was succesfully Added')

                    elif not(User._contactPkey == self.undefined):
                        result = User.editContactDetailsbyPkey()

                        if result == self.undefined:
                            contactmessage = 'Error Editing your Contact Details Record'
                            logging.info('Error Editing your Contact Details Record')
                        elif result == User._generalError:
                            contactmessage = 'Catastrophic Error Editing Contact Details Record'
                            logging.info('Catastrophic Error Editing Contact Details Record')
                        else:
                            contactmessage = 'Contact Details Record Succesfully Edited'
                            logging.info('Contact Details Record Succesfully Edited')
                    else:
                        contactmessage = 'Catastrophic Error Updating Contact Details Record'
                        logging.info('Catastrophic Error Updating Contact Details Record')

                    #We Must Update the vContactMessage to reflect the value of the contactmessage variable
                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to refmessage

                    User.clsPhysicalAddress.writeStandNumber(self.request.get('vStandNumberr'))
                    User.clsPhysicalAddress.writeStreetName(self.request.get('vStreetnamer'))
                    User.clsPhysicalAddress.writeCityTown(self.request.get('vCityTownr'))
                    User.clsPhysicalAddress.writeProvinceState(self.request.get('vProvinceStater'))
                    User.clsPhysicalAddress.writeCountry(self.request.get('vCountryr'))
                    User.clsPhysicalAddress.writePostalZipCode(self.request.get('vPostalZipCoder'))

                    result = User.getPhysicalAddressByRefnum(reference)

                    if result == User._referenceDoNotExist:
                        #User not loggedin or the reference number is not valid logging the info and exit
                        physicalmessage ='Physical Address Record cannot be added you might not be loggedin'
                        logging.info('Physical Address Record cannot be added you might not be loggedin')


                    elif result == self._clsPhysicalDonotExist:
                        result = User.addPhysicalAddressByRefNum(reference)

                        if User._physicalAddressPkey == self.undefined:
                            physicalmessage = 'Error Adding Physical Address Record'
                            logging.info('Error Adding Physical Address Record')
                        else:
                            physicalmessage = 'Physical Address Record has been succesfully added'
                            logging.info('Physical Address Record has been succesfully added')

                    elif result == User._generalError:
                        #Catastrophic Error
                        physicalmessage = 'Catastrophic Error Updating your Physical Address Record'
                        logging.info('Catastrophic Error Updating your Physical Address Record')
                    else:
                        result = User.editPhysicalAddressByPkey()

                        if result == self.undefined:
                            physicalmessage = 'Error Editing your Physical Address Record'
                            logging.info('Error Editing your Physical Address Record')
                        elif result == User._generalError:
                            physicalmessage = 'Catastrophic Error Editing your Physical Address Record'
                            logging.info('Catastrophic Error Editing your Physical Address Record')
                        else:
                            physicalmessage = 'Your Physical Address Record has been edited'
                            logging.info('Your Physical Address Record has been edited')



                    #Update teh vPhysicalMessage to reflecr physicalmessage
                    #We Must Update the vContactMessage to reflect the value of the contactmessage variable
                    #we must update vNamesMessage to inlcude the namesmessage
                    #We must update vRefMessage to reflect The Message Related to refmessage

                    User.clsPrivate.writePreferredLanguage(self.request.get('vPreferredLanguager'))
                    User.clsPrivate.writeMarital_Status(self.request.get('vMaritalStatusr'))
                    User.clsPrivate.writeGender(self.request.get('vGenderr'))
                    User.clsPrivate.writeDateofBirth(self.request.get('vBirthDater'))
                    User.clsPrivate.writeAge(self.request.get('vAger'))
                    User.clsPrivate.writeDependents(self.request.get('vDependentsr'))
                    User.clsPrivate.writeNationality(self.request.get('vNationalityr'))


                    result = User.getPrivateinfoByRefNum(reference)

                    if User._privatePkey == self.undefined:
                        #Record not found add a new one
                        result = User.addPrivateInfoByReference(reference)
                        if User._privatePkey == self.undefined:
                            privatemessage = 'Error Adding Private Record'
                            logging.info('Error Adding Private Record')
                        elif result == User._generalError:
                            privatemessage = 'Catastrophic Error Adding Private Record'
                            logging.info('Catastrophic Error Adding Private Record')
                        else:
                            privatemessage = 'Private Record Succesfully Added'
                            logging.info('Private Record Succesfully Added')
                    elif result == User._generalError:
                        #Catastrophic Error
                        privatemessage = 'Catastrophic Error with Private Information Record'
                        logging.info('Catastrophic Error with Private Information Record')
                    else:
                        #Record Found Edit it.
                        result = User.editPrivateInfobyPkey()

                        if (result == self.undefined):
                            privatemessage = 'Private Record NOT Succesfully Edited'
                            logging.info('Private Record NOT Succesfully Edited')
                        elif result == User._pkeyNotSet:
                            privatemessage = 'Bad Private Record cannot be edited'
                            logging.info('Bad Private Record cannot be edite')
                        elif result == User._generalError:
                            privatemessage = 'Error Editing Private Information try Again in 1 minute'
                            logging.info('Error Editing Private Information try Again in 1 minute')
                        else:
                            privatemessage = 'Private Information Record Edited Succesfully'
                            logging.info('Private Information Record Edited succesfully')



                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/ViewPersonalDetails.html')

                    context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                      'vPrivateMessage': privatemessage,
                                                                      'vReference': User.clsReference.readReference(),
                                                                      'vEmailAddress': User.clsReference.readVerEmail(),
                                                                      'vFirstname': User.clsNames.readFirstname(),
                                                                      'vSecondname': User.clsNames.readSecondname(),
                                                                      'vSurname': User.clsNames.readSurname(),
                                                                      'vIDNumber': User.clsReference.readIDNumber(),
                                                                      'vNationality': User.clsPrivate.readNationality(),
                                                                      'vCell': User.clsContactDetails.readCell(),
                                                                      'vEmail': User.clsContactDetails.readEmail(),
                                                                      'vFax': User.clsContactDetails.readFax(),
                                                                      'vTel': User.clsContactDetails.readTel(),
                                                                      'vFacebook': User.clsContactDetails.readFacebook(),
                                                                      'vTwitter': User.clsContactDetails.readTwitter(),
                                                                      'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                      'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                      'vPinterest': User.clsContactDetails.readPinterest(),
                                                                      'vSkype': User.clsContactDetails.readSkype(),
                                                                      'vBlog': User.clsContactDetails.readBlog(),
                                                                      'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                      'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                      'vWebsite': User.clsContactDetails.readWebsite(),
                                                                      'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                      'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                      'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                      'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                      'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                      'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                      'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                      'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                      'vGender': User.clsPrivate.readGender(),
                                                                      'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                      'vAge': User.clsPrivate.readAge(),
                                                                      'vDependents': User.clsPrivate.readDependents()}
                    self.response.write(template.render(context))
                    logging.info('Members Area Render Complete')


        except:
            doRender(self,'ViewPersonalDetails.html',{'MemberMessage': 'Error Accessing the Database try again in a minute'})

class ViewPersonalDetails(webapp2.RequestHandler, MyConstants, ErrorCodes):

        def get(self):

            try:


                Guser = users.get_current_user()

                if Guser:
                    if isGoogleServer:
                        reference = Guser.user_id()
                    else:
                        reference = self._tempCode


                    User.clsReference.writeReference(reference)
                    result = User.GetReferenceByRefNum(reference)

                    if not(User._pkeyvalue == self.undefined):
                        User.clsReference.writeUsername(result.readUsername())
                        User.clsReference.writeReference(result.readReference())
                        User.clsReference.writeIDNumber(result.readIDNumber())
                        User.clsReference.writePassword(result.readPassword())
                        User.clsReference.writeVerEmail(result.readVerEmail())
                        logging.info('Reference Field was Refreshed from DataStore')

                    elif result == User._referenceDoNotExist:
                        logging.info('Bad User Account please try login in again if this error persist create a new account')
                        referencemessage = 'Bad User Account please try login in again if this error persist create a new account'
                        User.clsReference.writeUsername(Guser.nickname())
                        User.clsReference.writeVerEmail(Guser.email())

                    else:
                        logging.info('Error Loading Account Details user might be logged off')
                        referencemessage = 'Error Loading Account Details user might be logged off'
                        User.clsReference.writeUsername(Guser.nickname())
                        User.clsReference.writeVerEmail(Guser.email())




                    result = User.getNamesbyRefNum(reference)

                    if not(User._namesPkeyvalue == self.undefined):
                        logging.info('Names Class was Refreshed from Datastore')
                        User.clsNames.writeFirstname(result.readFirstname())
                        User.clsNames.writeSecondname(result.readSecondname())
                        User.clsNames.writeSurname(result.readSurname())
                    elif result == self.undefined:
                        logging.info('Names class was not refreshed from datastore')
                        namesmessage ='Names class was not refreshed from datastore'
                    else:
                        logging.info('Error Loading Names Details from Datastore')
                        namesmessage = 'Error Loading Names Details from Datastore'


                    result = User.getPrivateinfoByRefNum(reference)

                    if not(User._privatePkey == self.undefined):
                        logging.info('Private Class was refreshed from Datastore')
                        User.clsPrivate.writeAge(result.readAge())
                        User.clsPrivate.writeCriminalRecord(result.readCriminalRecord())
                        User.clsPrivate.writeDateofBirth(result.readDateof_Birth())
                        User.clsPrivate.writeDependents(result.readDependents())
                        User.clsPrivate.writeEthnicGroup(result.readEthnicGroup())
                        User.clsPrivate.writeGender(result.readGender())
                        User.clsPrivate.writeHomeLanguage(result.readHomeLanguage())
                        User.clsPrivate.writeMarital_Status(result.readMarital_Status())
                        User.clsPrivate.writeNationality(result.readNationality())
                        User.clsPrivate.writePreferredLanguage(result.readPrefferedLanguage())
                    elif result == self.undefined:
                        logging.info('Private information was not Refreshed from Datastore')
                        privatemessage=('Private information was not Refreshed from Datastore')
                    else:
                        logging.info('Error Loading Private information from datastore')
                        privatemessage=('Error Loading Private information from datastore')



                    result = User.getContactDetailsByRefNum(reference)

                    if not(User._contactPkey == self.undefined):
                        logging.info('Contact Details was Refreshed from Datastore')
                        User.clsContactDetails.writeBlog(result.readBlog())
                        User.clsContactDetails.writeCell(result.readCell())
                        User.clsContactDetails.writeAboutMe(result.readAboutMe())
                        User.clsContactDetails.writeEmail(result.readEmail())
                        User.clsContactDetails.writeFacebook(result.readFacebook())
                        User.clsContactDetails.writeFax(result.readFax())
                        User.clsContactDetails.writeGooglePlus(result.readGooglePlus())
                        User.clsContactDetails.writeLinkedIn(result.readLinkedIn())
                        User.clsContactDetails.writePinterest(result.readPinterest())
                        User.clsContactDetails.writeSkype(result.readSkype())
                        User.clsContactDetails.writeTel(result.readTel())
                        User.clsContactDetails.writeTwitter(result.readTwitter())
                        User.clsContactDetails.writeWebsite(result.readWebsite())
                        User.clsContactDetails.writeWhosWho(result.readWhosWho())
                    elif result == User._referenceDoNotExist:
                        contactmessage = 'The login details supplied might be invalid or you simply need to create a new account'
                        logging.info('Reference Do not Exist')
                    else:
                        contactmessage = 'Error Loading Contact Details'
                        logging.info('Error Loading Contact Details from store')


                    result = User.getPhysicalAddressByRefnum(reference)

                    if not(User._physicalAddressPkey == self.undefined):
                        logging.info('Physical Details was Refreshed from Datastore')
                        User.clsPhysicalAddress.writeCityTown(result.readCityTown())
                        User.clsPhysicalAddress.writeCountry(result.readCountry())
                        User.clsPhysicalAddress.writeStreetName(result.readStreetName())
                        User.clsPhysicalAddress.writePostalZipCode(result.readPostalZipCode())
                        User.clsPhysicalAddress.writeProvinceState(result.readProvinceState())
                        User.clsPhysicalAddress.writeStandNumber(result.readStandNumber())
                    elif result == User._referenceDoNotExist:
                        physicalmessage = 'The Login details supplied might be invalid or you simply need to create a new account'
                        logging.info('Reference Do not Exist')
                    else:
                        physicalmessage = 'Error loading physical address Details'
                        logging.info('Error loading physical address Details')


                    vUsernamed = User.clsReference.readUsername()

                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/ViewPersonalDetails.html')

                    context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                          'vReference': User.clsReference.readReference(),
                                                                          'vEmailAddress': User.clsReference.readVerEmail(),
                                                                          'vFirstname': User.clsNames.readFirstname(),
                                                                          'vSecondname': User.clsNames.readSecondname(),
                                                                          'vSurname': User.clsNames.readSurname(),
                                                                          'vIDNumber': User.clsReference.readIDNumber(),
                                                                          'vNationality': User.clsPrivate.readNationality(),
                                                                          'vCell': User.clsContactDetails.readCell(),
                                                                          'vEmail': User.clsContactDetails.readEmail(),
                                                                          'vFax': User.clsContactDetails.readFax(),
                                                                          'vTel': User.clsContactDetails.readTel(),
                                                                          'vFacebook': User.clsContactDetails.readFacebook(),
                                                                          'vTwitter': User.clsContactDetails.readTwitter(),
                                                                          'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                          'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                          'vPinterest': User.clsContactDetails.readPinterest(),
                                                                          'vSkype': User.clsContactDetails.readSkype(),
                                                                          'vBlog': User.clsContactDetails.readBlog(),
                                                                          'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                          'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                          'vWebsite': User.clsContactDetails.readWebsite(),
                                                                          'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                          'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                          'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                          'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                          'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                          'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                          'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                          'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                          'vGender': User.clsPrivate.readGender(),
                                                                          'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                          'vAge': User.clsPrivate.readAge(),
                                                                          'vDependents': User.clsPrivate.readDependents()}
                    self.response.write(template.render(context))
                    logging.info('Members Area Render Complete')

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/ViewPersonalDetails.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': 'Please login to access the members Area'}
                    self.response.write(template.render(context))


            except:
                doRender(self, 'ViewPersonalDetails.html', {'MemberMessage': 'There was an Error accessing your records please try again in a minute'})


        def post(self):

            try:


                Guser = users.get_current_user()

                if Guser:
                    if isGoogleServer:
                        reference = Guser.user_id()
                    else:
                        reference = self._tempCode




                    User.clsReference.writeReference(reference)

                    result = User.GetReferenceByRefNum(reference)

                    if not(User._pkeyvalue == self.undefined):
                        User.clsReference.writeUsername(result.readUsername())
                        User.clsReference.writeReference(result.readReference())
                        User.clsReference.writeIDNumber(result.readIDNumber())
                        User.clsReference.writePassword(result.readPassword())
                        User.clsReference.writeVerEmail(result.readVerEmail())
                        logging.info('Reference Field was Refreshed from DataStore')

                    elif result == User._referenceDoNotExist:
                        logging.info('Bad User Account please try login in again if this error persist create a new account')
                        referencemessage = 'Bad User Account please try login in again if this error persist create a new account'
                        User.clsReference.writeUsername(Guser.nickname())
                        User.clsReference.writeVerEmail(Guser.email())

                    else:
                        logging.info('Error Loading Account Details user might be logged off')
                        referencemessage = 'Error Loading Account Details user might be logged off'
                        User.clsReference.writeUsername(Guser.nickname())
                        User.clsReference.writeVerEmail(Guser.email())




                    result = User.getNamesbyRefNum(reference)

                    if not(User._namesPkeyvalue == self.undefined):
                        logging.info('Names Class was Refreshed from Datastore')
                        User.clsNames.writeFirstname(result.readFirstname())
                        User.clsNames.writeSecondname(result.readSecondname())
                        User.clsNames.writeSurname(result.readSurname())
                    elif result == self.undefined:
                        logging.info('Names class was not refreshed from datastore')
                        namesmessage ='Names class was not refreshed from datastore'
                    else:
                        logging.info('Error Loading Names Details from Datastore')
                        namesmessage = 'Error Loading Names Details from Datastore'


                    result = User.getPrivateinfoByRefNum(reference)

                    if not(User._privatePkey == self.undefined):
                        logging.info('Private Class was refreshed from Datastore')
                        User.clsPrivate.writeAge(result.readAge())
                        User.clsPrivate.writeCriminalRecord(result.readCriminalRecord())
                        User.clsPrivate.writeDateofBirth(result.readDateof_Birth())
                        User.clsPrivate.writeDependents(result.readDependents())
                        User.clsPrivate.writeEthnicGroup(result.readEthnicGroup())
                        User.clsPrivate.writeGender(result.readGender())
                        User.clsPrivate.writeHomeLanguage(result.readHomeLanguage())
                        User.clsPrivate.writeMarital_Status(result.readMarital_Status())
                        User.clsPrivate.writeNationality(result.readNationality())
                        User.clsPrivate.writePreferredLanguage(result.readPrefferedLanguage())
                    elif result == self.undefined:
                        logging.info('Private information was not Refreshed from Datastore')
                        privatemessage=('Private information was not Refreshed from Datastore')
                    else:
                        logging.info('Error Loading Private information from datastore')
                        privatemessage=('Error Loading Private information from datastore')



                    result = User.getContactDetailsByRefNum(reference)

                    if not(User._contactPkey == self.undefined):
                        logging.info('Contact Details was Refreshed from Datastore')
                        User.clsContactDetails.writeBlog(result.readBlog())
                        User.clsContactDetails.writeCell(result.readCell())
                        User.clsContactDetails.writeAboutMe(result.readAboutMe())
                        User.clsContactDetails.writeEmail(result.readEmail())
                        User.clsContactDetails.writeFacebook(result.readFacebook())
                        User.clsContactDetails.writeFax(result.readFax())
                        User.clsContactDetails.writeGooglePlus(result.readGooglePlus())
                        User.clsContactDetails.writeLinkedIn(result.readLinkedIn())
                        User.clsContactDetails.writePinterest(result.readPinterest())
                        User.clsContactDetails.writeSkype(result.readSkype())
                        User.clsContactDetails.writeTel(result.readTel())
                        User.clsContactDetails.writeTwitter(result.readTwitter())
                        User.clsContactDetails.writeWebsite(result.readWebsite())
                        User.clsContactDetails.writeWhosWho(result.readWhosWho())
                    elif result == User._referenceDoNotExist:
                        contactmessage = 'The login details supplied might be invalid or you simply need to create a new account'
                        logging.info('Reference Do not Exist')
                    else:
                        contactmessage = 'Error Loading Contact Details'
                        logging.info('Error Loading Contact Details from store')


                    result = User.getPhysicalAddressByRefnum(reference)

                    if not(User._physicalAddressPkey == self.undefined):
                        logging.info('Physical Details was Refreshed from Datastore')
                        User.clsPhysicalAddress.writeCityTown(result.readCityTown())
                        User.clsPhysicalAddress.writeCountry(result.readCountry())
                        User.clsPhysicalAddress.writeStreetName(result.readStreetName())
                        User.clsPhysicalAddress.writePostalZipCode(result.readPostalZipCode())
                        User.clsPhysicalAddress.writeProvinceState(result.readProvinceState())
                        User.clsPhysicalAddress.writeStandNumber(result.readStandNumber())
                    elif result == User._referenceDoNotExist:
                        physicalmessage = 'The Login details supplied might be invalid or you simply need to create a new account'
                        logging.info('Reference Do not Exist')
                    else:
                        physicalmessage = 'Error loading physical address Details'
                        logging.info('Error loading physical address Details')


                    vUsernamed = User.clsReference.readUsername()

                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/ViewPersonalDetails.html')

                    context = {'vUsername': User.clsReference.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'vPassword': User.clsReference.readPassword(),
                                                                          'vReference': User.clsReference.readReference(),
                                                                          'vEmailAddress': User.clsReference.readVerEmail(),
                                                                          'vFirstname': User.clsNames.readFirstname(),
                                                                          'vSecondname': User.clsNames.readSecondname(),
                                                                          'vSurname': User.clsNames.readSurname(),
                                                                          'vIDNumber': User.clsReference.readIDNumber(),
                                                                          'vNationality': User.clsPrivate.readNationality(),
                                                                          'vCell': User.clsContactDetails.readCell(),
                                                                          'vEmail': User.clsContactDetails.readEmail(),
                                                                          'vFax': User.clsContactDetails.readFax(),
                                                                          'vTel': User.clsContactDetails.readTel(),
                                                                          'vFacebook': User.clsContactDetails.readFacebook(),
                                                                          'vTwitter': User.clsContactDetails.readTwitter(),
                                                                          'vLinkedin': User.clsContactDetails.readLinkedIn(),
                                                                          'vGooglePlus': User.clsContactDetails.readGooglePlus(),
                                                                          'vPinterest': User.clsContactDetails.readPinterest(),
                                                                          'vSkype': User.clsContactDetails.readSkype(),
                                                                          'vBlog': User.clsContactDetails.readBlog(),
                                                                          'vWhosWho': User.clsContactDetails.readWhosWho(),
                                                                          'vAboutMe': User.clsContactDetails.readAboutMe(),
                                                                          'vWebsite': User.clsContactDetails.readWebsite(),
                                                                          'vStandNumber': User.clsPhysicalAddress.readStandNumber(),
                                                                          'vStreetname': User.clsPhysicalAddress.readStreetName(),
                                                                          'vCityTown': User.clsPhysicalAddress.readCityTown(),
                                                                          'vProvinceState': User.clsPhysicalAddress.readProvinceState(),
                                                                          'vCountry': User.clsPhysicalAddress.readCountry(),
                                                                          'vPostalZipCode': User.clsPhysicalAddress.readPostalZipCode(),
                                                                          'vPreferredLanguage': User.clsPrivate.readPrefferedLanguage(),
                                                                          'vMaritalStatus': User.clsPrivate.readMarital_Status(),
                                                                          'vGender': User.clsPrivate.readGender(),
                                                                          'vBirthDate': User.clsPrivate.readDateof_Birth(),
                                                                          'vAge': User.clsPrivate.readAge(),
                                                                          'vDependents': User.clsPrivate.readDependents()}
                    self.response.write(template.render(context))
                    logging.info('Members Area Render Complete')

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')

                    template = template_env.get_template('/templates/ViewPersonalDetails.html')

                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': 'Please login to access the members Area'}
                    self.response.write(template.render(context))


            except:
                doRender(self, 'ViewPersonalDetails.html', {'MemberMessage': 'There was an Error accessing your records please try again in a minute'})

class ViewEducationalDetailsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):

        try:

            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/ViewEducationDetails.html')
            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)
                UNames = User.getNamesbyRefNum(reference)
                if not(User._pkeyvalue == self.undefined):
                    logging.info('REFERENCE WAS FOUND:')

                    findrequest = db.Query(HighSchoolQualifications).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=self._maxQResults)

                    if len(results) > 0:
                        logging.info('HIGH SCHOOL FOUND:')
                        tHighSchoolQual = results[0]
                    else:
                        logging.info('HIGH SCHOOL WAS NOT FOUND:')
                        tHighSchoolQual = HighSchoolQualifications()


                    findrequest = db.Query(TertiaryQualifications).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        logging.info('TERTIARY FOUND:')
                        tTertiary = results[0]
                    else:
                        logging.info('TERTIARY WAS NOT FOUND:')
                        tTertiary = TertiaryQualifications()

                    tHighSchool = tHighSchoolQual.RetrieveHighSchool()


                    if not(tHighSchool == self.undefined) and not(tHighSchool == self._generalError):

                        tHighSchoolPhysicalAdd = tHighSchool.retrievePhysicalAddress()

                        if not(tHighSchoolPhysicalAdd == self.undefined) and not(tHighSchoolPhysicalAdd == self._clsPhysicalDonotExist) and not(tHighSchoolPhysicalAdd == self._generalError):
                            context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                       'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail(),
                                       'vSchoolNamer':tHighSchool.readSchoolName(), 'vSPAStreetName': tHighSchoolPhysicalAdd.readStreetName(),
                                       'vSPAStreetNumber': tHighSchoolPhysicalAdd.readStandNumber(), 'vSPACityTown': tHighSchoolPhysicalAdd.readCityTown(),
                                       'vSPAProvinceState': tHighSchoolPhysicalAdd.readProvinceState(), 'vSPACountryr': tHighSchoolPhysicalAdd.readCountry(),
                                       'vSPAPostalZIPCode': tHighSchoolPhysicalAdd.readPostalZipCode(), 'vSPAHighestGrade': tHighSchoolQual.readHighestGradePassed(),
                                       'vSPAYearPassed': tHighSchoolQual.readYearPassed(),'vSPASubjectPassed': tHighSchoolQual.readSubjectsPassed()}
                            self.response.write(template.render(context))
                        else:
                            context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                       'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail(),
                                       'vSchoolNamer':tHighSchool.readSchoolName(), 'vSPAStreetName': tHighSchoolPhysicalAdd.readStreetName(),
                                       'vSPAStreetNumber': tHighSchoolPhysicalAdd.readStandNumber(), 'vSPAHighestGrade': tHighSchoolQual.readHighestGradePassed(),
                                       'vSPAYearPassed': tHighSchoolQual.readYearPassed(),'vSPASubjectPassed': tHighSchoolQual.readSubjectsPassed()}
                            self.response.write(template.render(context))

                    else:
                        context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                   'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail()}
                        self.response.write(template.render(context))



                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured


    def post(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        doRender(self,'ViewEducationDetails.html', {'loginURL': login_url, 'logoutURL': logout_url})

class EditEducationalDetailsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):

    def get(self):
        try:
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/EditEducationDetails.html')
            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)
                UNames = User.getNamesbyRefNum(reference)
                if not(User._pkeyvalue == self.undefined):
                    logging.info('REFERENCE WAS FOUND:')
                    findrequest = db.Query(HighSchoolQualifications).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        logging.info('HIGH SCHOOL WAS NOT FOUND:')
                        tHighSchoolQual = results[0]
                    else:
                        logging.info('HIGH SCHOOL NOT FOUND:')
                        tHighSchoolQual = HighSchoolQualifications()

                    findrequest = db.Query(TertiaryQualifications).filter('indexReference =', User._pkeyvalue)
                    results = findrequest.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        logging.info('TERTIARY FOUND:')
                        tTertiary = results[0]
                    else:
                        logging.info('TERTIARY WAS NOT FOUND:')
                        tTertiary = TertiaryQualifications()

                    tHighSchool = tHighSchoolQual.RetrieveHighSchool()


                    if not(tHighSchool == self.undefined) and not(tHighSchool == self._generalError):

                        tHighSchoolPhysicalAdd = tHighSchool.retrievePhysicalAddress()

                        if not(tHighSchoolPhysicalAdd == self.undefined) and not(tHighSchoolPhysicalAdd == self._clsPhysicalDonotExist) and not(tHighSchoolPhysicalAdd == self._generalError):
                            context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                       'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail(),
                                       'vSchoolNamer':tHighSchool.readSchoolName(), 'vSPAStreetName': tHighSchoolPhysicalAdd.readStreetName(),
                                       'vSPAStreetNumber': tHighSchoolPhysicalAdd.readStandNumber(), 'vSPACityTown': tHighSchoolPhysicalAdd.readCityTown(),
                                       'vSPAProvinceState': tHighSchoolPhysicalAdd.readProvinceState(), 'vSPACountryr': tHighSchoolPhysicalAdd.readCountry(),
                                       'vSPAPostalZIPCode': tHighSchoolPhysicalAdd.readPostalZipCode(), 'vSPAHighestGrade': tHighSchoolQual.readHighestGradePassed(),
                                       'vSPAYearPassed': tHighSchoolQual.readYearPassed(),'vSPASubjectPassed': tHighSchoolQual.readSubjectsPassed()}
                            self.response.write(template.render(context))
                        else:
                            context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                       'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail(),
                                       'vSchoolNamer':tHighSchool.readSchoolName(), 'vSPAStreetName': tHighSchoolPhysicalAdd.readStreetName(),
                                       'vSPAStreetNumber': tHighSchoolPhysicalAdd.readStandNumber(), 'vSPAHighestGrade': tHighSchoolQual.readHighestGradePassed(),
                                       'vSPAYearPassed': tHighSchoolQual.readYearPassed(),'vSPASubjectPassed': tHighSchoolQual.readSubjectsPassed()}
                            self.response.write(template.render(context))

                    else:
                        context = {'vUsername':UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                                   'vFirstname':UNames.readFirstname(), 'vSecondname': UNames.readSecondname(), 'vSurname': UNames.readSurname(),
                                       'vPassword': UReference.readPassword(), 'vEmailAddress': UReference.readVerEmail()}
                        self.response.write(template.render(context))



                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured


    def post(self):
        try:
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')
            template = template_env.get_template('/templates/EditEducationDetails.html')
            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)
                UNames = User.getNamesbyRefNum(reference)
                if not(User._pkeyvalue == self.undefined):
                    tHighSchool = HighSchool()
                    tHighSchool.writeSchoolName(strinput=self.request.get('vSchoolNamer'))
                    tHighSchoolPAdrress = PhysicalAddress()
                    tHighSchoolPAdrress.writeStreetName(strinput=self.request.get('vSPAStreetNamer'))
                    tHighSchoolPAdrress.writeStandNumber(strinput=self.request.get('vSPAStreetNumberr'))
                    tHighSchoolPAdrress.writeCityTown(strinput=self.request.get('vSPACityTownr'))
                    tHighSchoolPAdrress.writeProvinceState(strinput=self.request.get('vSPAProvinceStater'))
                    tHighSchoolPAdrress.writeCountry(strinput=self.request.get('vSPACountryr'))
                    tHighSchoolPAdrress.writePostalZipCode(strinput=self.request.get('vSPAPostalZIPCoder'))
                    tHPAkey = tHighSchoolPAdrress.put()
                    tHighSchool.writePhysicalAddress(strinput=tHPAkey)
                    tHighSchoolQual = HighSchoolQualifications()
                    tHighSchoolQual.writeHighestGradePassed(self.request.get('vSPAHighestGrader'))
                    tHighSchoolQual.writeYearPassed(self.request.get('vSPAYearPassedr'))
                    tHSIkey = tHighSchool.put()
                    tHighSchoolPAdrress.indexReference = tHSIkey
                    tHighSchoolPAdrress.put()
                    tHighSchoolQual.writeHighSchoolIndex(strinput=tHSIkey)
                    tHighSchoolQual.writeOwnerIndex(strinput=User._pkeyvalue)
                    tHSQkey = tHighSchoolQual.put()
        except:
            pass

class ViewSkillsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        template = template_env.get_template('/templates/ViewSkills.html')

        try:

            Guser = users.get_current_user()

            if Guser:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    context = {'vUsername': UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))


                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured

    def post(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        template = template_env.get_template('/templates/ViewSkills.html')

        try:

            Guser = users.get_current_user()

            if Guser:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    context = {'vUsername': UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))


                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured
class EditSkillsHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        template = template_env.get_template('/templates/EditSkills.html')

        try:

            Guser = users.get_current_user()

            if Guser:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    context = {'vUsername': UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))


                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured
    def post(self):
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')

        template = template_env.get_template('/templates/EditSkills.html')

        try:

            Guser = users.get_current_user()

            if Guser:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                UReference = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    context = {'vUsername': UReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))


                else:
                    pass
                    # USer Reference not valid
            else:
                pass
                # User not logged in
        except:
            pass
            # Error Occured

class TestCentreMainHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode




                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                if not(User._pkeyvalue == self.undefined):
                    findrequest = db.Query(Exam).filter('strTestKind =', 'freelancer')
                    results = findrequest.fetch(limit=self._maxExams)
                    if len(results) > 0:
                        ExamsList = results
                    else:
                        ExamsList = []

                    template = template_env.get_template('/templates/TestCentre.html')
                    context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                               'ExamsList': ExamsList}
                    self.response.write(template.render(context))

                else:
                    login_url = users.create_login_url(self.request.path)
                    logout_url = users.create_logout_url(dest_url='/')
                    User.clsReference.writeUsername(Guser.nickname())
                    User.clsReference.writeVerEmail(Guser.email())

                    template = template_env.get_template('/templates/TestCentre.html')

                    context = {'vUsername': User.clsReference.readUsername(),'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._clsReferenceDonotExist}
                    self.response.write(template.render(context))
            else:
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/TestCentre.html')

                context = {'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': self._userNotLoggedin}
                self.response.write(template.render(context))


class TestCentreCreatorHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):

        Guser = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(dest_url='/')
        if Guser:
            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            TestReference = self.request.get('vTestReferencer')
            TestName = self.request.get('vTestNamer')
            TestLevel =self.request.get('vTestLevelr')
            TestKind = self.request.get('vTestKindr')
            Question = self.request.get('vQuestionr')
            Answer1 = self.request.get('vAnswer1r')
            Answer2 = self.request.get('vAnswer2r')
            Answer3 = self.request.get('vAnswer3r')
            Answer4 = self.request.get('vAnswer4r')
            RightAnswer = self.request.get('vRightAnswerr')

            Uref = User.GetReferenceByRefNum(reference)
            template = template_env.get_template('templates/admin.html')

            if not(TestReference == self.undefined):
                Ptest = Exam.get(TestReference)
                findrequest = db.Query(Exam)
                results = findrequest.fetch(limit=self._maxExams)
                if len(results) > 0:
                    ExamList = results
                else:
                    ExamList = []

                if (Ptest.readTestName() == TestName) and (Ptest.readTestLevel() == TestLevel) and (Ptest.readTestKind() == TestKind):
                       if Ptest.CreateQuestion(inQuestion=Question, inAnswer1=Answer1, inAnswer2=Answer2, inAnswer3=Answer3, inAnswer4=Answer4, inRightAnswer=RightAnswer):
                           Ptest.put()
                           context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                      'vTestReference': TestReference, 'vTestName': TestName, 'vTestLevel': TestLevel,
                                      'TestsList': ExamList}
            else:
                Ptest = Exam()
                Ptest.CreateExam(inTestName=TestName, inTestLevel=TestLevel, inTestCode=Ptest.CreateTestCode(), inTestKind='freelancer')
                Ptest.put()
                findrequest = db.Query(Exam)
                results = findrequest.fetch(limit=self._maxExams)
                if len(results) > 0:
                    ExamList = results
                else:
                    ExamList = []
                TestReference = Ptest.key()
                TestName = Ptest.readTestName()
                TestLevel = Ptest.readTestLevel()
                context = {'vUsername': Uref.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url,
                                      'vTestReference': TestReference, 'vTestName': TestName, 'vTestLevel': TestLevel,
                                      'TestsList': ExamList}
            self.response.write(template.render(context))
        else: # This event will never occur
            pass
class VerificationEmailHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):

        try:
            Guser = users.get_current_user()

            if Guser:

                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode

                User.clsReference.writeReference(reference)

                result = User.GetReferenceByRefNum(reference)

                vEmail = self.undefined
                vEmail = self.request.get('vVerificationEmairl')
                logging.info(vEmail)

                namesResult = User.getNamesbyRefNum(reference)


                if not(User._pkeyvalue == self.undefined) and not(User._namesPkeyvalue == self.undefined):
                    User.clsReference.writeVerEmail(result.readVerEmail())
                    User.clsReference.writeDateTimeVerified(result.readDatetimeVerified())
                    User.clsReference.writeUsername(result.readUsername())
                    User.clsReference.writeReference(result.readReference())
                    User.clsReference.writePassword(result.readPassword())
                    User.clsReference.writeIDNumber(result.readIDNumber())
                    User.clsReference.writeLogoPhoto(result.readLogoPhoto())
                    User.clsReference.writeIsUserVerified(result.readIsUserVerified())
                    User.clsReference.EmailVerCode = result.EmailVerCode

                    User.clsNames.writeFirstname(namesResult.readFirstname())
                    User.clsNames.writeSecondname(namesResult.readSecondname())
                    User.clsNames.writeSurname(namesResult.readSurname())
                    User.clsNames.writeTitle(namesResult.readTitle())
                    User.clsNames.writeInitials(namesResult.readInitials())

                    if result.readVerEmail() == vEmail: #  Verification email is valid

                        logging.info(result.readVerEmail())
                        if not(vEmail == self.undefined):
                            logging.info('INSIDE VERIFICATION EMAIL')

                            tofielder = User.clsNames.readFirstname() + " " + User.clsNames.readSurname() + " " + "<" + User.clsReference.readVerEmail() + ">"
                            logging.info(tofielder)
                            senderField = "freelancing-solutions@appspot.gserviceaccount.com  Verifications <freelancing-solutions@appspot.gserviceaccount.com>"

                            SubjectField = "Verify Account Freelancing Solutions"
                            IntroField = "Dear " + User.clsNames.readFirstname()
                            BodyField = IntroField + """:
                             your Freelancing Solutions Email Verification Code is
                             :"""
                            VerificationCode = result.CreateEmailVerCode()
                            logging.info(VerificationCode)
                            if not(VerificationCode == self.undefined):
                                BodyField = BodyField + VerificationCode
                            else:
                                BodyField = BodyField + "Error Creating Verification Code Please try Again Later"

                            BodyField = BodyField + """

                                                        Please Enter the verification Code now on the opened window
                                                        The Freelancing Solutions Team"""
                            mail.send_mail(sender=senderField,
                              to=tofielder,
                              subject=SubjectField,
                            body=BodyField)
                            result.put() #Saving the Present Verification Code
                            login_url = users.create_login_url(self.request.path)
                            logout_url = users.create_logout_url(dest_url='/')
                            template = template_env.get_template('/templates/verify.html')
                            VerifyEmail = 'Yes'

                            context = {'loginURL': login_url, 'logoutURL': logout_url, 'vUsername': result.readUsername(),
                                       'VerifyEmail': VerifyEmail}
                            self.response.write(template.render(context))

        except:
            return self.undefined

class ActualEmailVerification(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def post(self):
        Guser = users.get_current_user()

        if Guser:

            if isGoogleServer:
                reference = Guser.user_id()
            else:
                reference = self._tempCode

            User.clsReference.writeReference(reference)

            result = User.GetReferenceByRefNum(reference)

            namesResult = User.getNamesbyRefNum(reference)

            VeryCode = self.request.get('vEnterEmailCode')
            logging.info(VeryCode)
            logging.info(result.readEmailVerCode())

            if (VeryCode == result.readEmailVerCode()) and not(result.EmailVerCode == self.undefined) and not(VeryCode == '00000000'):
                result.writeIsUserVerified(True)
                VerifiedTime = datetime.datetime.now()
                result.writeDateTimeVerified(VerifiedTime)
                result.put()
                MemberMessage = self._EmailSuccesfullyVerified
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/verify.html')

                context = {'vUsername': result.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage}
                self.response.write(template.render(context))
            else:
                MemberMessage = self._VerificationCodeIncorrect
                login_url = users.create_login_url(self.request.path)
                logout_url = users.create_logout_url(dest_url='/')

                template = template_env.get_template('/templates/verify.html')

                context = {'vUsername': result.readUsername(), 'loginURL': login_url, 'logoutURL': logout_url, 'MemberMessage': MemberMessage}
                self.response.write(template.render(context))

class adminHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        try:
            Guser = users.get_current_user()
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            if Guser:
                if isGoogleServer:
                    reference = Guser.user_id()
                else:
                    reference = self._tempCode
                Uref = User.GetReferenceByRefNum(reference)
                tFeedback = Feedback()

                if users.is_current_user_admin():
                    findrequest = db.Query(Exam)
                    results = findrequest.fetch(limit=self._maxExams)
                    if len(results) > 0:
                        ExamLists = results
                    else:
                        ExamLists = []
                    findrequest = db.Query(Feedback).filter('CustomerSatisfied =', False)
                    results = findrequest.fetch(limit=self._maxQResults)
                    if len(results) > 0:
                        FeedbackList = results
                    else:
                        FeedbackList = []

                    if not(User._pkeyvalue == self.undefined):
                        template = template_env.get_template('templates/admin.html')
                        context = {'vUsername': Uref.readUsername(),'loginURL': login_url, 'logoutURL': logout_url,
                               'TestsList': ExamLists, 'FeedbackList': FeedbackList}
                        self.response.write(template.render(context))
                    else:
                        pass  # This event will never occur
                else:  # The User is not administrator we render the home page
                    template = template_env.get_template('templates/index.html')
                    context = {'vUsername': Uref.readUsername(),'loginURL': login_url, 'logoutURL': logout_url}
                    self.response.write(template.render(context))
            else: # Render The Home Page Again
                template = template_env.get_template('templates/index.html')
                context = {'loginURL': login_url, 'logoutURL': logout_url}
                self.response.write(template.render(context))
        except:
            login_url = users.create_login_url(self.request.path)
            logout_url = users.create_logout_url(dest_url='/')

            template = template_env.get_template('templates/index.html')
            context = {'loginURL': login_url, 'logoutURL': logout_url}
            self.response.write(template.render(context))

app = webapp2.WSGIApplication([('/members', MembersAreaHandler),
                               ('/membersProfiles', ProfilesMainHandler),
                               ('/membersAccount', MembersAccountHandler),
                               ('/membersAccountSettings', MembersAccountSettingsHandler),
                               ('/membersVerifications', MemberVerificationsHandler),
                               ('/membersServices', MemberServicesSubscriptionsHandler),
                               ('/membersAccountTopup',  MembersAccountTopUpHandler),
                               ('/EditAccountDetails', EditAccountDetailsHandler),
                               ('/ViewAccountDetails', ViewAccountDetailsHandler),
                                ('/EditPersonalDetails', EditPersonalHandler),
                               ('/ViewPersonalDetails', ViewPersonalDetails),
                               ('/ViewEducationalDetails', ViewEducationalDetailsHandler),
                               ('/EditEducationalDetails', EditEducationalDetailsHandler),
                               ('/VerificationEmail', VerificationEmailHandler),
                               ('/EmailVerifications', ActualEmailVerification),
                               ('/membersAdmin', adminHandler),
                               ('/ViewSkills', ViewSkillsHandler),
                               ('/EditSkills', EditSkillsHandler),
                               ('/TestCentre', TestCentreMainHandler),
                               ('/TestCentreCreate', TestCentreCreatorHandler),], debug=True)


