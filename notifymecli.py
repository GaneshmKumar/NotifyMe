import datetime
import getpass

#Database connectivity
import MySQLdb
db=MySQLdb.connect("localhost","root","your_sql_db_password","your_sql_database_name")
cursor=db.cursor()

#variable declaration
t=0
d="0"
m="0"
y="0"
leap=0
'''def goodbye():
    print "bye"
    atexit.register(goodbye)'''

#Retype Password
def retype(username,newpassword):
    retypepassword=getpass.getpass('Retype New Password: ')
    if(newpassword!=retypepassword):
        print "Password Mismatch"
        retype(username,newpassword)
    else:
        cursor.execute("update login set password=%s where username=%s",(newpassword,username,))
        db.commit()
        print "Password Updated Successfully \n"
        option()

#Event Type
def evtype():
    eventtype=raw_input('Event Type (1.once/2.every year): ')
    if(eventtype=='1'):
        t=0
    elif(eventtype=='2'):
        t=1
    else:
        print "Enter Valid Event Type"
        evtype()

    return t
#Year
def year(mint,dint,m,d):
    leap=0
    y=raw_input('Year (yyyy): ')
    yint=int(y)
    if(yint<2015):
        print "Cannot Set Remainder For The Past"
        year(mint,dint,m,d)
    else:
        if(mint==2 and dint==29):
            if(yint/4==0):
                if(yint/100==0):
                    if(yint/400==0):
                        leap=1
            if(leap!=1):
                print "Month 2 Do Not Have Day 29 In The Year",y
                day()
    date=y+'-'+m+'-'+d
    return date

#Month
def month(dint,d):
    m=raw_input('Month (mm): ')
    mint=int(m)
    if(mint<01 or mint>12):
        print "Enter A Valid Month"
        month(dint,d)
    if(mint==4 or mint==6  or mint==9 or mint==11):
        if(dint==31):
                print "This Month Do Not Have Day 31"
                day()
        if(mint==2):
            if(dint==30 or dint==31):
                print "This Month Do Not Have Day 30 and 31"
                day()
    date=year(mint,dint,m,d)
    return date

#Day
def day():
    d=raw_input('Day (dd): ')
    dint=int(d)
    if(dint<01 or dint>31):
        print "Enter A Valid Day"
        day()
    else:
        date=month(dint,d)
        return date

#Quit
def quit():
    exit()

#check
def check():
    print "Check An Event"
    print "--------------"
    date=day()
    dates=datetime.datetime.strptime(date,'%Y-%m-%d').date()
    cursor.execute("select name,description,type from notify where eventdate=%s",(dates,))
    db.commit()
    data=cursor.fetchall()
    for row in data:11
        print "Event Name: ",row[0]
        print "Event Description: ",row[1]
        if(row[2]==0):
            print "Event Type: Once"
        else:
            print "Event Type: Every Year"
        print "\n"

#Change Password
def change():
    print "Change Password"
    print "---------------"
    log(1)

#Delete Event
def deleteevent():
        c=0
        print "Delete An Event"
        print "---------------"
        log(2)
        eventname=raw_input('Event Name: ')
        date=day()
        ddate=datetime.datetime.strptime(date,'%Y-%m-%d').date()
        cursor.execute("select id,name,eventdate from notify")
        data=cursor.fetchall()
        for row in data:
            if(row[2]==ddate):
                c=1
                if(row[1]==eventname):
                    cursor.execute("delete from notify where id=%s",(row[0],))
                    db.commit()
                    print "Event Deleted Successfully"
                    option()

        if(c==0):
            print "No Event Available In The Given Name \n"
            option()

#Add Event
def addevent():
    print "Add An Event"
    print "------------"
    iid=0
    eventname=raw_input('Event Name: ')
    date=day()
    ddate=datetime.datetime.strptime(date,'%Y-%m-%d').date()
    t=evtype()
    desc=raw_input('Event Description: ')
    cursor.execute("insert into notify(id,name,eventdate,description,type) values(%s,%s,%s,%s,%s)",(iid,eventname,ddate,desc,t))
    db.commit()
    print "Event Added Successfully \n"
    option()

#Option
def option():
    print "Select An Option To Continue"
    print "----------------------------"
    options=raw_input(' 1.Add \n 2.Delete \n 3.Change Password \n 4.Check \n 5.Quit \n')
    if(options=='1'):
        addevent()
    elif(options=='2'):
        deleteevent()
    elif(options=='3'):
        change()
    elif(options=='4'):
        check()
    elif(options=='5'):
        quit()
    else:
        option()

#Login
def log(ch):
    #username=raw_input('Username: ')
    cursor.execute("select username,password from login")
    data=cursor.fetchall()
    for row in data:
        print "Hi ",row[0]
        password=getpass.getpass('Password: ')
        if(ch==0):
            if(row[1]==password):
                print "Login Successful"
                print "Welcome ",row[0],"\n"
                option()
            else:
                print "Wrong Username Or Password"
                log(0)
        elif(ch==1):
            if(row[1]==password):
                newpassword=getpass.getpass('New Password: ')
                retype(row[0],newpassword)
        elif(ch==2):
            if(row[1]==password):
                print "Login Successful \n"
                return
            else:
                print "Wrong Username Or Password"
                log(2)

try:
    log(0)
except KeyboardInterrupt:
    print "\n"
    cursor.execute("select username from login")
    data=cursor.fetchall()
    for row in data:
        print "\n"
        if(row[0]!=""):
            print "Bye ",row[0]
        else:
            print "Bye"
    quit()
