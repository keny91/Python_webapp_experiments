#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course

import os
import webapp2
import functions # Funciones externas 
import jinja2
import time
import string
import random
import hmac
import hashlib

from google.appengine.ext import db


SECRET = 'ojetemoreno'


template_dir = os.path.join(os.path.dirname(__file__),'templates')  # nade of my directory + /templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) ,autoescape = True)

    


####### SECURITY

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


#  Generates a string (name+pw+salt,salt)
def make_pw_hash(name, pw, salt=''):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    val = h.split('|')[0]
    salt = h.split('|')[1]
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



#################

# Database

class UserReg(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw): # le estamos pasando una lista(array *) y un diccionario (**)
        self.response.out.write(*a,**kw)

#  Methods to render basic HTML files
    def render_str(self, template, **params):
        t =jinja_env.get_template(template) 
        return t.render(params)


    def render(self , template, **kw):
        self.write(self.render_str(template,**kw))




class SignupHandler(Handler):



    # def render_front(self):
    #     self.response.headers['Content-Type'] ='text/plain'
    #     # visits_cookie_val = self.request.cookies.get('visits')


    # writing the form, it shows error just when it fails
    # DEAFAULT PARAMETER
    def render_form(self, error1="",error2="",error3="",error4="",username="",email=""):  # SELF to work
        # self.response.out.write(form % {"error": error, "month":functions.html_escape(month), "day":functions.html_escape(day), "year":functions.html_escape(year)})
        self.render('signup.html',error_username = error1, error_invalid_pasword = error2, error_invalid_match = error3 , error_invalid_email = error4, username = username, email= email)

        # user_cookie_val = self.request.cookies.get('username')


    def get(self):

        # self._render_text = self.content.replace('\n','<br>')
        return self.render("signup.html",p=self)

    def post(self):

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify_password = self.request.get('verify')
        user_email = self.request.get('email')

        username = functions.valid_username(user_username)
        # username= user_username
        password = functions.valid_password(user_password)
        verify = functions.compare_passwords(user_password,user_verify_password)
        email = functions.valid_email(user_email)

# caso de que alguno no se válido
# Vuelve a cargar el form

        error_message_1 = ""
        error_message_2 = ""
        error_message_3 = ""
        error_message_4 = ""
#           case any information is incorrect 
        if not (username and password and verify and email):

            #  we determine which information is incorrect
            if not username:
                error_message_1 = "Not a valid username"

            if not password:
                error_message_2 = "Not a valid password"

            if not verify:
                error_message_3 = 'Your password didnt match'
                # error_message_3 = 'user = %s pass = %s email = %s' % (username,password,email)
            if not email:
                error_message_4 = "Not a valid email"

            u = UserReg.all().filter('username =', username).get()
            if u:
                error_message_1 = "That user already exists"
            
            self.render_form(error_message_1,error_message_2,error_message_3,error_message_4, user_username, user_email)
            

          # case information is correct
        else:

            if email == False:
                email = ""

            pass_hash = make_pw_hash(username, password)
            user = UserReg(username=username,
                            password=pass_hash,
                            email=str(email))
            user.put()

            new_cookie_user= make_secure_val(str(username))

            self.response.headers.add_header('Set-Cookie', 'username=%s' % new_cookie_user)
            self.redirect("/welcome")
           #q = self.request.get("q")
        #self.response.out.write(q)

        #See the http request
       # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)


class LoginHandler(Handler):

    def render_form(self, error=""):  # SELF to work
        # self.response.out.write(form % {"error": error, "month":functions.html_escape(month), "day":functions.html_escape(day), "year":functions.html_escape(year)})
        self.render('login.html', error = error)

        # user_cookie_val = self.request.cookies.get('username')


    def get(self):

        # self._render_text = self.content.replace('\n','<br>')
        return self.render("login.html",p=self)

    def post(self):

        user_username = self.request.get('username')
        user_password = self.request.get('password')


        # username = functions.valid_username(user_username)
        username = functions.valid_username(user_username)
        password = functions.valid_password(user_password)
        u = UserReg.all().filter('username =', username).get()

        # if not username and password:
        #     error = "Invalid Login"
        #     self.render_form(error)

        # elif not u:
        #     error = "That user does not exists"
        #     self.render_form(error)

        # else:
        check_pass = valid_pw(username,password,u.password)

        if check_pass:
                #success
            new_cookie_user= make_secure_val(str(username))

            self.response.headers.add_header('Set-Cookie', 'username=%s' % new_cookie_user)
            self.redirect("/welcome")

        else:
                #
            error = "Invalid Login"
            self.render_form(error)

class LogoutHandler(Handler):

    def get(self):
        self.response.delete_cookie('username')
        # user_cookie_val = self.request.cookies.get('username')
        # self.response.headers.add_header('Set-Cookie', 'username=%s', 'expires=0' % user_cookie_val)
        self.redirect("/signup")



        

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):

        user_cookie_val = self.request.cookies.get('username')
        cookie_val = check_secure_val(user_cookie_val)
        if not cookie_val:
            self.redirect("/signup")
            
        else:
            self.response.out.write("Welcome, %s!"%(cookie_val))
                
        # self.response.headers['Content-Type'] = 'text/plain'
        
          # recoge la variable



app = webapp2.WSGIApplication([('/signup', SignupHandler),('/welcome', WelcomeHandler),('/login', LoginHandler),('/logout', LogoutHandler)],debug=True)




















































# #  APP ENGINE PROBLEMAS CON ','

# # Generates a 5 char string with Random chars
# def make_salt():
#     return ''.join(random.choice(string.letters) for x in xrange(5))


# #  Generates a string (name+pw+salt,salt)
# #  If we have an already vreated salt, we will respect that
# def make_pw_hash(name, pw, salt=''):
#     if not salt:
#         salt = make_salt()
#     h = hashlib.sha256(name + pw + salt).hexdigest()
#     return '%s,%s' % (h, salt)

# def valid_pw(name, pw, h):
#     val = h.split(',')[0]
#     salt = h.split(',')[1]
#     if (hashlib.sha256(name + pw + salt).hexdigest()==val):
#         return True
#     else:
#         return False


# def hash_str(s):
#     ###Your code here
#     return hmac.new(SECRET,s).hexdigest()


# # OLD HASH
# # def hash_str(s):
# #     return hashlib.md5(s).hexdigest()

# def make_secure_val(s):
#     return "%s|%s" % (s, hash_str(s))

# # -----------------
# # User Instructions
# # 
# # Implement the function check_secure_val, which takes a string of the format 
# # s,HASH
# # and returns s if hash_str(s) == HASH, otherwise None 

# def check_secure_val(h):
#     val = h.split('|')[0]
#     if h==make_secure_val(val):
#         return val
#     else:
#         return None


# #Variables globales

# #HANDLER

# class Handler(webapp2.RequestHandler):
#     def write(self, *a,**kw): # le estamos pasando una lista(array *) y un diccionario (**)
#         self.response.out.write(*a,**kw)

# #  Methods to render basic HTML files
#     def render_str(self, template, **params):
#         t =jinja_env.get_template(template) 
#         return t.render(params)


#     def render(self , template, **kw):
#         self.write(self.render_str(template,**kw))

# #  CLASS TO CREATE AN ENTITY
# class Post_Entries(db.Model):
#     subject = db.StringProperty(required = True)
#     content = db.TextProperty(required = True)
#     # url = db.
#     created = db.DateTimeProperty(auto_now_add = True)


#     def render(self):
#         self._render_text = self.content.replace('\n','<br>')
#         return render_str("post.html",p=self)


# class MainHandler(Handler):



#     def render_front(self):
#         self.response.headers['Content-Type'] ='text/plain'
#         visits_cookie_val = self.request.cookies.get('visits')


#         visits=0
#         if visits_cookie_val:
#             cookie_val = check_secure_val(visits_cookie_val)
#             if cookie_val:
#                 visits = int(cookie_val)

#         # if visits.isdigit():
#         #     visits=int(visits)+1

#         visits += 1

#         new_cookie_val= make_secure_val(str(visits))
#         self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)


#         if visits < 20:
#             self.write("You have been here %s times!"% visits)
#         else:
#             self.write("You are the best ever!")


#         # x = hashlib.sha256("udacity")
#         # self.write(x.hexdigest())










#                 # if visits.isdigit():
#         #     visits=int(visits)+1
        
#         # else:
#         #     visits=0
        

#         # self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)
#         # if visits < 10:
#         #     self.write("You have been here %s times!"% visits)
#         # else:
#         #     self.write("You are the best ever!")
#     def get(self):
#         self.render_front()



# class PostHandler(Handler):
#     def get(self, post_id):
#         post_entry = Post_Entries.get_by_id(int(post_id))

#         if post_entry:
#             self.render("Post.html", post_entry=post_entry)

#         else:
#             self.render("Post.html",error="Post %s not found" %post_id)


        


# app = webapp2.WSGIApplication([
#     ('/', MainHandler),
#     (r'/blog/(\d+)',PostHandler ) 
#     ], debug=True)
   




# #   ENCRYPTING

# # def hash_str(s):
# #     return hashlib.md5(s).hexdigest()

# # def make_secure_val(s):
# #     return "%s,%s" % (s, hash_str(s))

# # # -----------------
# # # User Instructions
# # # 
# # # Implement the function check_secure_val, which takes a string of the format 
# # # s,HASH
# # # and returns s if hash_str(s) == HASH, otherwise None 

# # def check_secure_val(h):
# #     val = h.split(',')[0]
# #     if h==make_secure_val(val):
# #         return val
# #     else:
# #         return None






   