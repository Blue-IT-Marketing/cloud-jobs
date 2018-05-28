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


'''
freelancing solutions
market place module
by Justice Ndou
Python Class defining the market place
all the major functionality of the market place will be implemented here

'''
from datatypes import Reference
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import logging
from accounts import Wallet
from ConstantsAndErrorCodes import MyConstants, ErrorCodes
#Merchant is a class for those who are selling on the market place
class Merchant(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='merchant_collection')
#Control Class for the buyers
class Buyer(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='buyer_collection')

class Shop(db.Expando):
    indexReference = db.ReferenceProperty(Reference, collection_name='shop_collection')
'''
Need a Store Design
create a fresh design that allows buying and selling by everyone

We Need
Products.
Services


(Each product and service have an owner
and when bought money is transferred from the buyer to the seller)
'''
#Control class for the store


class Products(db.Expando):
    strProductCode = db.StringProperty()
    strProductName = db.StringProperty()
    strProductDescription = db.StringProperty(multiline=True)
    strProductPrice = db.StringProperty(default='0')
    # Referes back to the user who owns this product
    strProductOwner = db.ReferenceProperty(Reference, collection_name='products_collection')
    # Product Logo or Picture
    ProductlogoPicture = db.BlobProperty()
    # If set to true teh product can be sold
    ProductIsSelling = db.BooleanProperty(default=False)
    DateTimeCreated = db.DateTimeProperty(auto_now=True)
    DateTimeModified = db.DateTimeProperty(auto_now_add=True)


class Service(db.Expando):
    strServiceCode = db.StringProperty()
    strServiceName = db.StringProperty()
    strServiceDescription = db.StringProperty()
    strServicePrice = db.StringProperty()
    strServiceOwner = db.ReferenceProperty(Reference, collection_name='service_collection')
    ServiceLogoPicture = db.BlobProperty()
    #If its set to true the service can be sold
    ServiceIsSelling = False
    DateTimeCreated = db.DateTimeProperty(auto_now=True)
    DateTimeModified = db.DateTimeProperty(auto_now_add=True)

#Linking to all products and services on the market presently


class MarketPlace(db.Expando):
    clsProducts = db.ReferenceProperty(Products, collection_name='market_place_collection')
    clsService = db.ReferenceProperty(Service, collection_name='market_place_collection')






