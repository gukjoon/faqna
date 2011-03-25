#!/usr/bin/env python
import cgi
import datetime
import hashlib
import logging
import string
import time

from django.utils import simplejson as json
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue
from google.appengine.api import memcache

from faqna_models import *
from faqna_helpers import *

class MainPage(webapp.RequestHandler):
    def get(self):
        ShowTemplate(self, 'templates/index.html', {})
        

class ProductPage(webapp.RequestHandler):
    def get(self,product_id):
        fetched_product = Product.get_by_id(int(product_id))
        fetched_tags = ProductTags.all().ancestor(fetched_product.key())[0]
        ShowTemplate(self, 'templates/product.html',
                     {'product_title' : fetched_product.title, 
                      'product_id' : product_id,
                      'product_tags' : fetched_tags.tags,
                      'questions' : [{'answers' : question.answers,
                                      'question_id' : question.key().id(),
                                      'text' : question.text} for question in fetched_product.questions]})


class RegisterPage(webapp.RequestHandler):
    def get(self):
        ShowTemplate(self, 'templates/register.html', {})
    def post(self):
        hashedpass = hashlib.md5(self.request.get('password')).hexdigest()
        handle=self.request.get('handle')
        email=self.request.get('email')
        user = User(key_name=self.request.get('handle'),password=hashedpass,handle=handle,email=email)
        user.put()
        self.response.headers.add_header('Set-Cookie', 'user_name=%s' % user.handle.encode())
        self.redirect('/')

class TagSearchPage(webapp.RequestHandler):
    def get(self,tag):
        product_tags = db.GqlQuery("SELECT __key__ FROM ProductTags "
                               "WHERE tags = :1", tag)
        product_keys = [k.parent() for k in product_tags]
        products = [{'title' : product.title,
                     'id': product.key().id()} for product in db.get(product_keys)]
        ShowTemplate(self, 'templates/tagsearch.html', {'products' : products})


class LoginPage(webapp.RequestHandler):
    def get(self):
        ShowTemplate(self, 'templates/login.html', {})
    def post(self):
        
        handle = self.request.get('handle')
        password = hashlib.md5(self.request.get('password')).hexdigest()
        
        user = User.get_by_key_name(handle)
        
        if user:
            if password == user.password:
                self.response.headers.add_header('Set-Cookie', 'user_name=%s' % user.handle.encode())
                self.redirect('/')
            else:
                self.response.out.write('incorrect pass')
        else:
            self.response.out.write('invalid user')
            
        
class SellPage(webapp.RequestHandler):
    def get(self):
        user = GetUser(self)
        if user:
            ShowTemplate(self, 'templates/sell.html', {'products':[{'title':product.title,
                                                                    'id':product.key().id()}
                                                                   for product in user.products]})
        else:
            self.redirect('/login')
    


class BuyPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('not implemented yet')
