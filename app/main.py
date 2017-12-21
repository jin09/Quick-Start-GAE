#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import calendar
import hashlib
import hmac
import random
import string
import json
import logging
import urllib
import jinja2
import re
import datetime as dt
import sys
import webapp2
import os
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db
import pymongo
import pprint
from pymongo import MongoClient
from datetime import datetime
import requests
from time import gmtime, strftime
import csv
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os
import webapp2
from google.appengine.api import app_identity
from bson import ObjectId
import settings
import constants

#######################################################


jinja_env = jinja2.Environment(autoescape=True,
                               loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

### Validation regex for username email etc ... ############
USER_RE = re.compile(r"^[a-zA-Z]{3,20}\s?([a-zA-Z]{3,20})?$")


def valid_name(username):
    if username and USER_RE.match(username):
        return True
    else:
        return False


EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def valid_email(email):
    if email and EMAIL_RE.match(email):
        return True
    else:
        return False


def valid_phone(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    else:
        return False


######## Login Cookie pass hash handling #####################

SECRET = "lw45!y1dt9fg#h75df$W0f*gyfg@xy$e56h2@ddfgh2d#7s$t6h"


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_user_cookie(user_id):
    return "%s|%s" % (str(user_id), str(hmac.new(SECRET, str(user_id)).hexdigest()))


def check_valid_cookie(test_cookie):
    if "|" not in test_cookie:
        return False
    user_val = test_cookie.split('|')[0]
    if make_user_cookie(user_val) == test_cookie:
        return True
    else:
        return False


def create_pass_hash(pwd, username):
    salt = make_salt()
    h = hashlib.sha256(username + pwd + salt).hexdigest()
    return "%s,%s" % (h, salt)


def check_valid_pass(pass_val, pass_hash, username):
    h = hashlib.sha256(username + pass_val + pass_hash.split(',')[1]).hexdigest()
    if h == pass_hash.split(',')[0]:
        return True
    else:
        return False


###################################################################


###### DATETIME SERIALIZER #############

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


#########################################


######### Base Handler Class ###############


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


##############################################


############ DATABASE OPERATIONS (MONGO DB) #############



##################################################################


class MainHandler(Handler):
    def dispatch(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        super(MainHandler, self).dispatch()

    def get(self):
        self.write("Hello World!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
