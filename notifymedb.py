#!/usr/bin/env python
import MySQLdb
import pynotify
from datetime import datetime
import getpass

#declaration
show="show tables"
create="create table notify(id int NOT NULL PRIMARY KEY AUTO_INCREMENT,name varchar(32),eventdate date,description varchar(100),type int)"
select="select name,day(eventdate),month(eventdate),year(eventdate),description,type from notify"
delete="delete from notify where id=%s"
delete1="select id,eventdate,type from notify"
login="create table login(username varchar(32),password varchar(32))"
count=0
text=""
val=0
check=0
#database connectivity
db=MySQLdb.connect("localhost","root","your_sql_db_password","your_sql_database_name")
cursor=db.cursor()


def createev():

    #table creation
    cursor.execute(show)
    table=cursor.fetchall()
    count=0

    for row in table:
        if row[0]=="notify":
            count=count+1
    if count==0:
        cursor.execute(create)
        db.commit()
        print "table created"

    count=0

    for row in table:
        if row[0]=="login":
            count=count+1
    if count==0:
        cursor.execute(login)
        db.commit()
        print "table created"

    #deletion
def deleteev(x):
    cursor.execute(delete1)
    deletion=cursor.fetchall()
    for row in deletion:
        y=x.date()
        if(row[2]==0 and row[1]<y):
            cursor.execute(delete,(row[0],))
            db.commit()

def retrieve(x):
    check=0
    val=0
    cursor.execute("select username from login")
    data=cursor.fetchall()
    for row in data:
                check=1
                pynotify.init("Display")
                notice=pynotify.Notification("Hi "+row[0],"Events Are Loading ...")
                notice.show()

    if(check==0):
                print "Register Username And Password"
                print "------------------------------"
                usr=raw_input('Username: ')
                pwd=getpass.getpass('Password: ')
                cursor.execute("insert into login values(%s,%s)",(usr,pwd,))
                db.commit()

    cursor.execute(select)
    data=cursor.fetchall()
    for row in data:
        if(row[5]==1):
            if(x.day==row[1] and x.month==row[2]):
                val=1
                pynotify.init("Display")
                notice=pynotify.Notification(row[0],row[4])
                notice.show()
        if(row[5]==0):
            if(x.day==row[1] and x.month==row[2] and x.year==row[3]):
                val=1
                pynotify.init("Display")
                notice=pynotify.Notification(row[0],row[4])
                notice.show()
        if(row[5]==2):
                val=1
                pynotify.init("Display")
                notice=pynotify.Notification(row[0],row[4])
                notice.show()

    if(val==0 and check==1):
            pynotify.init("Display")
            notice=pynotify.Notification("Sorry","No Events Today")
            notice.show()



try:
    x=datetime.today()
    createev()
    retrieve(x)
    deleteev(x)
except KeyboardInterrupt:
    print "\n"
    print "Bye \n"
    exit()
db.close()
