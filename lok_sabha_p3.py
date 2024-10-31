#!/usr/bin/python3

import urllib
from urllib import request
import urllib.parse
from bs4 import BeautifulSoup

fh = open('lkattendance.txt', 'w')

########## Input the session range to scarpe data from particular session or multiple sessions ###############
##########                     To get data from all sessions make range (1,5)                  ###############                     

for session in range(3,4):
  url1 = "http://164.100.47.132/Members_Attendance16/datewise_attendance.aspx?xlok=16&vsessionno="+str(session)
  fh.write('Session '+str(session)+'\n')
  
  f = urllib.request.urlopen(url1)
  s = f.read()
  soup = BeautifulSoup(s)
  for p in soup.find_all("a"):
    link = p.get('href')
    url = "http://164.100.47.132/Members_Attendance16/"+link
    print (url)
    fh.write('Date'+' - '+str(link[46:])+'\n')
    
        
    f = urllib.request.urlopen(url)
    s = f.read()

    soup = BeautifulSoup(s)

    state = soup.find(attrs={"name" : "__VIEWSTATE"})
    v = state['value']

    valid = soup.find(attrs={"name" : "__EVENTVALIDATION"})
    e = valid['value']

    generator = soup.find(attrs={"name" : "__VIEWSTATEGENERATOR"})
    y = generator['value']

    for x in range(0,16):
         if x < 10:
           g = 'DataGrid1$ctl01$ctl0'+str(x)
         else:
           g = 'DataGrid1$ctl01$ctl'+str(x)
 
         params = {
         '__EVENTTARGET': g,
         '__EVENTARGUMENT': '',
         '__VIEWSTATE': v,
         '__VIEWSTATEGENERATOR': y,
         '__EVENTVALIDATION':e
         }

         DATA = urllib.parse.urlencode(params)
         DATA = DATA.encode('utf-8')
   
         request = urllib.request.Request(
         url, DATA) 

         request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
         request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/33.0")
         f = urllib.request.urlopen(request)

         soup = BeautifulSoup(f)
         table = soup.find_all('table', {'id':'DataGrid1'})
         for table1 in table:
                for row in table1.find_all('tr'):
               
                   if not row.find_all('td',{'align':'left'}):                
                        col = row.find_all('td')

                 
                        div = col[0].string
                        attendance = col[-1].string
                        name = col[int(len(col)/2)].string
      	                                            
                        if div and attendance is not None:
                            fh.write(str(div)+'\t\t'+str(attendance)+'\t\t'+str(name)+'\n')

  

f.close()

