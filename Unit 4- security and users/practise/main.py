#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course

import os
import webapp2
# import functions # Funciones externas 
import jinja2
import time
import string

import hmac
import hashlib

from google.appengine.ext import db


SECRET = 'imsosecret'


template_dir = os.path.join(os.path.dirname(__file__),'templates')  # nade of my directory + /templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) ,autoescape = True)

    


#  APP ENGINE PROBLEMAS CON ','

# Generates a 5 char string with Random chars
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


#  Generates a string (name+pw+salt,salt)
def make_pw_hash(name, pw, salt=''):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    val = h.split(',')[0]
    salt = h.split(',')[1]
    if (hashlib.sha256(name + pw + salt).hexdigest()==val):
        return True
    else:
        return False


def hash_str(s):
    ###Your code here
    return hmac.new(SECRET,s).hexdigest()


# OLD HASH
# def hash_str(s):
#     return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    val = h.split('|')[0]
    if h==make_secure_val(val):
        return val
    else:
        return None


#Variables globales

#HANDLER

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw): # le estamos pasando una lista(array *) y un diccionario (**)
        self.response.out.write(*a,**kw)

#  Methods to render basic HTML files
    def render_str(self, template, **params):
        t =jinja_env.get_template(template) 
        return t.render(params)


    def render(self , template, **kw):
        self.write(self.render_str(template,**kw))

#  CLASS TO CREATE AN ENTITY
class Post_Entries(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    # url = db.
    created = db.DateTimeProperty(auto_now_add = True)


    def render(self):
        self._render_text = self.content.replace('\n','<br>')
        return render_str("post.html",p=self)


class MainHandler(Handler):



    def render_front(self):
        self.response.headers['Content-Type'] ='text/plain'
        visits_cookie_val = self.request.cookies.get('visits')


        visits=0
        if visits_cookie_val:
            cookie_val = check_secure_val(visits_cookie_val)
            if cookie_val:
                visits = int(cookie_val)

        # if visits.isdigit():
        #     visits=int(visits)+1

        visits += 1

        new_cookie_val= make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)


        if visits < 20:
            self.write("You have been here %s times!"% visits)
        else:
            self.write("You are the best ever!")


        # x = hashlib.sha256("udacity")
        # self.write(x.hexdigest())










                # if visits.isdigit():
        #     visits=int(visits)+1
        
        # else:
        #     visits=0
        

        # self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)
        # if visits < 10:
        #     self.write("You have been here %s times!"% visits)
        # else:
        #     self.write("You are the best ever!")
    def get(self):
        self.render_front()



class PostHandler(Handler):
    def get(self, post_id):
        post_entry = Post_Entries.get_by_id(int(post_id))

        if post_entry:
            self.render("Post.html", post_entry=post_entry)

        else:
            self.render("Post.html",error="Post %s not found" %post_id)


        


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/blog/(\d+)',PostHandler ) 
    ], debug=True)
   




#   ENCRYPTING

# def hash_str(s):
#     return hashlib.md5(s).hexdigest()

# def make_secure_val(s):
#     return "%s,%s" % (s, hash_str(s))

# # -----------------
# # User Instructions
# # 
# # Implement the function check_secure_val, which takes a string of the format 
# # s,HASH
# # and returns s if hash_str(s) == HASH, otherwise None 

# def check_secure_val(h):
#     val = h.split(',')[0]
#     if h==make_secure_val(val):
#         return val
#     else:
#         return None






   