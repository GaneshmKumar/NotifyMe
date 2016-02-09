#!/usr/bin/env python
import Tkinter as tk
from Tkinter import *
import datetime

#Database Connection
import MySQLdb
db=MySQLdb.connect("localhost","root","samepassword","ganesh")
cursor=db.cursor()

#Variable Declaration
m=0
d=0
y=0
text=""

#Login
def login():
    msg.delete('1.end',tk.END)
    msg.delete(tk.CURRENT,tk.END)
    cursor.execute("select username,password from login")
    data=cursor.fetchall()
    for row in data:
        if(row[1]==passtext.get()):
            passtext.delete(0,35)
            addb.config(state=tk.NORMAL)
            delb.config(state=tk.NORMAL)
            chkb.config(state=tk.NORMAL)
            enterb.config(state=tk.DISABLED)
            lockb.config(state=tk.NORMAL)
            clearb.config(state=tk.NORMAL)
            uname=Label(main,text="Hi "+row[0] +" :)",font=('cosmicsans',35),fg='white',bg='#4169e1')
            changeb.config(state=tk.NORMAL)
            uname.place(x=660,y=220)
        else:
            passtext.delete(0,10)
            msg.insert(tk.END,"WRONG PASSWORD")
            return

#Lock
def lock():
    passtext.delete(0,35)
    msg.delete('1.end',tk.END)
    msg.delete(tk.CURRENT,tk.END)
    addb.config(state=tk.DISABLED)
    delb.config(state=tk.DISABLED)
    chkb.config(state=tk.DISABLED)
    enterb.config(state=tk.NORMAL)
    lockb.config(state=tk.DISABLED)
    changeb.config(state=tk.DISABLED)
    clearb.config(state=tk.DISABLED)

#Change
def change():
    msg.delete('1.end',tk.END)
    msg.delete(tk.CURRENT,tk.END)
    if(passtext.get()==""):
        msg.insert(tk.END,"Password Cannot Be Empty")
        return
    else:
        cursor.execute("select username from login")
        u=cursor.fetchall()
        for row in u:
            cursor.execute("update login set password=%s where username=%s",(passtext.get(),row[0],))
            db.commit()
            msg.insert(tk.END,"Password Updated Successfully")
            passtext.delete(0,20)

#Add
def add():
        eid=0
        message=""
        desc=""
        msg.delete('1.0',tk.END)
        name=addEnamet.get()
        if(name==""):
            msg.insert(tk.END,"Please Enter A Name \n")
        else:
            date=day(0)
            if(date!=None):
                x=convert(date)
                if(addEdesct.get()==""):
                    desc=""
                else:
                    desc=addEdesct.get()
                if(var.get()=="Remaind Only Once"):
                    t=0
                elif(var.get()=="Remaind Every Year"):
                    t=1
                else:
                    t=2

                cursor.execute("Insert into notify(id,name,eventdate,description,type) values(%s,%s,%s,%s,%s)",(eid,name,x,desc,t))
                print "y"
                msg.insert(tk.END,"Event Added Successfully\n")
                addEnamet.delete(0,30)
                addEdayt.delete(0,3)
                addEmontht.delete(0,3)
                addEyeart.delete(0,5)
                addEdesct.delete(0,5)
                var.set("Remaind Only Once")
                db.commit()

#Delete
def delete():
    msg.delete('1.0',tk.END)
    name=addEnamet.get()
    if(name==""):
        msg.insert(tk.END,"Please Enter The  Name Of The Event To Be Deleted \n")
    else:
        date=addEyeart.get()+"-"+addEmontht.get()+"-"+addEdayt.get()
        if(date==""):
            msg.insert(tk.END,"Please Enter The Date Of The Event To Be Deleted \n")
        else:
            x=convert(date)
            cursor.execute("delete from notify where name=%s and eventdate=%s",(name,x))
            db.commit()
            msg.insert(tk.END,"Event Deleted Successfully \n")
            addEnamet.delete(0,30)
            addEdayt.delete(0,3)
            addEmontht.delete(0,3)
            addEyeart.delete(0,5)
            addEdesct.delete(0,5)
            var.set("Remaind Only Once")

#Check
def check():
    text=""
    data=""
    x="1111-11-11"
    val=0
    msg.delete('1.end',tk.END)
    msg.delete(tk.CURRENT,tk.END)
    name=addEnamet.get()
    if(name==""):
        if(addEyeart.get()=="" or  addEmontht.get()=="" or addEdayt.get()==""):
            msg.insert(tk.END,"Please Enter A Name or A Date or Both To Check")
            return
    if(addEyeart.get()!="" and  addEmontht.get()!="" and addEdayt.get()!=""):
        date=addEyeart.get()+"-"+addEmontht.get()+"-"+addEdayt.get()
    else:
        date=""
    if(name=="" and date!=""):
        x=convert(date)
        cursor.execute("select name,eventdate,description,type from notify where eventdate=%s",(x,))
        data=cursor.fetchall()
    elif(name!="" and date==""):
        cursor.execute("select name,eventdate,description,type from notify where name=%s",(name,))
        data=cursor.fetchall()
    elif(name!="" and date!=""):
        x=convert(date)
        cursor.execute("select name,eventdate,description,type from notify where name=%s and eventdate=%s",(name,x,))
        data=cursor.fetchall()

    for row in data:
        val=1
        if(row[2]==""):
            desc="None"
        else:
            desc=row[2]
        if(row[3]==0):
            etype="Remaind Once"
        elif(row[3]==1):
            etype="Remaind Every Year"
        else:
            etype="Remaind Daily"
        date=str(row[1])
        text="Event Name: "+row[0]+"\n----------\n"+"Event Date: "+date+"\n----------\n"+"Description: "+desc+"\n-----------\n"+"Event Type: "+etype+"\n----------\n\n"
        msg.insert(tk.END,text)
    addEnamet.delete(0,35)
    addEdayt.delete(0,3)
    addEmontht.delete(0,3)
    addEyeart.delete(0,5)
    addEdesct.delete(0,35)
    var.set("Remaind Only Once")
    f=open("db.txt","r")
    if(val==0):
        msg.insert(tk.END,"No Events To Display")
        return

#Clear
def clear():
    msg.delete('0.end',tk.END)
    msg.delete(tk.INSERT,tk.END)

#Day
def day(val):
    if(val!=1):
        if(addEdayt.get()==""):
            msg.insert(tk.END,"Please Enter A Day \n")
        if(addEmontht.get()==""):
            msg.insert(tk.END,"Please Enter A Month \n")
        if(addEyeart.get()==""):
            msg.insert(tk.END,"Please Enter A Year \n")
    if(addEdayt.get()!="" and addEmontht.get()!="" and addEyeart.get()!=""):
        d=addEdayt.get()
        dint=int(d)
        if(dint<01 or dint>31):
            msgtxt.insert(tk.END,"Enter A Valid Day")
        else:
            date=month(dint,day)
            return date

#Month
def month(dint,d):
    m=addEmontht.get()
    mint=int(m)
    if(mint<01 or mint>12):
        msgtxt.insert(tk.END,"Enter A Valid Month")
    if(mint==4 or mint==6  or mint==9 or mint==11):
        if(dint==31):
                msgtxt.insert(tk.END,"This Month Do Not Have Day 31")
        if(mint==2):
            if(dint==30 or dint==31):
                msgtxt.insert(tk.END,"This Month Do Not Have Day 30 and 31")
        else:
            date=year(mint,dint,m,d)
            return date
    else:
        date=year(mint,dint,m,d)
        return date

#Year
def year(mint,dint,m,d):
    leap=0
    y=addEyeart.get()
    yint=int(y)
    if(yint<2015):
        msgtxt.insert(tk.END,"Cannot Set Remainder For The Past")
    else:
        if(mint==2 and dint==29):
            if(yint/4==0):
                if(yint/100==0):
                    if(yint/400==0):
                        leap=1
            if(leap!=1):
                msgtxt.insert(tk.END,"Month 2 Do Not Have Day 29 In The Year",y)
        else:
            date=addEyeart.get()+"-"+addEmontht.get()+"-"+addEdayt.get()
            return date

#Convertor
def convert(date):
        x=datetime.datetime.strptime(date,"%Y-%m-%d").date()
        return x

#main
main=Tk()
main.configure(background='#4169e1')
main.attributes('-zoomed',True)
main.title("Notify Me :)")

#Today
date=datetime.datetime.today().date()
datestr=str(date)
todaydate=Label(main,text="Today: "+datestr,font=('productsans',25),fg='white',bg='#4169e1')
todaydate.place(x=870,y=320)

#title
title=Label(main,text="Notify Me :)",font=('comicsans',35),fg='white',bg='#4169e1')
title.place(x=160,y=70)
#password
passlabel=Label(main,text="Password",font=('productsans',15),fg='white',bg='#4169e1')
passlabel.place(x=160,y=160)

passetext=Text(main)
passtext=Entry(main,relief='ridge',highlightcolor='black',font='productsans',show="*",width=35,takefocus=1)
passtext.place(x=160,y=200)

enterb=Button(main,text="Enter",state=tk.NORMAL,font=('productsans',10),command=login,relief='flat',width=8)
enterb.place(x=160,y=250)

lockb=Button(main,text="Lock",state=tk.DISABLED,font=('productsans',10),command=lock,relief='flat',width=8)
lockb.place(x=290,y=250)

changeb=Button(main,text="Change",state=tk.DISABLED,font=('productsans',10),command=change,relief='flat',width=8)
changeb.place(x=421,y=250)

#Event Name
addEnamel=Label(main,text="Event Name",font=('productsans',15),fg='white',bg='#4169e1')
addEnamel.place(x=160,y=330)

addEnamet=Entry(main,relief='ridge',highlightcolor='black',font='productsans',width=35,takefocus=1)
addEnamet.place(x=160,y=370)

#Event Date
addEdatel=Label(main,text="Date\ndd mm yyyy",font=('productsans',15),fg='white',bg='#4169e1')
addEdatel.place(x=160,y=430)

addEdayt=Entry(main,relief='ridge',highlightcolor='black',font='productsans',width=2,takefocus=1)
addEdayt.place(x=160,y=490)

addEmontht=Entry(main,relief='ridge',highlightcolor='black',font='productsans',width=2,takefocus=1)
addEmontht.place(x=200,y=490)

addEyeart=Entry(main,relief='ridge',highlightcolor='black',font='productsans',width=4,takefocus=1)
addEyeart.place(x=240,y=490)

#Event Type
addEtypel=Label(main,text="Type",font=('productsans',15),fg='white',bg='#4169e1')
addEtypel.place(x=340,y=450)

var=StringVar()
addEtypeo=OptionMenu(main,var,'Remaind Only Once','Remaind Every Year','Remaind Daily')
var.set("Remaind Only Once")
addEtypeo.place(x=340,y=490)

#Event Description
addEdescl=Label(main,text="Event Description",font=('productsans',15),fg='white',bg='#4169e1')
addEdescl.place(x=160,y=560)
addEdesct=Entry(main,relief='ridge',highlightcolor='black',font='productsans',width=35,takefocus=1)
addEdesct.place(x=160,y=600)

#Add Delete Check
addb=Button(main,text="Add",state=tk.DISABLED,font=('productsans',10),command=add,relief='flat',width=8)
addb.place(x=160,y=660)

delb=Button(main,text="Delete",state=tk.DISABLED,font=('productsans',10),command=delete,relief='flat',width=8)
delb.place(x=288,y=660)
chkb=Button(main,text="Check",state=tk.DISABLED,font=('productsans',10),command=check,relief='flat',width=8)
chkb.place(x=420,y=660)

#Message Box
addEmsgl=Label(main,text="Message",font=('productsans',15),fg='white',bg='#4169e1')
addEmsgl.place(x=660,y=330)
msg=Text(main,width=75,height=16)
msg.place(x=660,y=370)
msgtxt=""
msg.insert(tk.INSERT,msgtxt)
clearb=Button(main,text="Clear",state=tk.DISABLED,font=('productsans',10),command=clear,relief='flat',width=63)
clearb.place(x=660,y=660)

#Max char
maxchar1=Label(main,text="Max-Characters:35",font=('productsans',10),fg='white',bg='#4169e1')
maxchar1.place(x=390,y=170)
maxchar2=Label(main,text="Max-Characters:35",font=('productsans',10),fg='white',bg='#4169e1')
maxchar2.place(x=390,y=340)
maxchar3=Label(main,text="Max-Characters:35",font=('productsans',10),fg='white',bg='#4169e1')
maxchar3.place(x=390,y=570)
mainloop()
