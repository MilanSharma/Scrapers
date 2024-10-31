#!/usr/bin/python


import urllib
import urllib2
from bs4 import BeautifulSoup
import MySQLdb
import datetime


db = MySQLdb.connect("localhost","root","root","lok")
cursor=db.cursor()
cursor.execute("SELECT * FROM attendance WHERE status = '0'")

results = cursor.fetchall()
db.commit()
db.close()

for row in results:
    session = row[0]
    date = row[1]
    status = row[2]

    db = MySQLdb.connect("localhost","root","root","lok")
    cursor=db.cursor()
    cursor.execute("DELETE from data WHERE date = %s",(date))                
    db.commit()
    db.close()    

    dt = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    new_date = '{0}/{1}/{2:02}'.format(dt.month, dt.day, dt.year)
    url = "http://164.100.47.132/Members_Attendance16/datewise_results.aspx?xlok=16&vsession="+str(session)+"&vdoa="+str(new_date)    

       
    f = urllib2.urlopen(url)
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

         user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/33.0"
         
         headers = { 'User-Agent' : user_agent  }

         DATA = urllib.urlencode(params)
         DATA = DATA.encode('utf-8')
   
         request = urllib2.Request(url, DATA, headers) 
 
         f = urllib2.urlopen(request)

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
                         if not div.isspace(): 
                          db = MySQLdb.connect("localhost","root","root","lok")
                          cursor=db.cursor()  
                          cursor.execute ("INSERT ignore INTO data (session,date,ic_no,name,attendance) VALUES (%s, %s, %s, %s, %s);", (session, date ,div, name, attendance))
                          db.commit()
                          db.close()
      	                 else:
                          db = MySQLdb.connect("localhost","root","root","lok")
                          cursor=db.cursor()  
                          cursor.execute ("INSERT ignore INTO data (session,date,name,attendance) VALUES (%s, %s, %s, %s);", (session, date , name, attendance))
                          db.commit()
                          db.close()
                          
    db = MySQLdb.connect("localhost","root","root","lok")
    cursor=db.cursor()  
    cursor.execute ("UPDATE attendance SET status = '1' WHERE date=%s;", date) 
    db.commit()
    db.close()        
    


