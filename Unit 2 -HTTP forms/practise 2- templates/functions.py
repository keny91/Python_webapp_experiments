#Functions that compliment main.py


import cgi
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

#  Match returns NONE if the string does not match the pattern
# RETURNs True if there is a match
def valid_username(username):
  return USER_RE.match(username) 
  # if not username:
  #   return False

  # else:
  #   return USER_RE.match(username)

# non- empty is OK
def valid_password(password):
  if not password: # caso no vacio
    return None

  else:
    return PASS_RE.match(password)


# 
def compare_passwords(password1,password2):
  if password1 == password2:
    return True
  else:
    return None
    

def valid_email(email):
  if not email: # if empty -> OK
    return True
  else:
    return EMAIL_RE.match(email)



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