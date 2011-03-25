#!/usr/bin/env python
from google.appengine.ext import db

class User(db.Model):
    handle = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)


#relation index entities

#seller side
class Product(db.Model):
    user = db.ReferenceProperty(reference_class=User,collection_name='products',required=True)
    title = db.StringProperty()
    description = db.TextProperty()
    
class ProductTags(db.Model):
    tags = db.StringListProperty(default=[])

    
#class ProductSubscription(db.Model):
#    user = db.ReferenceProperty(reference_class=User,required=True)
#    product = db.ReferenceProperty(reference_class=Product,required=True)


class Question(db.Model):
    user = db.ReferenceProperty(reference_class=User)
    product = db.ReferenceProperty(reference_class=Product,collection_name='questions',required=True)
    text = db.StringProperty(required=True)

class Answer(db.Model):
    user = db.ReferenceProperty(reference_class=User)    
    question = db.ReferenceProperty(reference_class=Question,collection_name='answers',required=True)
    text = db.TextProperty(required=True)




#keyname
class Tag(db.Model):
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(default=0)

#children
class TagProducts(db.Model):
    products = db.ListProperty(db.Key)

class TagSimilar(db.Model):
    similar = db.StringListProperty()

#buyerside
class Query(db.Model):
    #list of tags
    name = db.StringProperty()
    tags = db.StringListProperty()
    
#parent is Query
class QueryProperty(db.Model):
    question = db.StringProperty()
    answer = db.StringProperty()
