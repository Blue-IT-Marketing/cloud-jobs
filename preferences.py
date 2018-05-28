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
"""
Directly linked to the Reference class the preferences class will hold all the necessary preferences for each user,
company, freelancer, job seeker, and any other person making use of our system


WALLET-PREFERENCES
CURRENCY
PAYMENT_METHOD
PAYMENT_DATE


GENERAL PREFERENCES
TIME_ZONE
LANDING_PAGE


COMMUNICATION & NOTIFICATION PREFERENCES

SYSTEM NOTIFICATIONS
SMS_NOTIFICATIONS
EMAIL_NOTIFICATIONS
VOICE_NOTIFICATIONS
SOCIAL_NETWORKS_NOTIFICATIONS

PREFERRED METHOD OF COMMUNICATIONS WITH OTHER USERS
SMS_MESSAGES
EMAIL_MESSAGES
VOICE_MESSAGES
SOCIAL_NETWORKS_MESSAGES

FREELANCE JOBS
SEND NOTIFICATIONS ON THIS EVENTS.

WHEN FREELANCE JOBS YOU QUALIFY FOR ARE AVAILABLE.

    INDICATE THE KIND OF FREELANCE JOBS YOU INTEND TO BID FOR

    SEND NOTIFICATION ONLY
    SEND LINKS TO JOBS
    SEND SUMMARY AND LINKS

    NOTICE INTERVAL
        ONCE A DAY
        ONCE A WEEK

    TAKE ACTION
        SEND DEFAULT BID FOR THAT FREELANCE JOB TYPE.
        NOTIFY USING THE MOST PREFERRED METHOD FIRST. IF NO RESPONSE IN TWO HOURS THEN USE THE SECOND METHOD.

WHEN JOBS YOU QUALIFY FOR ARE AVAILABLE ON THE JOB MARKET.

    INDICATE THE KIND OF JOBS YOU INTEND TO APPLY FOR.

    SEND NOTIFICATION ONLY
    SEND LINKS TO JOBS
    SEND SUMMARY AND LINKS

    NOTICE INTERVAL
        ONCE A DAY
        ONCE A WEEK
        ONCE A MONTH

    TAKE ACTION
        SEND DEFAULT APPLICATION FOR THAT JOB TYPE.
        NOTIFY IF SHORTLISTED IMMEDIATELY. USING THE MOST PREFERRED METHOD OF COMMUNICATION IF NO RESPONSE WITHIN
        TWO HOURS THEN USE THE SECOND METHOD

SERVICES AND PRODUCTS OF INTEREST ON THE MARKET PLACE.

    INDICATE SERVICES AND PRODUCTS YOU ARE INTERESTED IN ON OUR MARKET PLACE.

    WHEN SERVICES YOU ARE INTERESTED ARE AVAILABLE ON THE MARKET PLACE.
        SEND NOTIFICATION ONLY.
        SEND LINKS TO SERVICES.
        SEND SUMMARY AND LINKS.

        NOTICE INTERVAL
            ONCE A DAY
            ONCE A WEEK

        TAKE ACTION.
            BUY IF PRICE IS BELOW AND ABOVE.
            BUY IF PRICE IS BELOW AND SELLER REPUTATION IS ABOVE.
            AND THEN SEND NOTIFICATION USING THE MOST PREFFERED METHOD IF NO RESPONSE WITHIN TWO HOURS THEN USE
            THE SECOND METHOD.


AFFILIATES PRODUCTS AND SERVICES.
    INDICATE AFFILIATE SERVICES AND PRODUCTS TYPES YOU ARE INTERESTED IN.
    WHEN AFFILIATES SERVICES AND PRODUCTS ARE AVAILABLE THAT YOU ARE INTERESTED IN.
        SEND NOTIFICATION ONLY.
        SEND LINKS TO AFFILIATE SERVICE OR PRODUCT.
        SEND SUMMARY AND LINKS.

        NOTICE INTERVAL
            ONCE A DAY
            ONCE A WEEK
            ONCE A MONTH.

        TAKE ACTION.
             SUBSCRIBE AND SEND DETAILS BY EMAIL.



"""
from datatypes import *
from companies import *
from ConstantsAndErrorCodes import *

class UserPreferences(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='preferences_collection')

class WalletPreferences(db.Expando, MyConstants, ErrorCodes):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='wallet_preferences')
    strCurrency = undefined  # Consider Creating a_constant list with all the Currency Codes Here
    PaymentMethod = undefined  # Consider creating a _constant list with all the payment methods here
    PaymentDay = undefined  # Consider creating a _constant list with all the possible values for payment days



class GeneralPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='general_preferences')
    TimeZone = undefined  # Consider a list with all the possible time zones
    LandingPage = undefined  # Consider a list with all the possible default landing pages

class SystemCommunicationPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='system_com_preferences')
    _notificationKinds = ['internal', 'sms', 'email', 'voice', 'social']
    _socialmedia = ['facebook', 'linkedin', 'google+', 'twitter']

    NotificationOrder = db.StringListProperty(default=_notificationKinds)
    SocialOrder = db.StringListProperty(default=_socialmedia)



class UserCommunicationPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='user_com_preferences')
    _messagingKinds = ['internal', 'email', 'sms', 'voice', 'social']
    _socialmedia = ['facebook', 'linkedin', 'google+', 'twitter']

    MessagingOrder = db.StringListProperty(default=_messagingKinds)
    SocialOrder = db.StringListProperty(default=_socialmedia)


class FreelanceJobsPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='freelance_jobs_preferences')
    _freelancejobsofinterest = ['seo', 'website development', 'article writing', 'landing page development', 'application development']
    _notificationevents = ['available', 'bidding ended', 'job awarded']
    _notificationsettings = ['notification only', 'links to jobs', 'summary and links']
    _notificationinterval = ['daily', 'weekly']
    _defaultactions = ['ignore', 'bid', 'notifyonly', 'notifyandbid']

    FreelanceJobsOfInterest = db.StringListProperty(default=_freelancejobsofinterest)
    EventsForNotifications = db.StringListProperty(default=_notificationevents)
    NotificationsSettings = db.StringListProperty(default=_notificationsettings)
    NotificationInterval = db.StringListProperty(default=_notificationinterval)
    DefaultActions = db.StringListProperty(default=_defaultactions)
    DateCreated = db.DateTimeProperty(auto_now_add=True)





class JobMarketPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='job_market_preferences')
class MarketPlacePreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='market_place_preferemces')
class AffiliatesPreferences(db.Expando):
    indexReference = db.ReferenceProperty(UserPreferences, collection_name='affiliates_preferences')




#Storing the preferences for companies


class CompanyPreferences(db.Expando):
    indexReference = db.ReferenceProperty(CompanyReference, collection_name='preferences_collection')



class InterfacePrefs(db.Expando, MyConstants, ErrorCodes):
    doshowlogin = db.BooleanProperty(default=True)
