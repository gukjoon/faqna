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

class ProductTagHandler(webapp.RequestHandler):
  def post(self,product_id):
    tag = self.request.get('tag')
    fetched_product = Product.get_by_id(int(product_id))
    fetched_tags = ProductTags.all().ancestor(fetched_product)[0]
    if not tag in fetched_tags.tags:
      fetched_tags.tags.append(tag)
      fetched_tags.put()
      #queue up tag updates
    self.redirect('/product/' + product_id)


class ProductUpdateHandler(webapp.RequestHandler):
  def post(self,product_id):
    self.response.out.write('not implemented')

class ProductCreateHandler(webapp.RequestHandler):
  def post(self):
    user = GetUser(self)
    if user:
      product_title = self.request.get('title')
      new_product = Product(title=product_title,user=user)
      new_product.put()
      new_product_tags = ProductTags(parent=new_product)
      new_product_tags.put()
      self.redirect('/product/' + str(new_product.key().id()))
    else:
      self.redirect('/login')


class QuestionHandler(webapp.RequestHandler):
  def post(self,product_id):
    question_text = self.request.get('text')
    fetched_product = Product.get_by_id(int(product_id))
    new_question = Question(product=fetched_product,text=question_text)
    new_question.put()
    self.redirect('/product/' + product_id)


class AnswerHandler(webapp.RequestHandler):
  def post(self,product_id,question_id):
    answer_text = self.request.get('text')
    fetched_question = Question.get_by_id(int(question_id))
    new_answer = Answer(question=fetched_question, text=answer_text)
    new_answer.put()
    self.redirect('/product/' + product_id)


class LogoutHandler(webapp.RequestHandler):
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'user_name=')
    self.redirect('/')
