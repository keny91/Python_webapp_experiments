#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course


import webapp2
import functions # Funciones externas 


# Contenido HTML

form=""" 

<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

</head>
<body>
<form  method ="post" >     
<b class="header1">Signup</b>
<br>
<br>


<label>Username
<input  style= "margin-left:93px;" name= "username" type="text" value="%(username)s">
</label>
<b style="color: red">%(error_username)s</b>
<br>
<br>


<label > Password
<input style="margin-left:96px;" name= "password" type="password">
</label>
<b style="color: red">%(error_invalid_pasword)s</b>
<br>
<br>

<label>Verify Password
<input style="margin-left:53px;" name= "verify" type="password">
</label>
<b style="color:red">%(error_invalid_match)s</b>
<br>
<br>
<label>Email (optional)
<input style="margin-left:53px;" name= "email" type="text" value="%(email)s">
</label>
<b style="color:red">%(error_invalid_email)s</b>
<br>
<br>
<input style="margin-left:93px;" type= "submit" >
</form>
</body>
</html>
"""


#Variables globales

#HANDLER
class MainHandler(webapp2.RequestHandler):


    # writing the form, it shows error just when it fails
    # DEAFAULT PARAMETER
    def write_form(self, error1="",error2="",error3="",error4="",username="",email=""):  # SELF to work
        self.response.out.write(form % {"error": error, "month":functions.html_escape(month), "day":functions.html_escape(day), "year":functions.html_escape(year)})
        self.response.out.write(form % {"error_username": error1, "error_invalid_pasword":error2, "error_invalid_match":error3 , "error_invalid_email":error4, "username":functions.html_escape(username), "email":functions.html_escape(email)})


    def get(self):
        
        self._render_text = self.content.replace('\n','<br>')
        return render_str("front.html",p=self)


    def post(self):

    	user_username = self.request.get('username')
    	user_password = self.request.get('password')
    	user_verify_password = self.request.get('verify')
        user_email = self.request.get('email')

        username = functions.valid_username(user_username)
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
                error_message_3 = "Your password didnt match"

            if not email:
                error_message_4 = "Not a valid email"
            
            self.write_form(error_message_1,error_message_2,error_message_3,error_message_4, user_username, user_email)

          # case information is correct
        else:
            self.redirect("/welcome?username=%s"%(user_username))
        
           #q = self.request.get("q")
        #self.response.out.write(q)

        #See the http request
       # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)




class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome, %s!"%(self.request.get('username')))  # recoge la variable



app = webapp2.WSGIApplication([('/', MainHandler),('/welcome', WelcomeHandler)],debug=True)



#month_abre =dict((m[:3].lower(),m) for m in months)

