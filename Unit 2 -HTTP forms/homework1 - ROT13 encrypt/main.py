#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course


import webapp2
import functions # Funciones externas 


# Contenido HTML

html_form=""" 
<form method ="post">     
Enter some text to be encrypted by ROT13
<br>
<br>

<textarea rows ="4" cols="60" name= "text" type="text" >
%(textarea_data)s
</textarea>

<br>
<input type= "submit" value="ROT13">
</form>
"""


#Global Variables


#HANDLER
class MainHandler(webapp2.RequestHandler):


    # writing the form, it shows error just when it fails
    # DEAFAULT PARAMETER
    def write_data(self, user_data=""):  # SELF to work
        self.response.out.write(html_form % {"textarea_data":user_data})

    def get(self):
        self.write_data()

    def post(self):

    	user_data = self.request.get("text") # data inserted by user in the databox

        print user_data
        data = functions.ROT13_onlyChar(user_data)
        self.write_data(data)




app = webapp2.WSGIApplication([('/', MainHandler)],debug=True)



#month_abre =dict((m[:3].lower(),m) for m in months)




