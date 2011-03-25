import os
import datetime
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from faqna_models import *

#ehhhhh
def ShowTemplate(webapp, template_file, template_values):
  #reset cookies
  user = webapp.request.cookies.get('user_name','')
  add_template = {'user_name' : user}
  if type(template_values) is dict:
    template_values.update(add_template)
  else:
    template_values = add_template
  path = os.path.join(os.path.dirname(__file__), template_file)
  webapp.response.out.write(template.render(path, template_values))


def GetUser(webapp):
  user_name = webapp.request.cookies.get('user_name','')
  if user_name == '':
    return None
  else:
    user = User.get_by_key_name(user_name)
    if user:
      return user
    else:
      return None
