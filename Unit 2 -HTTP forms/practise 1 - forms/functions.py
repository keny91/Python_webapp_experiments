#Functions that compliment main.py


import cgi



def valid_month(month, monthArray):
    
    month = month.capitalize()
    if (month in monthArray):
        return month
    else:
        return None
  

def valid_day(day):
      if day.isdigit() and 1<= int(day) and int(day)<= 31:
          return int(day)
      else:
          return None  

def valid_year(year):
      if year.isdigit() and 1900 <= int(year) and int(year)<= 2020:
          return int(year)
      else:
          return None 

# Helps to avoid HTML interferences when reciving inputs
def html_escape (s):
#Replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# NOTE!!! ====>& MUST BE CONVERTED FIRST


  # Library code
  return cgi.escape(s,quote = True)
# My code 
""" 
s = s.replace('&', '&amp;')
s = s.replace('>', '&gt;')
s = s.replace('<', '&gl;')
s = s.replace('"', '&quot;')

return s 
"""