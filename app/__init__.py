from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask import jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from xml.etree import ElementTree as ET
from socket import *
from functools import wraps
from decimal import Decimal
from bs4 import BeautifulSoup
import gc
import urllib
import urllib2
from urllib2 import urlopen
import xmltodict
import json
from flask import json
from sqlalchemy import exists
import csv
from datetime import date, datetime, timedelta
from operator import itemgetter
import string
from sqlalchemy.sql import and_, or_, not_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f14'
db = SQLAlchemy(app)


teachers_classes = db.Table('teachers_classes',
    db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('classes_id', db.Integer, db.ForeignKey('classes.id'))
)

rooms_classes = db.Table('rooms_classes',
    db.Column('rooms_id', db.Integer, db.ForeignKey('rooms.id')),
    db.Column('classes_id', db.Integer, db.ForeignKey('classes.id'))
)

dates_courses = db.Table('dates_courses',
    db.Column('dates_id', db.Integer, db.ForeignKey('dates.id')),
    db.Column('courses_id', db.Integer, db.ForeignKey('courses.id'))
)

dates_rooms = db.Table('dates_rooms',
    db.Column('dates_id', db.Integer, db.ForeignKey('dates.id')),
    db.Column('rooms_id', db.Integer, db.ForeignKey('rooms.id'))
)

dates_teachers = db.Table('dates_teachers',
    db.Column('dates_id', db.Integer, db.ForeignKey('dates.id')),
    db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id'))
)

# One-to-many. Parent to Rooms
class Roomtypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomtype = db.Column(db.String(30))
    cost = db.Column(db.Integer)
    rooms = db.relationship('Rooms', backref='roomtypes', lazy='dynamic')

# One-to-many. Child to Roomtypes
class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    seats = db.Column(db.Integer)
    roomtypes_id = db.Column(db.Integer, db.ForeignKey('roomtypes.id'))
    classes = db.relationship('Classes', secondary=rooms_classes, backref=db.backref('rooms', lazy='dynamic'))


class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    courses = db.relationship('Courses', secondary=dates_courses, backref=db.backref('dates', lazy='dynamic'))
    rooms = db.relationship('Rooms', secondary=dates_rooms, backref=db.backref('dates', lazy='dynamic'))
    teachers = db.relationship('Teachers', secondary=dates_teachers, backref=db.backref('dates', lazy='dynamic'))
    classes = db.relationship('Classes', backref='dates', lazy='dynamic')


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    initials = db.Column(db.String(3), unique=True)
    password = db.Column(db.String(30))
    kthid = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(100))
    examiner = db.relationship('Courses', backref='examiner', lazy='dynamic', foreign_keys='[Courses.examiner_id]')
    responsible = db.relationship('Courses', backref='responsible', lazy='dynamic', foreign_keys='[Courses.responsible_id]')
    classes = db.relationship('Classes', secondary=teachers_classes, backref=db.backref('teachers', lazy='dynamic'))


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    classes = db.relationship('Classes', backref='courses', lazy='dynamic')
    examiner_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    responsible_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    starttime = db.Column(db.Integer)
    endtime = db.Column(db.Integer)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    dates_id = db.Column(db.Integer, db.ForeignKey('dates.id'))


### CREATE TABLES
def createtables():
    db.create_all()
    db.session.commit()

###Import CSV-file and transform imported CSV to tables
def csvimporter():
    with open('static/teachers.csv', 'rb') as f:
        reader = csv.reader(f)
        teachers_list = list(reader)

    with open('static/roomtypes.csv', 'rb') as f:
        reader = csv.reader(f)
        roomtypes_list = list(reader)

    with open('static/rooms.csv', 'rb') as f:
        reader = csv.reader(f)
        rooms_list = list(reader)

    with open('static/courses.csv', 'rb') as f:
        reader = csv.reader(f)
        courses_list = list(reader)

    with open('static/roles.csv', 'rb') as f:
        reader = csv.reader(f)
        roles_list = list(reader)

    with open('static/schedules.csv', 'rb') as f:
        reader = csv.reader(f)
        schedules_list = list(reader)


    schedules_list = remove_col(schedules_list, 0)

    schedules_list = reformat_date(schedules_list)

    schedules_list = add_col(schedules_list)

    schedules_list = add_col(schedules_list)

    schedules_list = extract_start_slut_tid(schedules_list)

    schedules_list = remove_col(schedules_list, 1)






    #for i in schedules_list:
    #    print i




    #Populate tables
    for i in roomtypes_list:
        roomtype = db.session.query(exists().where(Roomtypes.roomtype==i[0])).scalar()
        if not roomtype:
            record = Roomtypes(**{
                'roomtype' : i[0],
                'cost' : i[1]
            })
            db.session.add(record)
            db.session.commit()


    for i in rooms_list:
        #print i[0]
        name = db.session.query(exists().where(Rooms.name==i[0])).scalar()
        if not name:
            record = Rooms(**{
                'name' : i[0],
                'seats' : i[1],
                'roomtypes_id' : Roomtypes.query.filter_by(id=i[2]).first().id
            })
            db.session.add(record)
            db.session.commit()


    for i in teachers_list:
        already = db.session.query(exists().where(or_(Teachers.kthid==i[0], Teachers.initials==i[1], Teachers.email==i[2]))).scalar()
        if not already:
            record = Teachers(**{
                'kthid' : i[0],
                'initials' : i[1],
                'email' : i[2],
                'firstname' : i[3],
                'lastname' : i[4]
            })
            db.session.add(record)
            db.session.commit()


    for i in courses_list:
        already = db.session.query(exists().where(and_(Courses.code==i[0], Courses.year==i[3]))).scalar()
        if not already:
            record = Courses(**{
                'code' : i[0],
                'name' : i[1],
                'schedule_exists' : i[2],
                'year' : i[3]
            })
            db.session.add(record)
            db.session.commit()


    for i in schedules_list:
        if not Dates.query.filter_by(date=i[0]).first():
            #print "dubbel"
        #else:
            record = Dates(**{
                'date' : i[0]
                })
            db.session.add(record)
            db.session.commit()


    for i in schedules_list:
        already = db.session.query(exists().where(and_(Classes.content==i[3], Classes.starttime==i[7], Classes.endtime==i[8], Classes.courses_id==Courses.query.filter_by(code=i[5]).first().id, Classes.dates_id==Dates.query.filter_by(date=i[0]).first().id))).scalar()
        if (not already) and (len(i[3]) < 100):
            record = Classes(**{
                #'date' : i[0],
                'content' : i[3],
                'starttime' : i[7],
                'endtime' : i[8],
                'courses_id' : Courses.query.filter_by(code=i[5]).first().id,
                'dates_id' : Dates.query.filter_by(date=i[0]).first().id
            })
            db.session.add(record)
            db.session.commit()

            coursevar = Courses.query.filter_by(code=i[5]).first()
            datevar = Dates.query.filter_by(date=i[0]).first()
            #print datevar.date
            datevar.courses.append(coursevar)
            #datevar.classes.append(record)
            db.session.commit()


            words = i[4].split()
            for word in words:
                #print word

                already = db.session.query(exists().where(Teachers.initials==word)).scalar()

                if already:
                    teachervar = Teachers.query.filter_by(initials=word).first()
                    #print teachervar.firstname
                    teachervar.classes.append(record)
                    teachervar.dates.append(datevar)
                    db.session.commit()

            words = i[2].split()
            for word in words:

                already = db.session.query(exists().where(Rooms.name==word)).scalar()

                if already:
                    roomvar = Rooms.query.filter_by(name=word).first()
                    #print roomvar.name
                    roomvar.classes.append(record)
                    roomvar.dates.append(datevar)

                    db.session.commit()

### CLEAN THE CSV
# Remove Column from Table
def remove_col(list1, i):
    temp_list_suf = []
    temp_list_pre = []
    temp_list = []
    for n in list1:
        temp_list_suf.append(n[i+1:])
        temp_list_pre.append(n[:i])
    for index, item in enumerate(list1):
        temp_list.append(temp_list_pre[index] + temp_list_suf[index])
    return temp_list
# Reformat date
def reformat_date(list1):
    i = 0
    for p in range(0, len(list1)):
        year_var = "2016"
        if list1[p][i][2] == "/":
            day_var = list1[p][i][:2]
            #print day_var
        else:
            day_var = "0" + list1[p][i][:1]
            #print day_var
        if list1[p][i][-3] == "/":
            #print "hej"
            month_var = list1[p][i][-2:]
            #print month_var
        else:
            month_var = "0" + list1[p][i][-1:]
            #print month_var

        #print list1[p][7]
        if list1[p][7]:
            year_var = list1[p][7]

        list1[p][i] = year_var + "-" + month_var + "-" + day_var
        year_var = "2016"

        #print list1[p][7]
    return list1
# Insert Column to Table
def add_col(list1):
    for i in range(0, len(list1)):
        list1[i].append("")
    return list1
# Extract beginning and end time
def extract_start_slut_tid(list1):
     i = 1
     for p in range(0, len(list1)):
        list1[p][-2] = list1[p][i][0:2]
        list1[p][-1] = list1[p][i][3:5]
        # print list1[p][i]

     return list1
# Separate teachers
def separate_teachers(list1):
    temp_list = []
    for p in range(0, len(list1)):
        words = list1[p][4].split()
        for word in words:
            #print word
            alist = []
            alist = list1[p]
            alist[4] = word

            #print alist
            temp_list.extend(alist)
            #print "hej"

    #print temp_list



    return temp_list
# Separate teachers
def separate_rooms(list1):
    temp_list = []
    for p in range(0, len(list1)):
        words = list1[p][2].split()
        for word in words:
            #print word
            alist = []
            alist = list1[p]
            alist[2] = word

            #print alist
            temp_list.extend(alist)
            #print "hej"

    return temp_list











def fetchinglistofcodesfordepartmentcourses(department):
    j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/%s.json' % (department))

    j_obj = json.load(j)

    tempdict = {}
    templist =[]

    for item in j_obj['courses']:
        #print item['code']
        templist.append(item['code'])

    tempdict = {'department':j_obj['department'], 'courses':templist}

    return tempdict


def jsonifycoursesfromdepartment(tempdict):

    templist2 = []
    tempdict2 = {}

    for item in tempdict['courses']:
        req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s' % (item))

        xml = BeautifulSoup(req)


        #varname = xml.title.string
        try:
            varcode = xml.course['code']
            #print varcode

        except Exception, e:
            varcode = "no name"
            #print varcode


        try:
            varmail = xml.examiner['primaryemail']
            #print varmail

        except Exception, e:
            varmail = "no email"
            #print varmail


        try:
            varname = xml.title.string
            #print varname.encode('utf-8')
            #print varname

        except Exception, e:
            varname = "no name"
            #print varname

        tempdict2 = {'code':varcode, 'name':varname, 'examiner':varmail, 'department':tempdict['department']}

        templist2.append(tempdict2)

    return templist2


def staffperdepartment(department):
    req = urllib2.urlopen('https://www.kth.se/directory/a/%s' % (department))

    xml = BeautifulSoup(req)

    templist = xml.find("table")
    templist = templist.find("tbody")
    templist = templist.findAll("tr")

    templist2 = []
    tempdict = {}

    for tr in templist:
        tdlist = tr.findAll("a")
        #print tdlist[1]['href']
        firstname = tdlist[2].text
        lastname = tdlist[1].text
        email = tdlist[3].text
        username = tdlist[1]['href'][27:]
        #print username

        tempdict = {'firstname':firstname, 'lastname':lastname, 'email':email, 'username':username}
        templist2.append(tempdict)


    tempdict2 = {'department':department, 'teacher':templist2}

    return tempdict2


def courseinfoperyearandround(x, y):
    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/courseRounds/%s:%s' % (x, y))

    xml = BeautifulSoup(req)

    templist = xml.findAll("courseround")

    templist2 = []

    for item in templist:
        #print "1"
        #print item['coursecode']
        coursecode = item['coursecode']
        if coursecode[:2] == "AI":

            startterm = item['startterm']
            roundid = item['roundid']

            if int(startterm[-1:]) == 1:
                period = int(roundid) + 2
            else:
                period = int(roundid)

            year = startterm[:4]

            print coursecode, roundid, startterm, period, year

            tempdict = {'coursecode':coursecode, 'year':year, 'period':period, 'startterm':startterm, 'roundid':roundid}

            templist2.append(tempdict)

    tempdict2 = {'year':x, 'round':y, 'courseinfo':templist2}

    return tempdict2


def coursesfromdepartment(templist):
    for itemlist in templist:
        for item in itemlist:
            name = item['name']
            code = item['code']
            examiner = item['examiner']
            department = item['department']

            tempdict = {}
            ret = db.session.query(exists().where(Courses.code==code)).scalar()
            print ret
            ret2 = db.session.query(exists().where(Teachers.email==examiner)).scalar()
            print ret2
            if (not ret) and ret2:
                print code
                print examiner
                if name and code and (examiner != "no email"):
                    tempdict['name'] = name
                    tempdict['code'] = code
                    tempdict['examiner_id'] = Teachers.query.filter_by(email=examiner).first().id
                    record = Courses(**tempdict)
                    db.session.add(record)
                    db.session.commit()
                    print tempdict


def teachersfromdepartment(templist):
    for xitem in templist:
        #print xitem
        #print xitem['department']

        department = xitem['department']

        for item in xitem['teacher']:
            #print item
            firstname = item['firstname']
            lastname = item['lastname']
            email = item['email']
            username = item['username']

            if firstname and lastname and (email != "no email") and username:
                tempdict = {}
                tempdict['firstname'] = firstname
                tempdict['lastname'] = lastname
                tempdict['email'] = email
                tempdict['username'] = username
                tempdict['department'] = department

                already = db.session.query(exists().where(or_(Teachers.username==username, Teachers.email==email))).scalar()
                if not already:
                    record = Teachers(**tempdict)
                    db.session.add(record)
                    db.session.commit()
                else:
                    tempobj = db.session.query(Teachers).filter(or_(Teachers.username==username, Teachers.email==email)).first()
                    tempobj.firstname = firstname
                    tempobj.lastname = lastname
                    tempobj.email = email
                    tempobj.username = username




def xrestartall():
    tempdict = {}
    tempdict2 = {}
    tempdict3 = {}

    templist = []
    templist2 = []
    templist3 = []

    departments = ["AIB", "AIC", "AID", "AIE"]


    for item in departments:
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        templist.append(jsonifycoursesfromdepartment(tempdict))

        tempdict2 = staffperdepartment(item)
        templist2.append(tempdict2)


        #templist3.append(jsonifylitteraturefromdepartment(tempdict))

    #tempdict3 = courseinfoperyearandround(2016, 1)


    #ADD ALL TEACHERS TO DB
    teachersfromdepartment(templist2)

    #ADD ALL COURSES TO DB
    coursesfromdepartment(templist)




    #FETCH ALL LITERATURE
    #jsonifylitteraturefromdepartment()

    #FETCH CALENDAR
    #calTest()

    #testv = jsonify(tempdict3)


#NOT READY
def jsonifylitteraturefromdepartment():

    templist = []
    item = "AI1128"
    #for item in tempdict['courses']:
        #varname = xml.title.string
    try:
        req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s/plan' % (item))
        xml = BeautifulSoup(req)
        templist = xml.findAll("literature")
        for literature in templist:
            print literature
            print "######"
            print literature.string
            print "______"
            for child in literature.children:
                print child
                print "######"
                print child.string
                print "______"
                for child2 in child.children:
                    print child2
                    print "######"
                    print child2.string
                    print "______"


    except Exception, e:
        print "no literature"

#NOT READY
def calTest():
    req = urllib2.Request('https://www.kth.se/social/course/AI1146/calendar/ical/?lang=sv')
    response = urllib2.urlopen(req)
    data = response.read()
    for line in data.split('\n'):
        #print line
        print "######"
        if line.startswith('SUMMARY:'):
            print line
        if line.startswith('LOCATION:'):
            print line
        if line.startswith('DTSTART;VALUE=DATE-TIME:'):
            print line
        if line.startswith('DTEND;VALUE=DATE-TIME:'):
            print line


    return




@app.route('/')
def hello_world():
    #varcourse = Courses.query.get(1)
    #varcourse.responsible_id = 10
    #db.session.commit()

    #print db.session.query(Courses.code).join(Courses.responsible).filter(TEACHERS.firstname == "Maria").first()

    varuser = db.session.query(Teachers).filter(Teachers.firstname == "Berndt").first()

    '''
    #ADD FOREIGN KEY AS ID
    varcourse = db.session.query(Courses).join(Courses.examiner).filter(Teachers.firstname == "Kent").first()
    varcourse.responsible_id = 12
    db.session.commit()

    #ADD FOREIGN KEY AS OBJECT TO FIRST
    varcourse = db.session.query(Courses).join(Courses.examiner).filter(Teachers.firstname == "Kent").first()
    varcourse.responsible = varuser
    db.session.commit()

    #ADD FOREIGN KEY AS OBJECT TO ALL
    varcourse = db.session.query(Courses).join(Courses.examiner).filter(Teachers.firstname == "Berndt").all()
    for item in varcourse:
        item.responsible = varuser
    db.session.commit()

    #REPLACE FOREIGN KEY AS OBJECT TO ALL OF FILTERED
    varcourse = db.session.query(Courses).join(Courses.responsible).filter(Teachers.id == varuser.id).all()
    for item in varcourse:
        item.responsible = db.session.query(Teachers).filter(Teachers.firstname == "Anders").first()
    db.session.commit()
    '''

    #REPLACE FOREIGN KEY AS OBJECT TO ALL OF FILTERED
    varcourse = db.session.query(Courses).join(Courses.examiner).filter(Teachers.id == varuser.id).all()
    for item in varcourse:
        print "HEJ"
        print item.code


    return "testx"



@app.route('/restartall')
def restartall():

    #createtables()
    #csvimporter()

    tempdict = {}
    tempdict2 = {}
    tempdict3 = {}

    templist = []
    templist2 = []
    templist3 = []

    departments = ["AIB", "AIC", "AID", "AIE"]


    for item in departments:
        #tempdict = fetchinglistofcodesfordepartmentcourses(item)
        #templist.append(jsonifycoursesfromdepartment(tempdict))

        tempdict2 = staffperdepartment(item)
        templist2.append(tempdict2)


        #templist3.append(jsonifylitteraturefromdepartment(tempdict))

    #tempdict3 = courseinfoperyearandround(2016, 1)


    #ADD ALL TEACHERS TO DB
    teachersfromdepartment(templist2)

    #ADD ALL COURSES TO DB
    #coursesfromdepartment(templist)









    return "restartall"








if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
