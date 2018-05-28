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

from google.appengine.api import mail
from google.appengine.ext import db
import logging
import datetime
undefined = None
#TODO-include currency symbol for each country and their timezone information
class Util ():

    Max_Chars = 256
    First_Upper_Char = 65
    Last_Upper_Char  = 91
    First_Lower_Char = 97
    Last_Lower_Char  = 122
    First_Number_Char = 48
    Last_Number_Char = 57

    #Special Characters
    Space_Bar = ' '
    Full_Stop = '.'
    Collon    = ':'
    SemiCollon =';'
    Comma     = ','
    At        = '@'
    doubleQuote = '"'
    singleQuote = "'"
    Special_Chars = (Space_Bar, Full_Stop, Collon, SemiCollon, Comma,At)
    #Important URLS
    http      = 'http://www.'
    https     = 'https://www.'

    #Countries and Provinces
    # Provinces of South Africa
    Gauteng = 'gauteng'
    Limpopo = 'limpopo'
    Mpumalanga = 'mpumalanga'
    Northwest = 'north west'
    FreeState = 'free state'
    KwazuluNatal = 'kwazulu natal'
    EasternCape = 'eastern cape'
    NorthernCape = 'northern cape'
    WesternCape = 'western cape'

    South_African_Provinces = (Gauteng, Limpopo, Mpumalanga, Northwest, FreeState, KwazuluNatal, EasternCape, NorthernCape, WesternCape)

    # Countries of Africa
    morocco       = 'morocco'
    mauritania    = 'mauritania'
    senegal       = 'senegal'
    TheGambia     = 'the gambia'
    Guinea        = 'guinea'
    sierraleone   = 'sierra leone'
    liberia       = 'liberia'
    ivorycoast    = 'ivory coast'
    ghana         = 'ghana'
    togo          = 'togo'
    benin         = 'benin'
    nigeria       = 'nigeria'
    burkinafaso   = 'burkina faso'
    mali          = 'mali'
    niger         = 'niger'
    algeria       = 'algeria'
    tunisia       = 'tunisia'
    libya         = 'libya'
    egypt         = 'egypt'
    chad                      = 'chad'
    cameroon                  = 'cameroon'
    equatorialguinea          = 'equatorial guinea'
    gabon                     = 'gabon'
    republicofthecongo        = 'republic of the congo'
    centralafricanrepublic    = 'central african republic'
    sudan                     = 'sudan'
    uganda                    = 'uganda'
    rwanda                    = 'rwanda'
    burundi                   = 'burundi'
    demrepofthecongo          = 'democratic republic of the congo'
    angola                    = 'angola'
    namibia                   = 'namibia'
    southafrica               = 'south africa'
    lesotho                   = 'lesotho'
    swaziland                 = 'swaziland'
    botswana                  = 'botswana'
    zimbabwe                  = 'zimbabwe'
    zambia                    = 'zambia'
    malawi                    = 'malawi'
    mozambique                = 'mozambique'
    madagascar                = 'madagascar'
    comoros                   = 'comoros'
    tanzania                  = 'tanzania'
    kenya                     = 'kenya'
    ethiopia                  = 'ethiopia'
    somalia                   = 'somalia'
    djibouti                  = 'djibouti'
    eritrea                   = 'eritrea'
    guineabissau              = 'guinea-bissau'
    capeverde                 = 'cape verde'
    seychelles                = 'seychelles'
    mauritias                 = 'mauritias'
    saotomeandprincipe        = 'saotome and principe'

    Countries_Of_Africa = (morocco, mauritania, senegal, TheGambia, Guinea, sierraleone,
    liberia, ivorycoast, ghana, togo, benin, nigeria, burkinafaso, mali, niger, algeria,
    tunisia, libya, egypt, chad, cameroon, equatorialguinea, gabon, republicofthecongo, centralafricanrepublic, sudan,
    uganda, rwanda, burundi, demrepofthecongo, angola, namibia, southafrica, lesotho,
    swaziland, botswana, zimbabwe, zambia, malawi, mozambique, madagascar, comoros,
    tanzania, kenya, ethiopia, somalia, djibouti, eritrea, guineabissau, capeverde, seychelles,
    mauritias, saotomeandprincipe)


    UnitedStatesOfAmerica     = 'united states of america'
    canada                    = 'canada'
    mexico                    = 'mexico'

    #States of America

    Alabama                     = 'alabama'
    Alaska                      = 'alaska'
    Arizona                     = 'arizona'
    Arkansas                    = 'arkansas'
    California                  = 'california'
    Colorado                    = 'colorado'
    Connecticut                 = 'connecticut'
    Delaware                    = 'delaware'
    DistrictofColumbia          = 'district of colombia'
    Florida                     = 'florida'
    Georgia                     = 'georgia'
    Hawaii                      = 'hawaii'
    Idaho                       = 'idaho'
    Illinois                    = 'illinois'
    Indiana                     = 'indiana'
    Iowa                        = 'iowa'
    Kansas                      = 'kansas'
    Kentucky                    = 'kentucky'
    Louisiana                   = 'louisiana'
    Maine                       = 'maine'
    Maryland                    = 'maryland'
    Massachusetts               = 'massachusetts'
    Michigan                    = 'michigan'
    Minnesota                   = 'minnesota'
    Mississippi                 = 'mississippi'
    Missouri                    = 'missouri'
    Montana                     = 'montana'
    Nebraska                    = 'nebraska'
    Nevada                      = 'nevada'
    NewHampshire                = 'new hampshire'
    NewJersey                   = 'new jersey'
    NewMexico                   = 'new mexico'
    NewYork                     = 'new york'
    NorthCarolina               = 'north carolina'
    NorthDakota                 = 'north dakota'
    Ohio                        = 'ohio'
    Oklahoma                    = 'oklahoma'
    Oregon                      = 'oregon'
    Pennsylvania                = 'pennsylvania'
    RhodeIsland                 = 'rhode island'
    SouthCarolina               = 'south carolina'
    SouthDakota                 = 'south dakota'
    Tennessee                   = 'tennessee'
    Texas                       = 'texas'
    Utah                        = 'utah'
    Vermont                     = 'vermont'
    Virginia                    = 'virginia'
    Washington                  = 'washington'
    WestVirginia                = 'west virginia'
    Wisconsin                   = 'winsconsin'
    Wyoming                     = 'wyoming'

    USA_States = (Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, DistrictofColumbia,
                  Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland,
                    Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, NewHampshire,
                    NewJersey, NewMexico, NewYork, NorthCarolina, NorthDakota, Ohio, Oklahoma, Oregon, Pennsylvania, RhodeIsland,
                    SouthCarolina, SouthDakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, WestVirginia, Wisconsin,
                    Wyoming)



    #Europian Countries
    portugal                    = 'portugal'
    spain                       = 'spain'
    france                      = 'france'
    switzerland                 = 'switzerland'
    italy                       = 'italy'
    slovenia                    = 'slovenia'
    croatia                     = 'croatia'
    bosniaandherzegovina        = 'bosnia and herzegovina'
    serbia                      = 'serbia'
    macedonia                   = 'macedonia'
    albania                     = 'albania'
    greece                      = 'greece'
    bulgaria                    = 'bulgaria'
    romania                     = 'romania'
    moldova                     = 'moldova'
    hungary                     = 'hungary'
    austria                     = 'austria'
    czechrepublic               = 'czech republic'
    germany                     = 'germany'
    belgium                     = 'belgium'
    netherlands                 = 'netherlands'
    unitedkingdom               = 'united kingdom'
    ireland                     = 'ireland'
    iceland                     = 'iceland'
    norway                      = 'norway'
    denmark                     = 'denmark'
    sweden                      = 'sweden'
    finland                     = 'finland'
    estonia                     = 'estonia'
    latvia                      = 'latvia'
    lithuania                   = 'lithuania'
    poland                      = 'poland'
    belarus                     = 'belarus'
    ukraine                     = 'ukraine'
    russia                      = 'russia'
    slovakia                    = 'slovakia'
    andorra                     = 'andorra'
    monaco                      = 'monaco'
    vaticancity                 = 'vatican city'
    sanmarino                   = 'san marino'
    luxembourgh                 = 'luxembourgh'
    liechenstein                = 'liechenstein'
    malta                       = 'malta'
    montenegro                  = 'montenegro'

    European_Countries = (portugal, spain, france, switzerland, italy, slovenia, croatia, bosniaandherzegovina, serbia,
    macedonia, albania, greece, bulgaria, romania, moldova, hungary, austria, czechrepublic, germany, belgium, netherlands,
    unitedkingdom, ireland, iceland, norway, denmark, sweden, finland, estonia, latvia, lithuania, poland, belarus, ukraine,
    russia, slovakia, andorra, monaco, vaticancity, sanmarino, luxembourgh, liechenstein, malta, montenegro)


    #Asian Countries
    lebanon                     = 'lebanon'
    israel                      = 'israel'
    cyprus                      = 'cyprus'
    jordan                      = 'jordan'
    syria                       = 'syria'
    iraq                        = 'iraq'
    kuwait                      = 'kuwait'
    saudiarabia                 = 'saudi arabia'
    bahrain                     = 'bahrain'
    qatar                       = 'qatar'
    yemen                       = 'yemen'
    oman                        = 'oman'
    unitedarabemirates          = 'united arab emirates'
    iran                        = 'iran'
    azerbaijan                  = 'azerbaijan'
    armenia                     = 'armenia'
    turkey                      = 'turkey'
    countryofgeorgia            = 'country georgia'
    kazakhstan                  = 'kazakhstan'
    turkmenistan                = 'turkmenistan'
    uzbekistan                  = 'uzbekistan'
    kyrgyzstan                  = 'kyrgyzstan'
    tajikistan                  = 'tajikistan'
    afghanistan                 = 'afghanistan'
    pakistan                    = 'pakistan'
    india                       = 'india'
    srilanka                    = 'srilanka'
    maldives                    = 'maldives'
    nepal                       = 'nepal'
    bhutan                      = 'bhutan'
    bangladesh                  = 'bangladesh'
    myanmar                     = 'myanmar'
    thailand                    = 'thailand'
    cambodia                    = 'cambodia'
    vietnam                     = 'vietnam'
    laos                        = 'laos'
    china                       = 'china'
    mongolia                    = 'mongolia'
    northkorea                  = 'north korea'
    southkorea                  = 'south korea'
    japan                       = 'japan'
    philippines                 = 'philippines'
    indonesia                   = 'indonesia'
    malaysia                    = 'malaysia'
    brunei                      = 'brunei'
    singapore                   = 'singapore'
    easttimor                   = 'east timor'
    papuanewguinea              = 'papua new guinea'

    Asian_Countries =[lebanon, israel, cyprus, jordan, syria, iraq, kuwait, saudiarabia, bahrain, qatar, yemen, oman, unitedarabemirates,
    iran, azerbaijan, armenia, turkey, countryofgeorgia, kazakhstan, turkmenistan, uzbekistan, kyrgyzstan, tajikistan, afghanistan,
    pakistan, india, srilanka, maldives, nepal, bhutan, bangladesh, myanmar, thailand, cambodia, vietnam, laos, china, mongolia,
    northkorea, southkorea, japan, philippines, indonesia, malaysia, brunei, singapore, easttimor, papuanewguinea]

    #South American Countries
    colombia                  = 'colombia'
    venezuela                 = 'venezuela'
    guyana                    = 'guyana'
    suriname                  = 'suriname'
    ecuador                   = 'ecuador'
    uruguay                   = 'uruguay'
    paraguay                  = 'paraguay'
    argentina                 = 'argentina'
    chile                     = 'chile'
    bolivia                   = 'bolivia'
    peru                      = 'peru'
    frenchguiana              = 'frech guiana'

    South_American_Countries = [colombia, venezuela, guyana, suriname, ecuador, uruguay, paraguay, argentina,
                                chile, bolivia, peru, frenchguiana]

    Country_list = [colombia, venezuela, guyana, suriname, ecuador, uruguay, paraguay, argentina,
                                chile, bolivia, peru, frenchguiana,lebanon, israel, cyprus, jordan, syria, iraq, kuwait, saudiarabia, bahrain, qatar, yemen, oman, unitedarabemirates,
    iran, azerbaijan, armenia, turkey, countryofgeorgia, kazakhstan, turkmenistan, uzbekistan, kyrgyzstan, tajikistan, afghanistan,
    pakistan, india, srilanka, maldives, nepal, bhutan, bangladesh, myanmar, thailand, cambodia, vietnam, laos, china, mongolia,
    northkorea, southkorea, japan, philippines, indonesia, malaysia, brunei, singapore, easttimor, papuanewguinea,portugal, spain, france, switzerland, italy, slovenia, croatia, bosniaandherzegovina, serbia,
    macedonia, albania, greece, bulgaria, romania, moldova, hungary, austria, czechrepublic, germany, belgium, netherlands,
    unitedkingdom, ireland, iceland, norway, denmark, sweden, finland, estonia, latvia, lithuania, poland, belarus, ukraine,
    russia, slovakia, andorra, monaco, vaticancity, sanmarino, luxembourgh, liechenstein, malta, montenegro, UnitedStatesOfAmerica, canada, mexico,morocco, mauritania, senegal, TheGambia, Guinea, sierraleone,
    liberia, ivorycoast, ghana, togo, benin, nigeria, burkinafaso, mali, niger, algeria,
    tunisia, libya, egypt, chad, cameroon, equatorialguinea, gabon, republicofthecongo, centralafricanrepublic, sudan,
    uganda, rwanda, burundi, demrepofthecongo, angola, namibia, southafrica, lesotho,
    swaziland, botswana, zimbabwe, zambia, malawi, mozambique, madagascar, comoros,
    tanzania, kenya, ethiopia, somalia, djibouti, eritrea, guineabissau, capeverde, seychelles,
    mauritias, saotomeandprincipe]
    #People Titles
    titMr                     = 'mr'
    titMrs                    = 'mrs'
    titMiss                   = 'miss'
    titDr                     = 'dr'
    titSir                    = 'sir'
    titProfessor              = 'professor'
    titReverend               = 'reverend'
    titPastor                 = 'pastor'
    titClergy                 = 'clergy'
    titRabbi                  = 'rabbi'
    titApostle                = 'apostle'
    titFather                 = 'father'
    titMother                 = 'mother'
    titElder                  = 'elder'
    titMadam                  = 'madam'
    titGeneral                = 'general'
    titCaptain                = 'captain'
    titDean                   = 'dean'
    titBrother                = 'brother'
    titSister                 = 'sister'

    full_titles = [titMr, titMrs, titMiss, titDr, titSir, titProfessor, titReverend,
                    titPastor, titClergy, titRabbi, titApostle, titFather, titMother, titElder,
                    titMadam, titGeneral, titCaptain, titDean, titBrother, titSister]



    def nextletter (self, strletter):

        try:

            strletter = str(strletter)
            strletter = strletter.lower()

            if len(strletter) == 1:
                ch = strletter[0]
                if ch == 'a':
                    return 'b'
                elif ch == 'b':
                    return 'c'
                elif ch == 'c':
                     return 'd'
                elif ch == 'd':
                    return 'e'
                elif ch == 'e':
                    return 'f'
                elif ch == 'f':
                    return 'g'
                elif ch == 'g':
                    return 'h'
                elif ch == 'h':
                    return 'i'
                elif ch == 'i':
                    return 'j'
                elif ch == 'j':
                    return 'k'
                elif ch == 'k':
                    return 'l'
                elif ch == 'l':
                    return 'm'
                elif ch == 'm':
                    return 'n'
                elif ch == 'n':
                    return 'o'
                elif ch == 'o':
                    return 'p'
                elif ch == 'p':
                    return 'q'
                elif ch == 'q':
                    return 'r'
                elif ch == 'r':
                    return 's'
                elif ch == 's':
                    return 't'
                elif ch == 't':
                    return 'u'
                elif ch == 'u':
                    return 'v'
                elif ch == 'v':
                    return 'w'
                elif ch == 'w':
                    return 'x'
                elif ch == 'x':
                    return 'y'
                elif ch == 'y':
                    return 'z'
                elif ch == 'z':
                    return 'a'
                else:
                    return 'a'

            else:
                return undefined
        except:
            return undefined


    # A Country is any of the ones mentioned above
    def isCountry (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.Countries_Of_Africa:
                return True
            elif strinput in self.European_Countries:
                return True
            elif strinput in self.Asian_Countries:
                return True
            elif strinput in self.South_American_Countries:
                return True
            elif strinput == self.canada:
                return True
            elif strinput == self.mexico:
                return True
            elif strinput == self.UnitedStatesOfAmerica:
                return True
            else:
                return False
        except:
            return undefined



    def is_American_State (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.USA_States:
                return True
            else:
                return False
        except:
            return undefined


    def is_African_Country (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.Countries_Of_Africa:
                return True
            else:
                return False
        except:
            return undefined


    def is_South_African_Province (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.South_African_Provinces:
                return True
            else:
                return False
        except:
            return undefined


    def is_European_Country (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.European_Countries:
                return True
            else:
                return False
        except:
            return undefined


    def is_Asian_Country (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.Asian_Countries:
                return True
            else:
                return False
        except:
            return undefined


    def is_SouthAmerican_Country (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.South_American_Countries:
                return True
            else:
                return False
        except:
            return undefined


    def is_title (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if strinput in self.full_titles:
                return True
            else:
                return False
        except:
            return undefined

    def isEven(self, inNum):
        try:
            inNum = str(inNum)
            inNum = inNum.strip()
            if inNum.isdigit():
                inNum = int(inNum)
                divNum = inNum % 2
                if divNum > 0:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False
    # Take any date and Add 30 days to it
    def Advance30Days(self, indate):
        try:
            if self.isEven(indate.year):
                feb = 28
                logging.info('FEBRUARY 28')
            else:
                feb = 29

            jan = 31
            mar = 31
            apr = 30
            may = 31
            jun = 30
            jul = 31
            aug = 31
            sep = 30
            oct = 31
            nov = 30
            dec = 31

            bDay = indate.day
            bmonth = indate.month
            byear = indate.year
            logging.info('YEAR :' + str(byear))
            logging.info('MONTH :' + str(bmonth))
            logging.info('DAY :' + str(bDay))
            if bmonth < 12:
                emonth = bmonth + 1
                eDay = bDay
                eYear = byear
                if (emonth == 2) and (bDay > feb):
                    eDay = bDay - feb
                    emonth = emonth + 1
                elif (emonth == 4) and (bDay == 31 ):
                    emonth = 5
                    eDay = 1
                elif (emonth == 6) and (bDay == 31):
                    emonth = 7
                    eDay = 1
                elif (emonth == 9) and (bDay == 31):
                    emonth = 10
                    eDay = 1
                elif (emonth == 11) and (bDay == 31):
                    emonth = 12
                    eDay = 1
            else:
                emonth = 1
                eDay = bDay
                eYear = byear + 1
            today = datetime.datetime.today()
            indate = today
            return indate.replace(year=eYear, month=emonth, day=eDay, hour=today.hour, minute=today.minute)
        except:
            return undefined










#Additional Classes for Contact Information Domains, Emails and Websites

class Domains (db.Expando):

    domains = []
    blacklist = [] #create the black listed domain list used to disallow everything from
    #emails websites and everything else from such domains and also to detect spam.
    #NOTE: I HAVE USED UNDEFINED ON THE LIST AS THE FIRST BLACKLIST OBJECT TO AVOID ERRORS WITH eXPANDO CLASS



    #add the functionality for the blacklisted domains

    #CONSIDER LOADING ALL THE VALID DOMAIN NAMES ONLINE AND ONLY USE LOAD DEFAULT FUNCTION
    #THIS WILL GET RID OF THE PART WHERE WE HAVE TO SAVE THIS DATA TO THE DATASTORE

    def loadDefault (self):

        try:
            #todo-find more domains to add here to allow more functionality with international clients
            self.domains = ['za','com','org','net','co','edu','mobi','fr','in','mx','jp','cn','ng']
            return True
        except:
            return False



    def isdomain (self, strinput):


        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if self.loadDefault(): #IF default domains are loaded then check for domain validity
                if strinput in self.domains:
                    return True
                else:
                    return False
        except:
            return False


    def addDomaintoBlackList (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if not(strinput in self.domains):
                self.blacklist.append(strinput)
                self.blacklist.sort()
                return True
            else:
                return False
        except:
            return False

    def removeDomaintoBlacklist (self, strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()

            if (strinput in self.domains):
                self.blacklist.remove(strinput)
                return True
            else:
                return False
        except:
            return False

    # Conduct a complete investigation first before you finalize this
    #The Ability to save and read domains from the store will be added later.
    #todo-remember to add the the domain storage capability this will give us the ability to create blacklists to combat spam





#Control Class for Contact Information

class CustomEmail(Domains):

    atsymbol = '@'
    dot = '.'





    #todo-Complete the send email verification algorithm
    #Given the Reference Number and the email address it sends a verification email
    #it directs the user to a verification form where the user must input their login name:
    #password email address and verification code to activate their account.

    #todo-After verification we can send a new email with the username and password
    def SendVerificationMail (self,strinput, strreference):

        try:

            logging.info('Inside Verification')

            html_message_body = '''
            <h2>Welcome to Freelancing Solutions</h2>
            <p>Your Account has been succesfully create and awaiting verification from you.</p>
            <p>Note: that failure to verify your account might lead to your account being cancelled</p>
            <p>In order to succesfully verify your account click on the link below:</p>
            <a href="http://freelancing-solutions.appspot.com/verifications"> <h3>Freelancing Solutions Account Verification</h3></a>
            <p>and on the form that appears input the code inserted below:</p>
            '''

            ActivationKey ='<h2> Activation Key: ' + str(strreference) + '</h2>'

            html_message_body = html_message_body + ActivationKey
            thankyoumessage = '<h3>Thank you</h3><h4>Freelancing Solutions</h4>'
            html_message_body = html_message_body + thankyoumessage

            logging.info('HTML BODY Message created')

            message_body ='''
            Welcome to Freelancing Solutions
            Your Account has been succesfully created and awaiting verification from you.
            Note: that failure to verify your account might lead to your account being cancelled.
            In order to succesfully verify your account go to the following URL address:
            http://freelancing-solutions.appspot.com/verifications/
            and on the form that appears input the code included below on this message:

            '''
            message_body = message_body + ' CODE : ' + str(strreference)
            logging.info(message_body)

            strinput = '<' + strinput + '>' #Adding ears to email

            mailmessage = mail.EmailMessage(
            #todo-i have to create an email address for the application and input it here
            sender='Freelancing Solutions  <mobiusndou@gmail.com>',
            to = strinput,
            subject='Freelancing Solutions Account Activation',
            body= message_body,  html = html_message_body
            )

            logging.info('Sending Activation Email')
            mailmessage.send() #Actually sending a message here

            return True
        except:
            logging.info('Raising an Exception sending emails')
            return False

    #todo-make this algorithm better it might contain bugs.
    def isemail(self, strinput):



        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.lower()


            if ((self.atsymbol in strinput) and (strinput[0].isalnum()) and (self.dot in strinput)):
                i = 1
                logging.info('all the symbols are being detected on the email address')
                while ((strinput[i] <> self.atsymbol) and (i < len(strinput))):
                    i = i + 1
                logging.info('We see if we found the at symbol' + strinput[i])
                if (len(strinput) > i):
                    j = len(strinput) - 1
                    while (strinput[j] <> self.dot) and (j > i):
                        j = j - 1
                    logging.info('still kicking')
                    domainstr = strinput[j+1 :(len(strinput) )] #getting a string output from a certain range
                    logging.info('here is the domain string: ' + domainstr)
                    if (strinput[j] == self.dot) and (self.isdomain(domainstr)):
                        logging.info('Email Verified')
                        return True
                else:
                    logging.info('check your alogrithm')
                    return False
            else:
                logging.info('Algo problems')
                return False
        except:
            logging.error('Raising exceptions on isemail')
            return False


#Control Class for Contact Information

class Website(Domains):

    dot = '.'

    def iswebsite (self, strinput):
    #Rewrite this alrogithm
        try:
            return True

        except:
            return False















"""


#This class will save the last system control information on the datastore and maintain a copy on the MemCache.



class DSettingsProfileStatus(db.Expando):

    #indexReference = db.ReferenceProperty(Reference, collection_name='settings_profile_status')
    DisplaySearch  = False
    LastSearchString = undefined
    DisplayBrowse  = False
    LastBrowsePosition = undefined
    DisplayDefault = False
    OwnProfilePosition = undefined
    DisplayOwnProfile = True


class DSettingsFreelanceJobsStatus (db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='settings_freelancejobs_status')


class DSettingsJobMarketStatus(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='settings_jobmarket_status')

class DSettingsAffiliatesStatus(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='settings_affiliates_status')


class DSettingsMarketPlaceStatus(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='settings_marketplace_status')




class Syscontrol(db.Expando):

    latestReference = undefined
    listRefIndexesforLoggedInUsers = undefined #this list can be used to check for loggedin users
    listIPAddressesforloggedinUsers = undefined #this list contains the list of loggedin IP Addresses
    #Every Reference must be added with its IP Address
    #todo-Create cookies to track the user sessions
    consNumLoggedinUsers = len(listRefIndexesforLoggedInUsers)


"""



