#!/usr/bin/python
  
from urllib import urlencode
import urllib2
from bs4 import BeautifulSoup
import urllib
import MySQLdb
import re
import time

start_time = time.time()

fg = open('result.txt','w+')
for x in range(1,31468): #input range from 1 till 31468 only
  url = 'http://judis.nic.in/supremecourt/imgst.aspx?filename='+str(x)
  try:
   f = urllib2.urlopen(url)
  except:
   fg.write(str(x)+'\n\n'+'Bad Status!'+'\n\n') 
   continue 

  s = f.read()
  soup = BeautifulSoup(s)
 
  if soup.find_all('textarea'):
    textarea = soup.find_all('textarea')
    text = textarea[0].string   
    try:
     text = text.encode('utf-8')
    except:
    # fg.write(str(x)+'\n\n'+'No Text!'+'\n\n') 
     continue


    if re.findall("CASE NO\.:\s*(.*)", str(text)):
     CASE_NO = re.findall("CASE NO\.:\s*(.*)", str(text))
     case_no = re.split('\n\s*\n', CASE_NO[0])  
    else:  
     case_no = ['Null']    

    if re.findall("PETITIONER:\s*(.*)", str(text)):
      PETITIONER = re.findall("PETITIONER:\s*(.*)", str(text))
      petitioner = re.split('\n\s*\n', PETITIONER[0])
    else:
      petitioner = ['Null']

    if re.findall("RESPONDENT:\s*(.*)", str(text)):
      RESPONDENT = re.findall("RESPONDENT:\s*(.*)", str(text)) 
      respondent = re.split('\n\s*\n', RESPONDENT[0])
    else:
      respondent = ['Null']

    if re.findall("DATE OF JUDGMENT:\s*(.*)", str(text)):
      DATE = re.findall("DATE OF JUDGMENT:\s*(.*)", str(text))
      date = re.split('\n\s*\n', DATE[0])
    elif re.findall("DATE OF JUDGMENT.*(\d{2}\/\d{2}\/\d{4})", str(text)):  
      DATE = re.findall("DATE OF JUDGMENT.*(\d{2}\/\d{2}\/\d{4})", str(text))
      date = re.split('\n\s*\n', DATE[0])
    elif re.findall("DATE OF JUDGMENT.*(\d\/\d{2}\/\d{4})", str(text)):  
      DATE = re.findall("DATE OF JUDGMENT.*(\d\/\d{2}\/\d{4})", str(text))
      date = re.split('\n\s*\n', DATE[0])
    else:
      date=['Null'] 

    if re.findall("DATE OF JUDGMENT.*BENCH:\s*(.*)", str(text), re.S):
     BENCH = re.findall("DATE OF JUDGMENT.*BENCH:\s*(.*)", str(text), re.S)
     bench = re.split('\n\s*\n', BENCH[0])
    elif  re.findall("BENCH:.*BENCH:\s*(.*)", str(text), re.S):
     BENCH = re.findall("BENCH:.*BENCH:\s*(.*)", str(text), re.S)
     bench = re.split('\n\s*\n', BENCH[0])
    else:
     bench = ['Null']    


    if re.findall("CITATION:\s*(.*)ACT:", str(text), re.S): 
     CITATION = re.findall("CITATION:\s*(.*)ACT:", str(text), re.S)
     citation = re.split('\n\s*\n', CITATION[0])
    elif re.findall("CITATION:\s*(.*)HEADNOTE:", str(text), re.S): 
     CITATION = re.findall("CITATION:\s*(.*)HEADNOTE:", str(text), re.S)
     citation = re.split('\n\s*\n', CITATION[0])
    elif re.findall("CITATION:\s*(.*)JUDGMENT:", str(text), re.S): 
     CITATION = re.findall("CITATION:\s*(.*)JUDGMENT:", str(text), re.S)
     citation = re.split('\n\s*\n', CITATION[0])
    else:
     citation = ['Null']


    if re.findall("ACT:\s*(.*)HEADNOTE:", str(text), re.S):
     ACT = re.findall("ACT:\s*(.*)HEADNOTE:", str(text), re.S)
     act = re.split('\n\s*\n', ACT[0])
    elif re.findall("ACT:\s*(.*)JUDGMENT:", str(text), re.S):
     ACT = re.findall("ACT:\s*(.*)JUDGMENT:", str(text), re.S)
     act = re.split('\n\s*\n', ACT[0])
    else:
     act = ['Null']
 

    if re.findall("HEADNOTE:\s*(.*)JUDGMENT:", str(text), re.S):
     HEADNOTE = re.findall("HEADNOTE:\s*(.*)JUDGMENT:", str(text), re.S)
     headnote = re.split('\n\s*\n', HEADNOTE[0])
    else:
     headnote = ['NULL']
 
 
    if re.findall("DATE OF JUDGMENT:.*JUDGMENT:\s*(.*)", str(text), re.S):
     JUDGMENT = re.findall("DATE OF JUDGMENT:.*JUDGMENT:\s*(.*)", str(text), re.S)
    elif re.findall("DATE OF JUDGMENT.*JUDGMENT:\s*(.*)", str(text), re.S):
     JUDGMENT = re.findall("DATE OF JUDGMENT.*JUDGMENT:\s*(.*)", str(text), re.S)
    else:
     JUDGMENT = ['Null']

#    judgment = re.split('\n\s*\n', JUDGMENT[0])


    db = MySQLdb.connect("localhost","root","password","judge")
    cursor=db.cursor()  
    cursor.execute ("DELETE FROM data1 WHERE case_no=%s AND petitioner=%s AND respondent=%s AND date=%s AND bench=%s AND citation=%s AND act=%s AND headnote=%s AND judgment=%s", (case_no[0], petitioner[0], respondent[0] ,date[0], bench[0], citation[0], act[0], headnote[0],JUDGMENT[0])) 
    cursor.execute ("INSERT ignore INTO data1 (case_no,petitioner,respondent,date,bench,citation,act,headnote,judgment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (case_no[0], petitioner[0], respondent[0] ,date[0], bench[0], citation[0], act[0], headnote[0],JUDGMENT[0]))
    db.commit()
    db.close()

    
#    fg.write(str(case_no[0])+'\n\n'+str(petitioner[0])+'\n\n'+str(respondent[0])+'\n\n'+str(date[0])+'\n\n'+str(bench[0])+'\n\n'+str(citation[0])+'\n\n'+str(act[0])+'\n\n'+str(headnote[0])+'\n\n'+str(JUDGMENT[0])+'\n\n')
    print str(x)
  else:
    continue

print("--- %s seconds ---" % (time.time() - start_time))
