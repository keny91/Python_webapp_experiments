#Functions that compliment main.py


import cgi

# method vars
def ROT13_onlyChar(s):
  #change only caracters and maintain simbols such as " ", "?","!"
  #FROM A to M  +13, FROM M to Z -13

  #This function will be only applied to characters and will not modify other punctuation simbols
  #num=ord(char)
  #char=chr(num)

  # a - z
  for i in range(0,len(s)):
      asc=ord(s[i])
      #print asc
      if(asc>=97 and asc<=122):
          s=s[0:i]+chr(((asc+13-97)%26)+97)+s[i+1:]

      elif(asc>=65 and asc<=90):
          s=s[0:i]+chr(((asc+13-65)%26)+65)+s[i+1:]


  return html_escape (s)


  

def ROT13(s, lower_limit, upper_limit):

  # m is the last caracter that +13  ( +12 gets to m included)
  # Transformation into unused symbols
  mid_term =lower_limit+((upper_limit-lower_limit)/2)
  print "midterm", mid_term
  print (upper_limit-lower_limit)

  for i in range(lower_limit,upper_limit+1):
    
    #print i , i-lower_limit  DEBUG
    s = s.replace(chr(i), chr(i-lower_limit))


    
      
    
    #CONVERSION FROM UNUSED SYMBOLS TO ROT13
  for j in range(0,upper_limit-lower_limit+1):
    if j <= (upper_limit-lower_limit)/2:
      s = s.replace(chr(j), chr(lower_limit+j+13))
      #print j, (lower_limit+j+13)  DEBUG
    else:
      s = s.replace(chr(j), chr(lower_limit+j-13))
      #print j, (lower_limit+j-13)


  return s









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

































