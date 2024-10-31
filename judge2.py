#!/usr/bin/python
  
from urllib import urlencode
import urllib2
from bs4 import BeautifulSoup
import urllib
import MySQLdb
import re
import time

start_time = time.time()

fg = open('result2.txt','w+')
for x in range(31469,39790): #input range from 31469 till you please 39244
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
 #    fg.write(str(x)+'\n\n'+'No Text!'+'\n\n') 
     continue
     
     
    if re.findall("\s*(.*APPEAL\s{,2}N[Oo][\.\(]\s*.*)", str(text)):
     CASE_NO = re.findall("\s*(.*APPEAL\s{,2}N[Oo][\.\(]\s*.*)", str(text))
    elif re.findall("\s*(.*APPEAL\s{,2}N[Oo][Ss]\.\s*.*)", str(text)):
     CASE_NO = re.findall("\s*(.*APPEAL\s{,2}N[Oo][Ss]\.\s*.*)", str(text))
    elif re.findall("\s*(.*PETITION.*\s{,2}N[Oo]\.\s*.*)", str(text)):
     CASE_NO = re.findall("\s*(.*PETITION.*\s{,2}N[Oo]\.\s*.*)", str(text))
    elif re.findall("\s*(.*PETITION.*\s{,2}N[Oo][Ss]\.\s*.*)", str(text)):
     CASE_NO = re.findall("\s*(.*PETITION.*\s{,2}N[Oo][Ss]\.\s*.*)", str(text))
    else:
     CASE_NO = ['Null']
    ##print CASE_NO[0]
  
    if re.findall("(.*)\s*[\.*\s-][\.*\s-][\.*\s-][\.*\s-][\.*\s-][AP][PpEe][PpTt][EeIi][LlTt][LlIi]", str(text)):
     APPELANT =	 re.findall("(.*)\s*[\.*\s-][\.*\s-][\.*\s-][\.*\s-][\.*\s-][AP][PpEe][PpTt][EeIi][LlTt][LlIi]", str(text))  
    else:
     APPELANT = ['Null']     
    ##print APPELANT[0]     


    if re.findall("(.*)\s*[\.*\s-][\.*\s-][\.*\s-][\.*\s-][\.*\s-]R[Ee][Ss][Pp]", str(text)):
     RESPONDENT = re.findall("(.*)\s*[\.*\s-][\.*\s-][\.*\s-][\.*\s-][\.*\s-]R[Ee][Ss][Pp]", str(text))
    else:
     RESPONDENT = ['Null']
    ##print RESPONDENT[0]

    if re.findall("JUDGMENT\s*(.*)", str(text), re.S):
     JUDGMENT = re.findall("JUDGMENT\s*(.*)", str(text), re.S)
    elif re.findall("ORDER\s*(.*)", str(text), re.S):
     JUDGMENT = re.findall("ORDER\s*(.*)", str(text), re.S)    
    elif re.findall("J U D G M E N T\s*(.*)", str(text), re.S):
     JUDGMENT = re.findall("J U D G M E N T\s*(.*)", str(text), re.S)
    else:
     JUDGMENT = ['Null']
 
    
    if re.findall("[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\).*[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\).*[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\)", str(text), re.S):
      BENCH = re.findall("[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\).*[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\).*[\.*\s]{50}[Jj][\.*\s].*\((.{,30})\)", str(text), re.S)
      bench = '\n'.join(str(p) for p in BENCH[0])
      print '3 wins'
    elif re.findall("[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]].*[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S):
      BENCH = re.findall("[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]].*[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S)
      bench = '\n'.join(str(p) for p in BENCH[0]) 
      print '2 wins'
    elif re.findall("[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S):
      BENCH = re.findall("[\.*\s]{50}[Jj][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S)
      bench = BENCH[0] 
      print '1 wins'
    elif re.findall("[\.*\s]{50}[Jj.][\.*\s].*[\(\[](.{,30})[\)\]].*[\.*\s]{50}[Jj.][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S):
      BENCH = re.findall("[\.*\s]{50}[Jj.][\.*\s].*[\(\[](.{,30})[\)\]].*[\.*\s]{50}[Jj.][\.*\s].*[\(\[](.{,30})[\)\]]", str(text), re.S)
      bench = '\n'.join(str(p) for p in BENCH[0]) 
      print '0 wins'
    else: 
      BENCH = ['Null']
      bench = BENCH[0]
     
    if re.findall("[\.*\s]{50}[Jj.].*(\s*[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}\s{,2}\d{1,2}[,.]\s*2\d{3})", str(text), re.S):
      DATE = re.findall("[\.*\s]{50}[Jj.].*(\s*[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}\s{,2}\d{1,2}[,.]\s*2\d{3})", str(text), re.S) 
#      date = ''.join(str(p) for p in DATE[0])
    elif re.findall("[\.*\s]{50}[Jj.].*(\d\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S):
      DATE = re.findall("[\.*\s]{50}[Jj.].*(\d\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S) 
    elif re.findall("[\.*\s]{50}[Jj.].*(\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S):
      DATE = re.findall("[\.*\s]{50}[Jj.].*(\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S) 
    elif re.findall("[\.*\s]{50}[Jj.].*(\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S):
      DATE = re.findall("[\.*\s]{50}[Jj.].*(\d.*\s{,2}[JFMASOND][AaEePpUuCcOo][NnBbRrYyLlGgPpTtVvCc]\w{0,}[,.]\s*2\d{3})", str(text), re.S) 
    else:
      DATE = ['Null']
#      date = ['Null'] 


    print DATE[0]	

    db = MySQLdb.connect("localhost","root","password","judge")
    cursor=db.cursor()  
    cursor.execute ("DELETE FROM data WHERE case_no=%s AND petitioner=%s AND respondent=%s AND date=%s AND bench=%s AND judgment=%s", (CASE_NO[0], APPELANT[0], RESPONDENT[0] ,DATE[0], bench, JUDGMENT[0])) 
    cursor.execute ("INSERT ignore INTO data (case_no,petitioner,respondent,date,bench,judgment) VALUES (%s, %s, %s, %s, %s, %s);", (CASE_NO[0], APPELANT[0], RESPONDENT[0] , DATE[0], bench , JUDGMENT[0]))
    db.commit()
    db.close()


#    fg.write(str(x)+'\n\n'+str(CASE_NO[0])+'\n\n'+str(DATE[0])+'\n\n'+str(APPELANT[0])+'\n\n'+str(RESPONDENT[0])+'\n\n'+str(bench)+'\n\n')
    print str(x)
  else:
#    fg.write(str(x)+'\n\n'+'No Text!'+'\n\n')
    continue
    
print("--- %s seconds ---" % (time.time() - start_time))
