#!/usr/bin/python

import urllib2
import MySQLdb
from bs4 import BeautifulSoup


url= 'http://164.100.47.4/Members_attendance/sessionwiseresults.aspx?vsessionno=235'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
table = soup.find('table', {'id':'GridView1'})
s = soup.find_all('span')
date = soup.find('span', {'id':'lb_period'}).string
sittings = soup.find('span', {'id':'lb_sittings'}).string



for row in table.find_all('tr', {'bgcolor':'White'}):
  
       col=row.find_all('td') 
        
       serial = col[0].string
       seat  = col[1].string
       name = col[2].string
       state = col[3].string
       attendance = col[4].string  
          
       db = MySQLdb.connect("localhost","root","root","rajya")
       cursor=db.cursor()  
       cursor.execute ("INSERT ignore INTO data (serial,seat_no,name,state,attendance) VALUES (%s, %s, %s, %s, %s);", (serial, seat ,name, state, attendance))
       db.commit()
       db.close()
      
          
      
         
                  
                 

