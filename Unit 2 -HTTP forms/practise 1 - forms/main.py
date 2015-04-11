#!/usr/bin/env python
# -- coding: utf-8 --
# Proyect 1 for Unit 2 in the Udacity Web course


import webapp2
import functions # Funciones externas 


# Contenido HTML

form=""" 
<form method ="post">     
What is your birthday?
<br>
<label>Month
<input name= "month" type="text" value="%(month)s">
</label>
<label> Day
<input name= "day" type="text" value="%(day)s">
</label>
<label>Year
<input name= "year" type="text" value="%(year)s">
</label>

<div style="color: red">%(error)s</div>
<br>

<input type= "submit">
</form>
"""


#Variables globales
months = ['January',
'February',
'March',
'April',
'May',
'June',
'July',
'August',
'September',
'October',
'November',
'December']


#HANDLER
class MainHandler(webapp2.RequestHandler):


    # writing the form, it shows error just when it fails
    # DEAFAULT PARAMETER
    def write_form(self, error="",month="",day="",year=""):  # SELF to work
        self.response.out.write(form % {"error": error, "month":functions.html_escape(month), "day":functions.html_escape(day), "year":functions.html_escape(year)})

    def get(self):
        self.write_form()

    def post(self):

    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')

        month = functions.valid_month( user_month, months)
        day = functions.valid_day(user_day)
        year = functions.valid_year(user_year)

# caso de que alguno no se válido
# Vuelve a cargar el form
        if not (month and day and year):
            self.write_form("INVALID DATE", user_month, user_day, user_year)  # si falla guarda los datos metidos

          # caso de que todas sean validas
        else:
            self.redirect("/success")

           #q = self.request.get("q")
        #self.response.out.write(q)

        #See the http request
       # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)




class SuccessHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a valid day!")



app = webapp2.WSGIApplication([('/', MainHandler),('/success', SuccessHandler)],debug=True)



#month_abre =dict((m[:3].lower(),m) for m in months)

