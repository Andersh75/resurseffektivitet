from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask import jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload, aliased
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
import requests
import xmltodict
import json
from flask import json
from sqlalchemy import exists
import csv
from datetime import date, datetime, timedelta
from operator import itemgetter
import string
from sqlalchemy.sql import and_, or_, not_
import cookielib
import mechanize




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f31'
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


subjects_classes = db.Table('subjects_classes',
    db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id')),
    db.Column('classes_id', db.Integer, db.ForeignKey('classes.id'))
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



class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    classes = db.relationship('Classes', secondary=subjects_classes, backref=db.backref('subjects', lazy='dynamic'))


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
    akafirstname = db.Column(db.String(100))
    akalastname = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    initials = db.Column(db.String(3), unique=True)
    password = db.Column(db.String(30))
    kthid = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(100))
    examiner = db.relationship('Courses', backref='examiner', lazy='dynamic', foreign_keys='[Courses.examiner_id]')
    responsible = db.relationship('Courses', backref='responsible', lazy='dynamic', foreign_keys='[Courses.responsible_id]')
    assistantone = db.relationship('Courses', backref='assistantone', lazy='dynamic', foreign_keys='[Courses.assistantone_id]')
    assistanttwo = db.relationship('Courses', backref='assistanttwo', lazy='dynamic', foreign_keys='[Courses.assistanttwo_id]')
    classes = db.relationship('Classes', secondary=teachers_classes, backref=db.backref('teachers', lazy='dynamic'))


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    period = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    studentsexpected = db.Column(db.Integer)
    studentsregistred = db.Column(db.Integer)
    startweek = db.Column(db.String(30))
    endweek = db.Column(db.String(30))
    classes = db.relationship('Classes', backref='courses', lazy='dynamic')
    examiner_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    responsible_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    assistantone_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    assistanttwo_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))


class Classtypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classtype = db.Column(db.String(30))
    classes = db.relationship('Classes', backref='classtypes', lazy='dynamic')


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    starttime = db.Column(db.Integer)
    endtime = db.Column(db.Integer)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    dates_id = db.Column(db.Integer, db.ForeignKey('dates.id'))
    classtypes_id = db.Column(db.Integer, db.ForeignKey('classtypes.id'))






class RegistrationForm(Form):
    initials = TextField('Initials', [validators.Length(min=2, max=20)])
    firstname = TextField('First name', [validators.Length(min=2, max=20)])
    lastname = TextField('Last name', [validators.Length(min=2, max=30)])
    email = TextField('Email Address', [validators.Length(min=7, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])





def scheduleInCourse(course):
# Lista med kurstillfallen som anvands i en kurs
    templist = []
    tempvar = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.id == course).order_by(Dates.date).order_by(Classes.starttime).all()
    for item in tempvar:
        print "x"
        templist.append(item)
    return templist

def roomsOnDate(date, course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Rooms.id).distinct().join(Rooms.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).filter(Courses.id == course).all()
    for item in tempvar:
        templist.append(item)
    return templist

def defteachersondate(date, course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname, Teachers.initials, Teachers.id).distinct().join(Teachers.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).filter(Courses.id == course).all()
    for item in tempvar:
        templist.append(item)
    return templist

def idtocode(courseid):
    tempvar = db.session.query(Courses.code).filter(Courses.id == courseid).first()
    print tempvar[0]
    return tempvar[0]



def allcourses():
    templist = db.session.query(Courses).order_by(Courses.code).all()
    return templist

def allrooms():
    templist = db.session.query(Rooms).order_by(Rooms.name).all()
    return templist

def allteachers():
    templist = db.session.query(Teachers).order_by(Teachers.akalastname).all()
    return templist

def roomsperroomtype(roomtypeid):
    templist = db.session.query(Rooms).join(Rooms.roomtypes).filter(Roomtypes.id == roomtypeid).order_by(Rooms.name).all()
    return templist

def onescoursesexaminerorresponsible(teacherid):
    examiner = aliased(Teachers)
    responsible = aliased(Teachers)
    templist = db.session.query(Courses).join(examiner, Courses.examiner).join(responsible, Courses.responsible).filter(or_(examiner.id == teacherid, responsible.id == teacherid)).all()

    return templist



def onescoursesresponsible(teacherid):
    templist = db.session.query(Courses).join(Courses.responsible).filter(Teachers.id == teacherid).all()

    return templist

def onescoursesteaching(teacherid):
    templist = db.session.query(Courses).join(Courses.classes).join(Classes.teachers).distinct().filter(Teachers.id == teacherid).all()

    return templist

def onescoursesexaminer(teacherid):
    templist = db.session.query(Courses).join(Courses.responsible).filter(Teachers.id == teacherid).all()

    return templist

def onesteachingincourse(courseid, teacherid):
    templist = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Classes.teachers).join(Classes.courses).filter(and_(Courses.id == courseid, Teachers.id == teacherid)).all()

    return templist

def onesslots(teacherid):
    templist = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id, Courses.code, Courses.id).distinct().join(Dates.classes).join(Classes.teachers).join(Classes.courses).filter(Teachers.id == teacherid).order_by(Dates.date).order_by(Classes.starttime).all()

    return templist


def roomsslots(roomid):
    templist = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id, Courses.code, Courses.id).distinct().join(Dates.classes).join(Classes.teachers).join(Classes.courses).join(Classes.rooms).filter(Rooms.id == roomid).order_by(Dates.date).order_by(Classes.starttime).all()

    return templist






def roomtypesuseincourse(courseid, roomtypeid):
    templist = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Classes.rooms).join(Rooms.roomtypes).join(Classes.courses).filter(and_(Courses.id == courseid, Roomtypes.id == roomtypeid)).all()

    return templist[0][0]



def sumofroomtypesuseincourse(courseid):
    templist = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Classes.rooms).join(Rooms.roomtypes).join(Classes.courses).filter(and_(Courses.id == courseid, Roomtypes.id.isnot(None))).all()

    return templist[0][0]


def sumofonesteachingincourse(courseid):
    templist = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Classes.teachers).join(Classes.courses).filter(and_(Courses.id == courseid, Teachers.id.isnot(None))).all()

    return templist

def sumofonesteachingincourseperroomtype(courseid, roomtypeid):
    templist = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Classes.teachers).join(Classes.rooms).join(Rooms.roomtypes).join(Classes.courses).filter(and_(Courses.id == courseid, Teachers.id.isnot(None), Roomtypes.id == roomtypeid)).all()

    return templist[0][0]


def sumofonesteachingincourseperroomtypeperhour(courseid, roomtypeid):

    varx = sumofonesteachingincourseperroomtype(courseid, roomtypeid)
    vary = roomtypesuseincourse(courseid, roomtypeid)
    #varz = float(varx[0][0]) / vary[0][0]
    print "varx"
    print varx
    print "vary"
    print vary

    varz = 0

    if varx and vary:
        varz = float(varx) / float(vary)

    return str(varz)[:4]


def roomtypeobjectfromid(roomtypeid):
    testvar = db.session.query(Roomtypes).filter(Roomtypes.id == roomtypeid).first()
    #print testvar.password
    return testvar

def roomobjectfromid(roomid):
    testvar = db.session.query(Rooms).filter(Rooms.id == roomid).first()
    #print testvar.password
    return testvar

def courseobjectfromid(courseid):
    testvar = db.session.query(Courses).filter(Courses.id == courseid).first()
    #print testvar.password
    return testvar

def myobject():
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    #print testvar.password
    return db.session.query(Teachers).filter(Teachers.email == session['user']).first()

def myobjectfromid(teacherid):
    testvar = db.session.query(Teachers).filter(Teachers.id == teacherid).first()
    #print testvar.password
    return testvar

def mycoursesexaminerorresponsible():
    examiner = aliased(Teachers)
    responsible = aliased(Teachers)
    templist = db.session.query(Courses).join(examiner, Courses.examiner).join(responsible, Courses.responsible).filter(or_(examiner.email == session['user'], responsible.email == session['user'])).all()
    #templist = db.session.query(Courses).join(examiner, Courses.examiner).join(responsible, Courses.responsible).all()
    #print templist
    return templist

def mycoursesresponsible():
    templist = db.session.query(Courses).join(Courses.responsible).filter(Teachers.email == session['user']).all()

    return templist

def mycoursesteaching():
    templist = db.session.query(Courses).join(Courses.classes).join(Classes.teachers).distinct().filter(Teachers.email == session['user']).all()

    return templist

def mycoursesexaminer():
    templist = db.session.query(Courses).join(Courses.responsible).filter(Teachers.email == session['user']).all()

    return templist


def myslots():
    templist = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id, Courses.code, Courses.id).distinct().join(Dates.classes).join(Classes.teachers).join(Classes.courses).filter(Teachers.email == session['user']).order_by(Dates.date).order_by(Classes.starttime).all()

    return templist

def roomsonslot(slotid):
    templist = db.session.query(Rooms.name, Rooms.id).distinct().join(Rooms.classes).filter(Classes.id == slotid).all()

    return templist

def teachersonslot(slotid):
    templist = db.session.query(Teachers.initials, Teachers.id).join(Teachers.classes).filter(Classes.id == slotid).all()

    return templist






def subjectsinslot(slotid):
    templist = db.session.query(Subjects).join(Subjects.classes).filter(Classes.id == slotid).all()
    for item in templist:
        print item.id
    return templist

def teachersincourse(courseid):
    templist = db.session.query(Teachers).join(Teachers.classes).join(Classes.courses).distinct().filter(Courses.id == courseid).all()

    return templist


def roomtypesincourse(courseid):
    templist = db.session.query(Roomtypes).join(Roomtypes.rooms).join(Rooms.classes).join(Classes.courses).distinct().filter(Courses.id == courseid).all()

    return templist

def mycourseslist():
    templist = db.session.query(Teachers.email).all()

    tempvar = "[{"
    id = 1
    for item in templist[:-1]:
        #print item
        tempvar = tempvar + " id: " + str(id) + ", text: '" + item[0] + "' }, {"
        id = id + 1
    tempvar = tempvar + " id: '" + str(id) + "', text: '" + templist[-1][0] + "' }]"

    #print tempvar
    #tempvar2 = "[{ id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }]"
    #print testvar.password
    return tempvar

def subjectslistjson():
    templist = db.session.query(Subjects.name).all()

    tempvar = "[{"
    id = 1
    for item in templist[:-1]:
        #print item
        tempvar = tempvar + " id: " + str(id) + ", text: '" + item[0] + "' }, {"
        id = id + 1
    tempvar = tempvar + " id: '" + str(id) + "', text: '" + templist[-1][0] + "' }]"

    #print tempvar
    #tempvar2 = "[{ id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }]"
    #print testvar.password
    return tempvar






def amiexaminer(code):
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    already = db.session.query(exists().where(and_(Courses.code==code, Courses.examiner==testvar))).scalar()
    return already

def amiresponsible(code):
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    already = db.session.query(exists().where(and_(Courses.code==code, Courses.responsible==testvar))).scalar()
    return already

def amiteaching(code):
    testvar = db.session.query(Courses).join(Teachers.classes).join(Classes.courses).filter(and_(Teachers.email==session['user'], Courses.code==code)).first()
    #print testvar
    already = False
    if testvar:
        print testvar.code
        already = True
    return already

app.jinja_env.globals.update(roomsslots=roomsslots, roomobjectfromid=roomobjectfromid, roomtypeobjectfromid=roomtypeobjectfromid, roomsperroomtype=roomsperroomtype, courseobjectfromid=courseobjectfromid, onesslots=onesslots, myobjectfromid=myobjectfromid, sumofonesteachingincourseperroomtypeperhour=sumofonesteachingincourseperroomtypeperhour, sumofonesteachingincourseperroomtype=sumofonesteachingincourseperroomtype, sumofonesteachingincourse=sumofonesteachingincourse, sumofroomtypesuseincourse=sumofroomtypesuseincourse, roomtypesuseincourse=roomtypesuseincourse, roomtypesincourse=roomtypesincourse, onesteachingincourse=onesteachingincourse, subjectslistjson=subjectslistjson, subjectsinslot=subjectsinslot, teachersincourse=teachersincourse, onescoursesteaching=onescoursesteaching, onescoursesresponsible=onescoursesresponsible, onescoursesexaminerorresponsible=onescoursesexaminerorresponsible, onescoursesexaminer=onescoursesexaminer, allteachers=allteachers, mycoursesteaching=mycoursesteaching, teachersonslot=teachersonslot, roomsonslot=roomsonslot, myslots=myslots, idtocode=idtocode, defteachersondate=defteachersondate, roomsOnDate=roomsOnDate, scheduleInCourse=scheduleInCourse, allcourses=allcourses, amiteaching=amiteaching, amiresponsible=amiresponsible, amiexaminer=amiexaminer, myobject=myobject, mycoursesexaminerorresponsible=mycoursesexaminerorresponsible, mycoursesexaminer=mycoursesexaminer, mycoursesresponsible=mycoursesresponsible, mycourseslist=mycourseslist)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap






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

    with open('static/subjects.csv', 'rb') as f:
        reader = csv.reader(f)
        subjects_list = list(reader)

    with open('static/courses.csv', 'rb') as f:
        reader = csv.reader(f)
        courses_list = list(reader)

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

    for i in subjects_list:
        #print i[0]
        name = db.session.query(exists().where(Subjects.name==i[0])).scalar()
        if not name:
            record = Subjects(**{
                'name' : i[0]
            })
            db.session.add(record)
            db.session.commit()


    for i in teachers_list:
        already = db.session.query(exists().where(or_(Teachers.kthid==i[0], Teachers.initials==i[1], Teachers.email==i[2]))).scalar()

        if not already:
            if len(i[0]) < 1:
                i[0] = None
            if len(i[1]) < 1:
                i[1] = None
            if len(i[2]) < 1:
                i[2] = None
            if i[0] or i[2]:
                record = Teachers(**{
                    'kthid' : i[0],
                    'initials' : i[1],
                    'email' : i[2],
                    'firstname' : i[3],
                    'akafirstname' : i[3],
                    'akalastname' : i[4],
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

        try:
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

        except Exception, e:
            varcode = "no URL"
            print varcode + " " + item

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


def courseinfoperyearandterm(x, y):
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

            #print coursecode, roundid, startterm, period, year
            term = roundid

            tempdict = {'coursecode':coursecode, 'year':year, 'term':term, 'period':period, 'startterm':startterm}

            templist2.append(tempdict)

    tempdict2 = {'year':x, 'round':y, 'courseinfo':templist2}

    return tempdict2


def coursesfromdepartment(templist):
    for itemlist in templist:
        print itemlist
        for item in itemlist:
            print item
            name = item['name']
            code = item['code']
            examiner = item['examiner']
            department = item['department']

            tempdict = {}
            already = db.session.query(exists().where(Courses.code==code)).scalar()
            print "already"
            existingexamner = db.session.query(exists().where(Teachers.email==examiner)).scalar()
            #print existingexamner
            if (not already) and existingexamner:
                print "(not already) and existingexamner"
                #print examiner
                if name and code and (examiner != "no email"):
                    tempdict['name'] = name
                    tempdict['code'] = code
                    tempdict['examiner_id'] = Teachers.query.filter_by(email=examiner).first().id
                    record = Courses(**tempdict)
                    db.session.add(record)
                    db.session.commit()
                    print tempdict

            if already and existingexamner:
                #print code
                print examiner
                tempobj = db.session.query(Courses).filter(Courses.code==code).first()
                tempobj.name = name
                tempobj.examiner_id = Teachers.query.filter_by(email=examiner).first().id
                db.session.commit()
                #print tempdict
    print "DONE"


def coursesfromdepartment2(item):

    code = item['coursecode']
    print "YYY"
    print code
    year = item['year']
    term = item['term']
    period = item['period']
    responsible = item['emailcourseresponsible']
    startweek = item['startweek']
    endweek = item['endweek']


    tempdict = {}
    already = db.session.query(exists().where(and_(Courses.code==code, Courses.year==year))).scalar()

    if (not already):
        print "NOT ALREADY"
        tempdict['code'] = code
        tempdict['year'] = year
        tempdict['term'] = term
        tempdict['period'] = period
        tempdict['startweek'] = startweek
        tempdict['endweek'] = endweek
        print tempdict['startweek']
        tempdict['responsible_id'] = Teachers.query.filter_by(email=responsible).first().id
        print "BEFOR ENDWEEK"
        record = Courses(**tempdict)
        db.session.add(record)
        db.session.commit()
        print "ENDWEEK"



    if already:
        print "ALREADY"
        tempobj = db.session.query(Courses).filter(and_(Courses.code==code, Courses.year==year)).first()
        tempobj.responsible_id = Teachers.query.filter_by(email=responsible).first().id
        db.session.commit()



def coursesfromdepartment3(templist):
    for itemlist in templist:
        print itemlist
        for item in itemlist:
            #print item
            name = item['name']
            code = item['code']
            examiner = item['examiner']
            department = item['department']
            print name
            latestcourse = db.session.query(Courses).filter(Courses.code==code).order_by(Courses.code.desc()).first()
            print latestcourse
            latestcourse.name = name
            latestcourse.examiner_id = Teachers.query.filter_by(email=examiner).first().id
            db.session.commit()
            #print tempdict
    #print "DONE"


def addcoursestotables_first(tempdict):

    for item in tempdict['courseinfo']:
        coursecode = item['coursecode']
        print "XXX"
        print coursecode
        year = item['year']
        term = item['term']
        period = item['period']
        if period < 3:
            roundid = period
        else:
            roundid = period - 2

        try:
            req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s/round/%s:%s/%s' % (coursecode, year, term, roundid))
            xml = BeautifulSoup(req)

            #print coursecode
            #print year
            #print term
            #print roundid

            courseround = xml.find('courseround')

            endweek = courseround['endweek']
            startweek = courseround['startweek']

            print endweek
            print startweek

            courseresponsible = xml.find('courseresponsible')
            emailcourseresponsible = courseresponsible['primaryemail']
            print emailcourseresponsible

            item['emailcourseresponsible'] = emailcourseresponsible
            item['startweek'] = startweek
            item['endweek'] = endweek

            coursesfromdepartment2(item)

        except Exception, e:
            varcode = "no name"
            print varcode




def teachersfromdepartment(templist):
    for xitem in templist:
        #print xitem
        #print xitem['department']

        department = xitem['department']

        for item in xitem['teacher']:
            print item
            firstname = item['firstname']
            lastname = item['lastname']
            email = item['email']
            username = item['username']

            if (email != "no email"):
                print "XXXXX"
                tempdict = {}
                tempdict['firstname'] = firstname
                tempdict['lastname'] = lastname
                tempdict['email'] = email
                tempdict['username'] = username
                tempdict['department'] = department

                already = db.session.query(exists().where(or_(Teachers.username==username, Teachers.email==email))).scalar()
                if not already:
                    print "ZZZZZ"
                    record = Teachers(**tempdict)
                    db.session.add(record)
                    db.session.commit()
                else:
                    print "already"
                    tempobj = db.session.query(Teachers).filter(or_(Teachers.username==username, Teachers.email==email)).first()
                    print tempobj.firstname.encode('utf-8')
                    tempobj.firstname = firstname
                    tempobj.lastname = lastname
                    tempobj.email = email
                    tempobj.username = username
                    tempobj.department = department
                    print tempobj.department.encode('utf-8')
                    db.session.commit()

        print "YYYYYY"




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

#NOT READY
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



@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:

        if request.method == "POST":

            attempted_email = request.form['email']
            attempted_password = request.form['password']

            xrubrik = db.session.query(Teachers).filter(Teachers.email == attempted_email).first()

            flash(xrubrik.email)
            #flash(attempted_password)

            if attempted_email == xrubrik.email and attempted_password == xrubrik.password:
                session['logged_in'] = True
                #session['username'] = request.form['initials']
                session['user'] = request.form['email']
                return redirect(url_for('login_page'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)


@app.route('/register/', methods=["GET","POST"])
def register_page():

    form = RegistrationForm(request.form)
    #flash("Before IF")

    if request.method == "POST" and form.validate():
            initials  = form.initials.data
            akafirstname  = form.firstname.data
            akalastname  = form.lastname.data
            email = form.email.data
            password = form.password.data
            already = db.session.query(exists().where(Teachers.email==email)).scalar()
            if not already:
                flash("Your email is not in the db")
                return render_template('register.html.j2', form=form)


            alreadyregistred = db.session.query(exists().where(and_(Teachers.password!=None, Teachers.email==email))).scalar()

            if alreadyregistred:
                flash("Already registred!")
                return redirect(url_for('login_page'))

            existinginitials = db.session.query(exists().where(Teachers.initials==initials)).scalar()

            if existinginitials:
                tempobj = db.session.query(Teachers).filter(Teachers.email==email).first()
                if tempobj.initials != initials:
                    flash("Initials are already taken")
                    return render_template('register.html.j2', form=form)



            flash("Thanks for registering!")
            flash(email)
            tempobj = db.session.query(Teachers).filter(Teachers.email==email).first()
            tempobj.akafirstname = akafirstname
            tempobj.akalastname = akalastname
            tempobj.password = password
            tempobj.initials = initials
            db.session.commit()
            return redirect(url_for('login_page'))


    flash("Please register!")
    return render_template("register.html.j2", form=form)

@app.route("/logout/")
@login_required
def logout():
    session.pop('user', None)
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login_page'))

@app.route('/rooms')
@app.route('/rooms/<int:page>')
def rooms_page(page=1):
    return render_template('rooms.html.j2', page=page)

@app.route('/teachers')
@app.route('/teachers/<int:page>')
def teachers_page(page=1):
    return render_template('teachers.html.j2', page=page)

@app.route('/courses')
@app.route('/courses/<int:page>')
def courses_page(page=1):
    return render_template('courses.html.j2', page=page)

@app.route('/allcourses')
@app.route('/allcourses/<int:page>')
def allcourses_page(page=1):
    return render_template('allcourses.html.j2', page=page)

@app.route('/allrooms')
@app.route('/allrooms/<int:page>')
def allrooms_page(page=1):
    return render_template('allrooms.html.j2', page=page)


@app.route('/allteachers')
@app.route('/allteachers/<int:page>')
def allteachers_page(page=1):
    return render_template('allteachers.html.j2', page=page)

@app.route('/oneteacher')
@app.route('/oneteacher/<int:teacherid>')
def oneteacher_page(teacherid=1):
    return render_template('oneteacher.html.j2', teacherid=teacherid)




@app.route('/onecourse')
@app.route('/onecourse/<int:courseid>')
def onecourse_page(courseid=1):
    return render_template('onecourse.html.j2', courseid=courseid)

@app.route('/oneroom')
@app.route('/oneroom/<int:roomid>')
def oneroom_page(roomid=1):
    return render_template('oneroom.html.j2', roomid=roomid)

@app.route('/oneslot')
@app.route('/oneslot/<int:slotid>')
def oneslot_page(slotid=1):
    return render_template('oneslot.html.j2', slotid=slotid)


@app.route('/myteaching')
@app.route('/myteaching/<int:page>')
def myteaching_page(page=1):
    return render_template('myteaching.html.j2', page=page)

@app.route('/myinfo')
@app.route('/myinfo/<int:page>')
def myinfo_page(page=1):
    return render_template('myinfo.html.j2', page=page)




@app.route('/user_edit_myinfo/akafirstname', methods=['GET', 'POST'])
def user_edit_myinfo_akafirstname():
    id = request.form["pk"]
    tempobj = db.session.query(Teachers).get(id)
    tempobj.akafirstname = request.form["value"]

    db.session.commit()

    result = {}

    return json.dumps(result)
@app.route('/user_edit_myinfo/akalastname', methods=['GET', 'POST'])
def user_edit_myinfo_akalastname():
    id = request.form["pk"]
    tempobj = db.session.query(Teachers).get(id)
    tempobj.akalastname = request.form["value"]

    db.session.commit()

    result = {}

    return json.dumps(result)
@app.route('/user_edit_myinfo/initials', methods=['GET', 'POST'])
def user_edit_myinfo_initials():
    id = request.form["pk"]
    tempobj = db.session.query(Teachers).get(id)
    tempobj.initials = request.form["value"]

    db.session.commit()

    result = {}

    return json.dumps(result)









@app.route('/user_edit_course/responsible', methods=['GET', 'POST'])
def user_edit_course_responsible():
    id = request.form["pk"]
    tempobj = db.session.query(Courses).get(id)
    tempobj.responsible = db.session.query(Teachers).filter(Teachers.email == request.form["value"]).first()

    db.session.commit()

    result = { 'id': id, 'text': request.form["value"] }

    return json.dumps(result)



@app.route('/user_edit_content/<int:page>', methods=['GET', 'POST'])
def user_edit_content(page):
    id = request.form["pk"]

    #varcode = id.split(',')[0]
    #varclassid = id.split(',')[1]
    #print varcode
    #print varclassid
    print id
    print "hej"

    #templist = []

    #templist = scheduleInCourse(varcode)
    #print templist

    #for item in templist:
    #   print item


    varteacher = db.session.query(Classes).get(id)
    print varteacher.content.encode('utf-8')
    #print varteacher.firstname.encode('utf-8')
    #print request.form["value"].encode('utf-8')
    varteacher.content = request.form["value"]
    print "Efter"
    print varteacher.content.encode('utf-8')
    #varteacher = Teachers.query.get(id)
    #print varteacher.firstname.encode('utf-8')
    result = {}
    db.session.commit()
    return json.dumps(result)







@app.route('/')
def index():
    print "HE"
    return redirect(url_for('login_page'))

'''    templist = xml.find("table")
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
'''

@app.route('/testlogin')
def testlogin():
    tempdict3 = courseinfoperyearandterm(2017, 1)


    for item in tempdict3['courseinfo']:
        coursecode = item['coursecode']
        year = item['year']
        term = item['term']
        period = item['period']
        if period < 3:
            roundid = period
        else:
            roundid = period - 2



        try:
            req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s/round/%s:%s/%s' % (coursecode, year, term, roundid))
            xml = BeautifulSoup(req)

            #print coursecode
            #print year
            #print term
            #print roundid

            courseround = xml.find('courseround')

            endweek = courseround['endweek']
            startweek = courseround['startweek']

            print endweek
            print startweek

            courseresponsible = xml.find('courseresponsible')
            emailcourseresponsible = courseresponsible['primaryemail']
            print emailcourseresponsible





        except Exception, e:
            varcode = "no name"
            print varcode

    return 'Some response'



    '''
        # Browser
    br = mechanize.Browser()

    # Enable cookie support for urllib2
    cookiejar = cookielib.LWPCookieJar()
    br.set_cookiejar( cookiejar )

    # Broser options
    br.set_handle_equiv( True )
    br.set_handle_gzip( True )
    br.set_handle_redirect( True )
    br.set_handle_referer( True )
    br.set_handle_robots( False )

    # ??
    br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )

    br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

    # authenticate
    br.open( 'https://login.kth.se/login/' )

    for form in br.forms():
        print form.name
    br.select_form(nr=0)
    # these two come from the code you posted
    # where you would normally put in your username and password
    br[ "username" ] = 'ahell'
    br[ "password" ] = '-Gre75kger-'
    res = br.submit()

    print "Success!\n"

    url = br.open('https://www.kth.se/internt/minasidor/kurs/delt/?ccode=AI1147&term=V17')

    returnPage = url.read()

    return returnPage






    with requests.Session() as c:
        url = 'https://login.kth.se/login'
        USERNAME = 'ahell'
        PASSWORD = '-Gre75kger-'
        c.get(url)
        logdata = dict(username=USERNAME, password=PASSWORD)
        c.post(url, data=logdata, headers={"Referer": "https://www.kth.se/"})
        page = c.get('https://www.kth.se/internt/minasidor/kurs/delt/?ccode=AI1147&term=V17')

    return page.content
    '''

@app.route('/restartall')
def restartall():

    createtables()

    #csvimporter()

    tempdict = {}
    tempdict2 = {}
    tempdict3 = {}

    templist = []
    templist2 = []
    templist3 = []

    departments = ["AIB", "AIC", "AID", "AIE"]

    '''
    for item in departments:

        tempdict2 = staffperdepartment(item)
        print tempdict2
        templist2.append(tempdict2)

    #ADD ALL TEACHERS TO DB
    teachersfromdepartment(templist2)

    '''


    

    '''

    tempdict20151 = courseinfoperyearandterm(2015, 1)
    tempdict20152 = courseinfoperyearandterm(2015, 2)
    tempdict20161 = courseinfoperyearandterm(2016, 1)
    tempdict20162 = courseinfoperyearandterm(2016, 2)
    tempdict20171 = courseinfoperyearandterm(2017, 1)

    addcoursestotables_first(tempdict20151)
    addcoursestotables_first(tempdict20152)
    addcoursestotables_first(tempdict20161)
    addcoursestotables_first(tempdict20162)
    addcoursestotables_first(tempdict20171)
    '''

    for item in departments:
        #print item
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        #print tempdict
        templist.append(jsonifycoursesfromdepartment(tempdict))



    #ADD ALL COURSES TO DB
    coursesfromdepartment3(templist)



    print "QQqqqqqqqqqqqqqqqqqqqqQQQ"

    return "restartall"






@app.errorhandler(404)
def page_not_found(e):
    #xrubrik = db.session.query(Courses.code).filter(Courses.id == 17).first()
    #xkurskod = db.session.query(Courses.name).filter(Courses.id == 17).first()
    #return render_template('blocks.html.j2', varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=17)
    return "fel"







if __name__ == "__main__":
    app.secret_key = 'asdasdasdasdasd'
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run(host='0.0.0.0', port=1080)
