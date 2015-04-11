#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course

import os
import webapp2
import functions # Funciones externas 
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')  # nade of my directory + /templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) ,autoescape = True)

# Contenido HTML



item_html="""
<li>%s</li>
"""


hidden_html="""
<input type="hidden" name="food" value="%s">

"""

shopping_list_html="""
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""


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


class MainHandler(Handler):


    # writing the form, it shows error just when it fails
    # DEAFAULT PARAMETER
    # def write_form(self, error1="",error2="",error3="",error4="",username="",email=""):  # SELF to work
    #     # self.response.out.write(form % {"error": error, "month":functions.html_escape(month), "day":functions.html_escape(day), "year":functions.html_escape(year)})
    #     self.response.out.write(form % {"error_username": error1, "error_invalid_pasword":error2, "error_invalid_match":error3 , "error_invalid_email":error4, "username":functions.html_escape(username), "email":functions.html_escape(email)})


    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items = items)


       
    

        

    # def post(self):

    	# user_username = self.request.get('username')
    


            # self.redirect("/welcome?username=%s"%(user_username))
        
 



# class WelcomeHandler(webapp2.RequestHandler):
# 	def get(self):
# 		self.response.out.write("Welcome, %s!"%(self.request.get('username')))  # recoge la variable


class FizzHandler(Handler):
    def get(self):
        n = self.request.get("n")
        if n:
            n= int(n)
        self.render("fizzbuzz.html", n=n)





app = webapp2.WSGIApplication([('/', MainHandler), ('/fizzbuzz', FizzHandler)],debug=True)
# app = webapp2.WSGIApplication([('/', MainHandler),('/welcome', WelcomeHandler)],debug=True)



#month_abre =dict((m[:3].lower(),m) for m in months)

