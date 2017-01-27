from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask import jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func, UniqueConstraint
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
# import wget
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.by import By
# from pyvirtualdisplay import Display
# import re
# import urlparse
# from time import sleep
# from ghost import Ghost, Session
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# from PyQt4.QtWebKit import *
# import sys
# from lxml import html
# import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f42'
db = SQLAlchemy(app)


teachers_classes = db.Table('teachers_classes',
                            db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
                            db.Column('classes_id', db.Integer, db.ForeignKey('classes.id')),
                            UniqueConstraint('teachers_id', 'classes_id')
                            )

rooms_classes = db.Table('rooms_classes',
                         db.Column('rooms_id', db.Integer, db.ForeignKey('rooms.id')),
                         db.Column('classes_id', db.Integer, db.ForeignKey('classes.id')),
                         UniqueConstraint('rooms_id', 'classes_id')
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
    roomtype = db.Column(db.String(30), unique=True)
    cost = db.Column(db.Integer)
    rooms = db.relationship('Rooms', backref='roomtypes', lazy='dynamic')


# One-to-many. Child to Roomtypes
class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    seats = db.Column(db.Integer)
    roomtypes_id = db.Column(db.Integer, db.ForeignKey('roomtypes.id'))
    classes = db.relationship('Classes', secondary=rooms_classes, backref=db.backref('rooms', lazy='dynamic'))


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    classes = db.relationship('Classes', secondary=subjects_classes, backref=db.backref('subjects', lazy='dynamic'))


class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
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
    __table_args__ = (db.UniqueConstraint('code', 'year'),
                      )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    period = db.Column(db.Integer)
    roundid = db.Column(db.Integer)
    studentsexpected = db.Column(db.Integer)
    studentsregistred = db.Column(db.Integer)
    startweek = db.Column(db.String(30))
    endweek = db.Column(db.String(30))
    classes = db.relationship('Classes', backref='courses', lazy='dynamic')
    examiner_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    responsible_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    assistantone_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    assistanttwo_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    # UniqueConstraint('code', 'year')


class Classtypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classtype = db.Column(db.String(30), unique=True)
    classes = db.relationship('Classes', backref='classtypes', lazy='dynamic')


class Classes(db.Model):
    __table_args__ = (db.UniqueConstraint('starttime', 'endtime', 'courses_id', 'dates_id'),
                      )
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    contentapi = db.Column(db.String(100))
    info = db.Column(db.String(500))
    starttime = db.Column(db.Integer, nullable=False)
    endtime = db.Column(db.Integer, nullable=False)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    dates_id = db.Column(db.Integer, db.ForeignKey('dates.id'), nullable=False)
    classtypes_id = db.Column(db.Integer, db.ForeignKey('classtypes.id'))
    # __table_args__ = (db.UniqueConstraint('starttime', 'endtime', 'courses_id', 'dates_id),)
    # UniqueConstraint('starttime', 'endtime', 'courses_id', 'dates_id')


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
    # accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

'''
class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()
'''


# Lista med kurstillfallen som anvands i en kurs
def scheduleInCourse(course):
    templist = []
    tempvar = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.id == course).order_by(Dates.date).order_by(Classes.starttime).all()
    for item in tempvar:
        print "x"
        templist.append(item)
    return templist


# Lista med salar som anvands i en kurs
def roomsOnDate(date, course):
    templist = []
    tempvar = db.session.query(Rooms.name, Rooms.id).distinct().join(Rooms.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).filter(Courses.id == course).all()
    for item in tempvar:
        templist.append(item)
    return templist


# Lista med salar som anvands i en kurs
def defteachersondate(date, course):
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
    templist = db.session.query(Courses).order_by(Courses.code.desc()).all()
    # templist = db.session.query(Courses).order_by(Courses.code).all()
    return templist


def allcourses_one_year(yearvar):
    # templist = db.session.query(Courses).order_by(Courses.code.desc()).all()
    templist = db.session.query(Courses).filter(Courses.year == yearvar).order_by(Courses.code).all()
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
    # varz = float(varx[0][0]) / vary[0][0]
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
    # print testvar.password
    return testvar


def roomobjectfromid(roomid):
    testvar = db.session.query(Rooms).filter(Rooms.id == roomid).first()
    # print testvar.password
    return testvar


def courseobjectfromid(courseid):
    testvar = db.session.query(Courses).filter(Courses.id == courseid).first()
    # print testvar.password
    return testvar


def myobject():
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    # print testvar.password
    return db.session.query(Teachers).filter(Teachers.email == session['user']).first()


def myobjectfromid(teacherid):
    testvar = db.session.query(Teachers).filter(Teachers.id == teacherid).first()
    # print testvar.password
    return testvar


def mycoursesexaminerorresponsible():
    examiner = aliased(Teachers)
    responsible = aliased(Teachers)
    templist = db.session.query(Courses).join(examiner, Courses.examiner).join(responsible, Courses.responsible).filter(or_(examiner.email == session['user'], responsible.email == session['user'])).all()
    # templist = db.session.query(Courses).join(examiner, Courses.examiner).join(responsible, Courses.responsible).all()
    # print templist
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
    '''
    templist = db.session.query(Teachers.email).all()
    tempvar = "[{"
    id = 1
    for item in templist[:-1]:
        # print item
        tempvar = tempvar + " id: " + str(id) + ", text: '" + item[0] + "' }, {"
        id = id + 1
    tempvar = tempvar + " id: '" + str(id) + "', text: '" + templist[-1][0] + "' }]"
    # print tempvar
    # tempvar2 = "[{ id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }]"
    # print testvar.password
    return tempvar
    '''


def subjectslistjson():
    templist = db.session.query(Subjects.name).all()

    tempvar = "[{"
    id = 1
    for item in templist[:-1]:
        # print item
        tempvar = tempvar + " id: " + str(id) + ", text: '" + item[0] + "' }, {"
        id = id + 1
    tempvar = tempvar + " id: '" + str(id) + "', text: '" + templist[-1][0] + "' }]"

    # print tempvar
    # tempvar2 = "[{ id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }]"
    # print testvar.password
    return tempvar


def amiexaminer(code):
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    already = db.session.query(exists().where(and_(Courses.code == code, Courses.examiner == testvar))).scalar()
    return already


def amiresponsible(code):
    testvar = db.session.query(Teachers).filter(Teachers.email == session['user']).first()
    already = db.session.query(exists().where(and_(Courses.code == code, Courses.responsible == testvar))).scalar()
    return already


def amiteaching(code):
    testvar = db.session.query(Courses).join(Teachers.classes).join(Classes.courses).filter(and_(Teachers.email == session['user'], Courses.code == code)).first()
    # print testvar
    already = False
    if testvar:
        print testvar.code
        already = True
    return already


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


# CREATE TABLES
def createtables():
    db.create_all()
    db.session.commit()


# Import CSV-file and transform imported CSV to tables
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

    # for i in schedules_list:
    #    print i

    # Populate tables
    '''
    for i in courses_list:
        monthvar = i[0][5:7]
        if monthvar == "01" or "02" or "03" or "04" or "05" or "06":
            datevar = "01"
        else:
            datevar = "09"
        yearvar = i[3]
        codevar = i[0]
        courseobj = create_or_fetch_courseobj(coursevar, yearvar)
        term = what_term_is_this(datevar)
        db.session.commit()
        courseobj.name = i[1]
        courseobj.schedule_exists = True
        db.session.add(record)
        db.session.commit()
    '''

    for i in roomtypes_list:
        roomtype = i[0]
        cost = i[1]
        if len(roomtype) < 1:
            roomtype = None
        if len(cost) < 1:
            cost = None
        roomtypeobj = create_or_fetch_roomtypeobj(roomtype)
        if roomtypeobj:
            roomtypeobj.cost = cost
            db.session.commit()

    for i in subjects_list:
        name = i[0]
        if len(name) < 1:
            name = None
        create_or_fetch_subjectobj(name)

    for i in teachers_list:
        kthid = i[0]
        initials = i[1]
        email = i[2]
        firstname = i[3]
        akafirstname = i[3]
        lastname = i[4]
        akalastname = i[4]
        if len(kthid) < 1:
            kthid = None
        if len(initials) < 1:
            initials = None
        if len(email) < 1:
            email = None
        if len(firstname) < 1:
            firstname = None
        if len(lastname) < 1:
            lastname = None
        if len(akafirstname) < 1:
            akafirstname = None
        if len(akalastname) < 1:
            akalastname = None
        teacherobj = fetch_teacherobj(email)

        if teacherobj:
            teacherobj.kthid = kthid
            teacherobj.initials = initials
            if not teacherobj.firstname:
                teacherobj.firstname = firstname
            if not teacherobj.lastname:
                teacherobj.lastname = lastname
            teacherobj.akafirstname = akafirstname
            teacherobj.akalastname = akalastname
            db.session.commit()

    for i in rooms_list:
        name = i[0]
        seats = i[1]
        roomtype = i[2]
        if len(name) < 1:
            name = None
        if len(seats) < 1:
            seats = None
        if len(roomtype) < 1:
            roomtype = None
        roomobj = create_or_fetch_roomobj(name)
        roomtypeobj = create_or_fetch_roomtypeobj(roomtype)
        if roomobj and roomtypeobj:
            roomobj.seats = seats
            roomobj.roomtypes_id = roomtypeobj.id
            db.session.commit()

    for i in schedules_list:
        datevar = i[0]
        contentvar = i[3]
        codevar = i[5]
        yearvar = i[6]
        starttimevar = i[7]
        endtimevar = i[8]
        roomsstring = i[2]
        teachersstring = i[4]

        if len(datevar) < 1:
            datevar = None
        if len(contentvar) < 1:
            contentvar = None
        if len(codevar) < 1:
            codevar = None
        if len(yearvar) < 1:
            yearvar = None
        if len(starttimevar) < 1:
            starttimevar = None
        if len(endtimevar) < 1:
            endtimevar = None
        if len(roomsstring) < 1:
            roomsstring = None
        if len(teachersstring) < 1:
            teachersstring = None

        courseobj = fetch_courseobj(codevar, yearvar)
        dateobj = fetch_dateobj(datevar)

        if dateobj and courseobj:
            create_course_date_connection(courseobj, dateobj)

            classobj = fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)

            if classobj:
                create_room_class_connection(roomobj, classobj)
                classobj.content = contentvar
                classobj.courses_id = courseobj.id
                classobj.dates_id = dateobj.id
                db.session.commit()

                if not classobj.content:
                    classobj.content = contentvar

                teacherslist = teachersstring.split()
                for initials in teacherslist:
                    already = db.session.query(exists().where(Teachers.initials == initials)).scalar()

                    if already:
                        teacherobj = Teachers.query.filter_by(initials=initials).first()
                        create_teacher_class_connection(teacherobj, classobj)
                        create_teacher_date_connection(teacherobj, dateobj)

                roomslist = roomsstring.split()
                for name in roomslist:
                    roomobj = create_or_fetch_roomobj(name)
                    create_room_class_connection(roomobj, classobj)
                    create_room_date_connection(roomobj, dateobj)


# CLEAN THE CSV
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
            # print day_var
        else:
            day_var = "0" + list1[p][i][:1]
            # print day_var
        if list1[p][i][-3] == "/":
            # print "hej"
            month_var = list1[p][i][-2:]
            # print month_var
        else:
            month_var = "0" + list1[p][i][-1:]
            # print month_var

        # print list1[p][7]
        if list1[p][7]:
            year_var = list1[p][7]

        list1[p][i] = year_var + "-" + month_var + "-" + day_var
        year_var = "2016"

        # print list1[p][7]
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
            # print word
            alist = []
            alist = list1[p]
            alist[4] = word

            # print alist
            temp_list.extend(alist)
            # print "hej"

    # print temp_list
    return temp_list


# Separate teachers
def separate_rooms(list1):
    temp_list = []
    for p in range(0, len(list1)):
        words = list1[p][2].split()
        for word in words:
            # print word
            alist = []
            alist = list1[p]
            alist[2] = word

            # print alist
            temp_list.extend(alist)
            # print "hej"

    return temp_list


def open_password_protected_site(link):

    # Browser
    br = mechanize.Browser()

    # Enable cookie support for urllib2
    cookiejar = cookielib.LWPCookieJar()
    br.set_cookiejar(cookiejar)

    # Broser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # ??
    # br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )

    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    print "heh"
    # authenticate
    br.open(link)

    br.select_form(nr=0)
    # these two come from the code you posted
    # where you would normally put in your username and password
    br["username"] = 'ahell'
    br["password"] = '-Gre75kger-'
    res = br.submit()

    print "Success!\n"

    return br


def pass_courseyear_from_classdate(datevar):

    yearvar = int(datevar[:4])
    monthvar = datevar[5:7]

    if monthvar == "01":
        try:
            dayvar = str(datevar[-2:])
            if dayvar < 15:
                yearvar = yearvar - 1

        except Exception, e:
            varcode = "Day lower than 10"
            print varcode

    return yearvar


def what_term_is_this(startdatevar):
    monthvar = startdatevar[5:7]
    if monthvar == "01" or "02" or "03" or "04" or "05" or "06":
        term = 1
    else:
        term = 2

    return term


def create_or_fetch_roomtypeobj(roomtype):

    roomtypeobj = None

    try:
        roomtypeobj = db.session.query(Roomtypes).filter(Roomtypes.roomtype == roomtype).first()
    except Exception, e:
        varcode = "NO PREVIOUS ROOMTYPEOBJECT"
        print varcode

    if not roomtypeobj:
        print "CREATING ROOMTYPEOBJECT"
        tempdict = {}
        tempdict['roomtype'] = roomtype
        record = Roomtypes(**tempdict)
        roomtypeobj = record
        db.session.add(record)
        db.session.commit()

    else:
        print "ROOMTYPEOBJECT EXISTS"

    return roomtypeobj


def create_or_fetch_subjectobj(subject):

    subjectobj = None

    try:
        subjectobj = db.session.query(Subjects).filter(Subjects.name == subject).first()
    except Exception, e:
        varcode = "NO PREVIOUS SUBJECTOBJECT"
        print varcode

    if not subjectobj:
        print "CREATING SUBJECTOBJECT"
        tempdict = {}
        tempdict['name'] = subject
        record = Subjects(**tempdict)
        subjectobj = record
        db.session.add(record)
        db.session.commit()

    else:
        print "SUBJECTOBJECT EXISTS"

    return subjectobj


def create_or_fetch_teacherobj(email):

    teacherobj = None

    try:
        teacherobj = db.session.query(Teachers).filter(Teachers.email == email).first()
    except Exception, e:
        varcode = "NO PREVIOUS TEACHEROBJECT"
        print varcode

    if not teacherobj:
        print "CREATING TEACHEROBJECT"
        tempdict = {}
        tempdict['email'] = email
        record = Teachers(**tempdict)
        teacherobj = record
        db.session.add(record)
        db.session.commit()

    else:
        print "TEACHEROBJECT EXISTS"

    return teacherobj


def fetch_teacherobj(email):

    teacherobj = None

    try:
        teacherobj = db.session.query(Teachers).filter(Teachers.email == email).first()
    except Exception, e:
        varcode = "NO TEACHEROBJECT TO FETCH"
        print varcode

    return teacherobj


def create_or_fetch_courseobj(code, year):

    print code
    print year

    courseobj = None

    if code and year:
        try:
            courseobj = db.session.query(Courses).filter(and_(Courses.code == code, Courses.year == year)).first()
        except Exception, e:
            varcode = "NO PREVIOUS COURSEOBJECT"
            print varcode
            print courseobj

        if not courseobj:
            print "CREATING_COURSEOBJECT"
            print code
            print year
            print "ZZZ"
            # print db.session.query(Courses).filter(and_(Courses.code == code, Courses.year == year)).first()
            tempdict = {}
            tempdict['code'] = code
            tempdict['year'] = year

            print "QQQ"
            db.session.commit()
            templist = db.session.query(Courses).all()
            for item in templist:
                print item.year
            print "XXX"
            courseobj = Courses(**tempdict)

            # courseobj = record
            db.session.add(courseobj)
            print courseobj.code


            print "YYY"
            db.session.commit()

            print courseobj.code

        else:
            print "COURSEOBJECT EXISTS ALREADY"

    return courseobj


def fetch_courseobj(code, year):

    courseobj = None

    try:
        courseobj = db.session.query(Courses).filter(and_(Courses.code == code, Courses.year == year)).first()
    except Exception, e:
        varcode = "NO COURSEOBJECT TO FETCH"
        print varcode

    return courseobj


def create_or_fetch_dateobj(datevar):

    dateobj = None

    try:
        dateobj = db.session.query(Dates).filter(Dates.date == datevar).first()

    except Exception, e:
        varcode = "NO PREVIOUS DATEOBJECT"
        print varcode

    if not dateobj:
        print "CREATING DATEOBJECT"
        tempdict = {}
        tempdict['date'] = datevar
        record = Dates(**tempdict)
        dateobj = record
        db.session.add(record)
        db.session.commit()
    else:
        print "DATEOBJECT EXISTS"

    return dateobj


def fetch_dateobj(datevar):

    dateobj = None

    try:
        dateobj = db.session.query(Dates).filter(Dates.date == datevar).first()

    except Exception, e:
        varcode = "NO DATEOBJECT TO FETCH"
        print varcode

    return dateobj


def create_or_fetch_roomobj(roomvar):
    roomobj = None

    try:
        roomobj = db.session.query(Rooms).filter(Rooms.name == roomvar).first()
    except Exception, e:
        varcode = "NO PREVIOUS ROOMOBJECT"
        print varcode

    if not roomobj:
        print "CREATING ROOMOBJECT"
        tempdict = {}
        tempdict['name'] = roomvar
        record = Rooms(**tempdict)
        roomobj = record
        db.session.add(record)
        db.session.commit()
    else:
        print "ROOMOBJECT EXISTS"

    return roomobj


def create_room_date_connection(roomobj, dateobj):
    alreadydate = None

    if roomobj and dateobj:
        try:
            alreadydate = db.session.query(Dates).join(Dates.rooms).filter(and_(Dates.id == dateobj.id, Rooms.id == roomobj.id)).first()
        except Exception, e:
            varcode = "NO PREVIOUS ROOM-DATE"
            print varcode

        if not alreadydate:
            print "CREATING ROOM-DATE"
            dateobj.rooms.append(roomobj)
            db.session.commit()
        else:
            print "ROOM-DATE EXISTS"
    else:
        print "NO ROOMOBJ OR DATEOBJ"


def create_room_class_connection(roomobj, classobj):
    alreadydate = None
    if roomobj and classobj:
        try:
            alreadydate = db.session.query(Classes).join(Classes.rooms).filter(and_(Classes.id == classobj.id, Rooms.id == roomobj.id)).first()
        except Exception, e:
            varcode = "NO PREVIOUS ROOM-CLASS"
            print varcode

        if not alreadydate:
            print "CREATING ROOM-CLASS"
            classobj.rooms.append(roomobj)
            db.session.commit()
        else:
            print "ROOM-CLASS EXISTS"
    else:
        print "NO ROOMOBJ OR CLASSOBJ"


def create_teacher_class_connection(teacherobj, classobj):
    alreadydate = None

    if teacherobj and classobj:
        try:
            alreadydate = db.session.query(Classes).join(Classes.teachers).filter(and_(Classes.id == classobj.id, Teachers.id == teacherobj.id)).first()
        except Exception, e:
            varcode = "NO PREVIOUS TEACHER-CLASS"
            print varcode

        if not alreadydate:
            print "CREATING TEACHER-CLASS"
            classobj.teachers.append(teacherobj)
            db.session.commit()
        else:
            print "TEACHER-CLASS EXISTS"
    else:
        print "NO TEACHEROBJ OR CLASSOBJ"


def create_teacher_date_connection(teacherobj, dateobj):
    alreadydate = None

    if teacherobj and dateobj:
        try:
            alreadydate = db.session.query(Dates).join(Dates.teachers).filter(and_(Dates.id == dateobj.id, Teachers.id == teacherobj.id)).first()
        except Exception, e:
            varcode = "NO PREVIOUS TEACHER-DATE"
            print varcode

        if not alreadydate:
            print "CREATING TEACHER-DATE"
            dateobj.teachers.append(teacherobj)
            db.session.commit()
        else:
            print "TEACHER-DATE EXISTS"
    else:
        print "NO TEACHEROBJ OR DATEOBJ"


def create_course_date_connection(courseobj, dateobj):
    alreadycourse = None

    if courseobj and dateobj:
        try:
            alreadycourse = db.session.query(Dates).join(Dates.courses).filter(and_(Dates.id == dateobj.id, Courses.id == courseobj.id)).first()
        except Exception, e:
            varcode = "NO PREVIOUS COURSE-DATE"
            print varcode

        if not alreadycourse:
            print "CREATING COURSE-DATE"
            dateobj.courses.append(courseobj)
            db.session.commit()
        else:
            print "COURSE-DATE EXISTS"
    else:
        print "NO COURSOBJ OR DATEOBJ"


def create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj):

    classobj = None

    if starttimevar and endtimevar and courseobj and dateobj:
            classobj = db.session.query(Classes).join(Classes.courses).join(Classes.rooms).join(Classes.dates).filter(and_(Courses.id == courseobj.id, Dates.id == dateobj.id, Classes.starttime == starttimevar, Classes.endtime == endtimevar))
            alreadyclass = session.query(classobj.exists()).scalar()

            if alreadyclass:
                print "CLASSOBJECT EXISTS"
                print varcode
                classobj = classobj.first()

            else:
                varcode = "NO PREVIOUS CLASSOBJECT"
                print varcode

                print "CREATING CLASSOBJECT"
                tempdict = {}
                tempdict['starttime'] = starttimevar
                tempdict['endtime'] = endtimevar
                tempdict['courses_id'] = courseobj.id
                tempdict['dates_id'] = dateobj.id

                record = Classes(**tempdict)
                classobj = record
                db.session.add(record)
                db.session.commit()

    return classobj


def fetch_classobj(starttimevar, endtimevar, courseobj, dateobj):

    classobj = None

    try:
        classobj = db.session.query(Classes).join(Classes.courses).join(Classes.rooms).join(Classes.dates).filter(and_(Courses.id == courseobj.id, Dates.id == dateobj.id, Classes.starttime == starttimevar, Classes.endtime == endtimevar)).first()
    except Exception, e:
        varcode = "NO CLASSOBJECT TO FETCH"
        print varcode

    return classobj


def fetchinglistofslotspercourse(course, starttime, endtime):

    tempdict = {}
    templist = []
    tempdict['code'] = course
    tempdict['slots'] = templist

    try:
        j = urllib2.urlopen('http://www.kth.se/api/schema/v2/course/%s?startTime=%s&endTime=%s' % (course, starttime, endtime))

        j_obj = json.load(j)

        templist = j_obj['entries']

        tempdict['slots'] = templist

    except Exception, e:
        varcode = "no json for course"
        print varcode
        print course
        print starttime
        print endtime

    return tempdict


def parselistofslotspercourse(tempdict):
    code = tempdict['code']

    for item in tempdict['slots']:
        info = item['info']
        start = item['start']
        end = item['end']
        title = item['title']
        kind_name = item['type_name']
        kind = item['type']
        locations = item['locations']

        date = start[:10]
        starttime = start[11:13]
        endtime = end[11:13]
        kind_name = kind_name['sv']

        year = pass_courseyear_from_classdate(date)

        courseobj = fetch_courseobj(code, year)
        dateobj = create_or_fetch_dateobj(date)
        create_course_date_connection(courseobj, dateobj)

        for location in locations:
            roomvar = location['name']
            roomobj = create_or_fetch_roomobj(roomvar)
            create_room_date_connection(roomobj, dateobj)
            classobj = create_or_fetch_classobj(starttime, endtime, courseobj, dateobj)
            create_room_class_connection(roomobj, classobj)
            if classobj:
                classobj.contentapi = info
                print "INFO ADDED TO CLASS"
                db.session.commit()

    return "DONE"


# ADDING TEACHERS TO DB
def staffperdepartment(department):
    try:
        req = urllib2.urlopen('https://www.kth.se/directory/a/%s' % (department))

        xml = BeautifulSoup(req)

        templist = xml.find("table")
        templist = templist.find("tbody")
        templist = templist.findAll("tr")

        templist2 = []
        tempdict = {}

        for tr in templist:
            tdlist = tr.findAll("a")
            firstname = tdlist[2].text
            lastname = tdlist[1].text
            email = tdlist[3].text
            username = tdlist[1]['href'][27:]

            tempdict = {'firstname': firstname, 'lastname': lastname, 'email': email, 'username': username}
            templist2.append(tempdict)

        tempdict2 = {'department': department, 'teacher': templist2}

    except Exception, e:
        varcode = "no list of staff per department"
        print varcode
        print x
        print y

    return tempdict2


def teachersfromdepartment(templist):
    for items in templist:

        department = items['department']

        for item in items['teacher']:
            firstname = item['firstname']
            lastname = item['lastname']
            email = item['email']
            username = item['username']

            if email:
                teacherobj = create_or_fetch_teacherobj(email)

                teacherobj.firstname = firstname
                teacherobj.lastname = lastname
                teacherobj.email = email
                teacherobj.username = username
                teacherobj.department = department

                db.session.commit()

        print "DONE"


# ADDING COURSES TO DB
def courseinfoperyearandterm(x, y):

    templist = []
    tempdict2 = {}
    tempdict2['year'] = None
    tempdict2['round'] = None
    tempdict2['courseinfo'] = templist

    # try:
    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/courseRounds/%s:%s' % (x, y))

    xml = BeautifulSoup(req)

    items = xml.findAll("courseround")

    templist = []

    for item in items:

        coursecode = item['coursecode']
        if coursecode[:2] == "AI":
            startterm = item['startterm']
            roundid = item['roundid']

            period = None

            year = startterm[:4]

            term = startterm[-1:]

            tempdict = {'coursecode': coursecode, 'year': year, 'term': term, 'period': period, 'startterm': startterm, 'roundid': roundid}

            templist.append(tempdict)

    tempdict2 = {'year': x, 'round': y, 'courseinfo': templist}

    '''
    except Exception, e:
        varcode = "no list of courserounds"
        print varcode
        print x
        print y
    '''
    return tempdict2


def addcoursestotables_first(tempdict):

    for item in tempdict['courseinfo']:
        coursecode = item['coursecode']

        year = item['year']
        term = item['term']
        period = item['period']
        roundid = item['roundid']

        try:
            req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s/round/%s:%s/%s' % (coursecode, year, term, roundid))
            xml = BeautifulSoup(req)

            try:
                courseround = xml.find('courseround')

                endweek = courseround['endweek']
                item['endweek'] = endweek

                startweek = courseround['startweek']
                item['startweek'] = startweek

            except Exception, e:
                item['endweek'] = None
                item['startweek'] = None
                varcode = "no courseround"
                print varcode

            try:
                courseresponsible = xml.find('courseresponsible')

                emailcourseresponsible = courseresponsible['primaryemail']

                item['emailcourseresponsible'] = emailcourseresponsible

            except Exception, e:
                item['emailcourseresponsible'] = None
                varcode = "no courseresponsible"
                print varcode

            coursesfromdepartment2(item)

        except Exception, e:
            varcode = "NOT FINDING COURSE"
            print varcode
            print coursecode
            continue


def coursesfromdepartment2(item):

    code = item['coursecode']
    year = item['year']
    term = item['term']
    period = item['period']
    roundid = item['roundid']
    responsible = item['emailcourseresponsible']
    startweek = item['startweek']
    endweek = item['endweek']

    courseobj = create_or_fetch_courseobj(code, year)
    courseobj.term = term
    courseobj.period = period
    courseobj.roundid = roundid
    courseobj.startweek = startweek
    courseobj.endweek = endweek
    courseobj.responsible_id = Teachers.query.filter_by(email=responsible).first().id

    db.session.commit()


def fetchinglistofcodesfordepartmentcourses(department):

    tempdict = {}

    try:
        j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/%s.json' % (department))

        j_obj = json.load(j)

        templist = []

        for item in j_obj['courses']:
            templist.append(item['code'])

        tempdict = {'department': j_obj['department'], 'courses': templist}

    except Exception, e:
        varcode = "no list of codes for department courses"
        print varcode

    return tempdict


def jsonifycoursesfromdepartment(tempdict):

    templist2 = []
    tempdict2 = {}

    for item in tempdict['courses']:

        try:
            req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s' % (item))

            xml = BeautifulSoup(req)

            # varname = xml.title.string
            try:
                varcode = xml.course['code']
                # print varcode

            except Exception, e:
                varcode = None
                # print varcode

            try:
                varmail = xml.examiner['primaryemail']
                # print varmail

            except Exception, e:
                varmail = None
                # print varmail

            try:
                varname = xml.title.string
                # print varname.encode('utf-8')
                # print varname

            except Exception, e:
                varname = None
                # print varname

            tempdict2 = {'code': varcode, 'name': varname, 'examiner': varmail, 'department': tempdict['department']}

            templist2.append(tempdict2)

        except Exception, e:
            varcode = "no URL"
            print varcode + " " + item
            continue

    return templist2


def coursesfromdepartment3(templist):
    for items in templist:
        for item in items:
            name = item['name']
            code = item['code']
            examiner = item['examiner']
            department = item['department']

            teacherobj = create_or_fetch_teacherobj(examiner)

            try:
                latestcourse = db.session.query(Courses).filter(Courses.code == code).order_by(Courses.year.desc()).first()
                latestcourse.name = name
                latestcourse.examiner_id = Teachers.query.filter_by(email=examiner).first().id
                db.session.commit()

            except Exception, e:
                varcode = "COURSE NOT EXISTING"
                print varcode
                print code
                continue


# NOT READY
def jsonifylitteraturefromdepartment():

    templist = []
    item = "AI1128"
    # for item in tempdict['courses']:
    # varname = xml.title.string
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


# NOT READY
def calTest():
    req = urllib2.Request('https://www.kth.se/social/course/AI1146/calendar/ical/?lang=sv')
    response = urllib2.urlopen(req)
    data = response.read()
    for line in data.split('\n'):
        # print line
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


# NOT READY
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

        # templist3.append(jsonifylitteraturefromdepartment(tempdict))

        # tempdict3 = courseinfoperyearandround(2016, 1)

    # ADD ALL TEACHERS TO DB
    teachersfromdepartment(templist2)

    # ADD ALL COURSES TO DB
    coursesfromdepartment(templist)

    # FETCH ALL LITERATURE
    # jsonifylitteraturefromdepartment()

    # FETCH CALENDAR
    # calTest()

    # testv = jsonify(tempdict3)

app.jinja_env.globals.update(sumofonesteachingincourse=sumofonesteachingincourse, sumofroomtypesuseincourse=sumofroomtypesuseincourse, roomtypesuseincourse=roomtypesuseincourse, roomtypesincourse=roomtypesincourse, onesteachingincourse=onesteachingincourse, subjectslistjson=subjectslistjson, mycoursesresponsible=mycoursesresponsible, mycourseslist=mycourseslist)
app.jinja_env.globals.update(roomsslots=roomsslots, roomobjectfromid=roomobjectfromid, roomtypeobjectfromid=roomtypeobjectfromid, roomsperroomtype=roomsperroomtype, courseobjectfromid=courseobjectfromid, onesslots=onesslots, myobjectfromid=myobjectfromid, sumofonesteachingincourseperroomtypeperhour=sumofonesteachingincourseperroomtypeperhour, sumofonesteachingincourseperroomtype=sumofonesteachingincourseperroomtype)
app.jinja_env.globals.update(teachersonslot=teachersonslot, roomsonslot=roomsonslot, myslots=myslots, idtocode=idtocode, defteachersondate=defteachersondate, roomsOnDate=roomsOnDate, scheduleInCourse=scheduleInCourse, allcourses=allcourses, amiteaching=amiteaching, amiresponsible=amiresponsible, amiexaminer=amiexaminer, myobject=myobject, mycoursesexaminerorresponsible=mycoursesexaminerorresponsible)
app.jinja_env.globals.update(subjectsinslot=subjectsinslot, teachersincourse=teachersincourse, onescoursesteaching=onescoursesteaching, onescoursesresponsible=onescoursesresponsible, onescoursesexaminerorresponsible=onescoursesexaminerorresponsible, onescoursesexaminer=onescoursesexaminer, allteachers=allteachers, mycoursesteaching=mycoursesteaching, mycoursesexaminer=mycoursesexaminer)
app.jinja_env.globals.update(allcourses_one_year=allcourses_one_year)


@app.route('/')
def index():

    return redirect(url_for('login_page'))


@app.route('/login/', methods=["GET", "POST"])
def login_page():

    error = ''
    try:

        if request.method == "POST":

            attempted_email = request.form['email']
            attempted_password = request.form['password']

            xrubrik = db.session.query(Teachers).filter(Teachers.email == attempted_email).first()

            flash(xrubrik.email)
            # flash(attempted_password)

            if attempted_email == xrubrik.email and attempted_password == xrubrik.password:
                session['logged_in'] = True
                # session['username'] = request.form['initials']
                session['user'] = request.form['email']
                return redirect(url_for('login_page'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error)


@app.route('/register/', methods=["GET", "POST"])
def register_page():

    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
            initials = form.initials.data
            akafirstname = form.firstname.data
            akalastname = form.lastname.data
            email = form.email.data
            password = form.password.data
            already = db.session.query(exists().where(Teachers.email == email)).scalar()
            if not already:
                flash("Your email is not in the db")
                return render_template('register.html.j2', form=form)

            tempobj = db.session.query(Teachers).filter(Teachers.email == email).first()
            alreadyregistred = tempobj.password
            print alreadyregistred
            # alreadyregistred = db.session.query(exists().where(and_(Teachers.password is not None, Teachers.email == email))).scalar()

            if alreadyregistred:
                flash("Already registred!")
                return redirect(url_for('login_page'))

            existinginitials = db.session.query(exists().where(Teachers.initials == initials)).scalar()

            if existinginitials:
                tempobj = db.session.query(Teachers).filter(Teachers.email == email).first()
                if tempobj.initials != initials:
                    flash("Initials are already taken")
                    return render_template('register.html.j2', form=form)

            flash("Thanks for registering!")
            flash(email)
            tempobj = db.session.query(Teachers).filter(Teachers.email == email).first()
            tempobj.akafirstname = akafirstname
            tempobj.akalastname = akalastname
            tempobj.password = password
            tempobj.initials = initials
            db.session.commit()
            return redirect(url_for('login_page'))

    flash("Please register!")
    return render_template("register.html.j2", form=form)


@app.route('/logout/')
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

    result = {'id': id, 'text': request.form["value"]}

    return json.dumps(result)


@app.route('/user_edit_content/<int:page>', methods=['GET', 'POST'])
def user_edit_content(page):
    id = request.form["pk"]

    # varcode = id.split(',')[0]
    # varclassid = id.split(',')[1]
    # print varcode
    # print varclassid
    print id
    print "hej"

    # templist = []

    # templist = scheduleInCourse(varcode)
    # print templist

    # for item in templist:
    #   print item

    varteacher = db.session.query(Classes).get(id)
    print varteacher.content.encode('utf-8')
    # print varteacher.firstname.encode('utf-8')
    # print request.form["value"].encode('utf-8')
    varteacher.content = request.form["value"]
    print "Efter"
    print varteacher.content.encode('utf-8')
    # varteacher = Teachers.query.get(id)
    # print varteacher.firstname.encode('utf-8')
    result = {}
    db.session.commit()
    return json.dumps(result)


# Adding registred and expected students for all courses
@app.route('/fetchregistredandexpectedstudents')
def fetchregistredandexpectedstudents():

    br = open_password_protected_site("https://login.kth.se/login/")

    studentreg = 0

    for item in allcourses():

        termvar = "H"

        if item.term == 1:
            termvar = "V"

        yearvar = str(item.year)[-2:]

        url = br.open('https://www.kth.se/internt/minasidor/kurs/delt/?ccode=%s&term=%s%s' % (item.code, termvar, yearvar))

        try:

            xml = BeautifulSoup(url)

            xml = xml.find('table')

            xml = xml.find('caption').text

            if xml[-1:] == ":":
                studentreg = 0
            if xml[-2:-1] == ":":
                studentreg = 0
            if xml[-3:-2] == ":":
                studentreg = int(xml[-1:])
            if xml[-4:-3] == ":":
                studentreg = int(xml[-2:])
            if xml[-5:-4] == ":":
                studentreg = int(xml[-3:])

            if xml[22:23] == ",":
                studentexp = 0
            if xml[23:24] == ",":
                studentexp = int(xml[22:23])
            if xml[24:25] == ":":
                studentexp = int(xml[22:24])
            if xml[25:26] == ":":
                studentexp = int(xml[22:25])

            if item.studentsregistred:
                if item.studentsregistred < studentreg:
                    item.studentsregistred = studentreg
                    db.session.commit()
            else:
                item.studentsregistred = studentreg
                db.session.commit()

            if item.studentsexpected:
                if item.studentsexpected < studentexp:
                    item.studentsexpected = studentexp
                    db.session.commit()
            else:
                item.studentsexpected = studentexp
                db.session.commit()

        except Exception, e:
            varcode = "FAILED TO FETCH REGISTRED AND EXPECTED STUDENTS"
            print varcode
            print item.code
            continue

    return "DONE"


# Adding slots from schedule API for all courses
def slotsfromscheduleapi(coursecode):
        tempdict = fetchinglistofslotspercourse(coursecode, "2011-01-01", "2018-06-30")
        parselistofslotspercourse(tempdict)


# Adding slots from Social for all courses
@app.route('/slotsfromapiandsocial')
def slotsfromsocial():
    # print "YO"
    linklist = []

    br = open_password_protected_site("https://login.kth.se/login/")

    # testcourse = ["AI2808"]

    templist = allcourses()
    templist = templist[18:20]
    for idx, item in enumerate(templist):
        # for idx, item in enumerate(testcourse):
        coursecode = item.code
        # coursecode = "AI2808"
        # Fetching slots from schedule API
        ''''
        slotsfromscheduleapi(coursecode)
        '''
        try:
            url = br.open('https://www.kth.se/social/course/%s/subgroup/' % (coursecode))

            courselink = "/social/course/"
            courselink = courselink + coursecode
            courselink = courselink + "/subgroup/"

        except Exception, e:
            varcode = "no subgroup on social"
            print varcode
            print coursecode

            try:
                url = br.open('https://www.kth.se/social/course/%s/other_subgroups/' % (coursecode))

                courselink = "/social/course/"
                courselink = courselink + coursecode
                courselink = courselink + "/other_subgroups/"

            except Exception, e:
                varcode = "no other subgroups on social"
                print varcode
                print coursecode
                # session.rollback()
                # raise
                continue

        try:
            # url = br.open('https://www.kth.se/social/course/%s/other_subgroups/' % (coursecode))

            courselink = "/social/course/"
            courselink = courselink + coursecode
            courselink1 = courselink + "/other_subgroups/"
            courselink2 = courselink + "/subgroup/"

            xml = BeautifulSoup(url)
            xml1 = xml.find_all('a', href=lambda value: value and value.startswith(courselink1))
            xml2 = xml.find_all('a', href=lambda value: value and value.startswith(courselink2))
            xml = xml1 + xml2

            for idx, item in enumerate(xml):
                print "outer"
                print idx
                try:
                    fullcourselink = "https://www.kth.se"
                    fullcourselink = fullcourselink + item['href']
                    print idx
                    print fullcourselink
                    url = br.open(fullcourselink)

                    xml = BeautifulSoup(url)
                    xml = xml.find('a', text="Schema")

                    schedulelink = "https://www.kth.se"
                    schedulelink = schedulelink + xml['href']

                    url = br.open(schedulelink)

                    xml = BeautifulSoup(url)
                    xml1 = xml.find_all('a', href=lambda value: value and value.startswith(courselink1))
                    xml2 = xml.find_all('a', href=lambda value: value and value.startswith(courselink2))
                    xml = xml1 + xml2
                    print xml
                    for idx, item in enumerate(xml):
                        print "inner"
                        print idx
                        print item['href']
                        if "event" in item['href']:
                            # linklist.append(item['href'])
                            linkvar = item['href']
                            print "FETCHING SLOT"
                            print coursecode
                            testlink = "https://www.kth.se"
                            testlink = testlink + linkvar
                            print testlink
                            url = br.open(testlink)

                            # xml = BeautifulSoup(src)
                            xml = BeautifulSoup(url)
                            # testlist = xml.find_all('a', { "class" : "fancybox" })

                            startdate = xml.find('span', itemprop=lambda value: value and value.startswith("startDate"))
                            startdate = startdate.text
                            print startdate
                            enddate = xml.find('span', itemprop=lambda value: value and value.startswith("endDate"))
                            enddate = enddate.text
                            print enddate

                            datevar = startdate[:10]
                            print datevar

                            yearvar = pass_courseyear_from_classdate(datevar)
                            print yearvar
                            codevar = testlink[33:39]
                            print codevar
                            starttimevar = startdate[11:13]
                            print starttimevar
                            endtimevar = enddate[11:13]
                            print endtimevar

                            templist = db.session.query(Courses).all()
                            for item in templist:
                                print item.year

                            roomobj = None

                            courseobj = create_or_fetch_courseobj(codevar, yearvar)
                            # term = what_term_is_this(datevar)
                            # db.session.commit()
                            print courseobj.code

                            dateobj = create_or_fetch_dateobj(datevar)
                            create_course_date_connection(courseobj, dateobj)

                            locations = xml.find_all('a', href=lambda value: value and value.startswith("https://www.kth.se/places/room"))

                            for location in locations:
                                print "location"
                                try:
                                    print location
                                    location = location.text
                                    print "FETCHING ROOM"
                                    # print location
                                    print codevar
                                    print yearvar

                                    roomobj = create_or_fetch_roomobj(location)
                                    create_room_date_connection(roomobj, dateobj)

                                    # kolla vidare classobject - det ballar ur
                                    classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                                    print "xxx"
                                    print classobj.starttime
                                    create_room_class_connection(roomobj, classobj)

                                except Exception, e:
                                    varcode = "NO ROOM"
                                    print varcode
                                    classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                                    print "yyy"
                                    print classobj.starttime
                                    # create_room_class_connection(roomobj, classobj)
                                    continue
                except Exception, e:
                    varcode = "No schedule"
                    print varcode
                    print coursecode
                    # session.rollback()
                    # raise
                    continue

        except Exception, e:
            varcode = "No subgroup or other subgroups"
            print varcode
            print coursecode
            continue

    return "DONE"


@app.route('/csvimport')
def csvimport():
    csvimporter()
    # now = datetime.datetime.now()
    # thisyear = now.year
    # nextyear = str(1 + int(thisyear))
    # enddate = nextyear + "-12-31"
    # print enddate
    return "DONE"


@app.route('/restartall')
def restartall():

    createtables()

    # csvimporter()

    tempdict = {}
    templist = []

    departments = ["AIB", "AIC", "AID", "AIE"]

    # ADD_ALL_TEACHERS_TO_DB
    for item in departments:
        tempdict = staffperdepartment(item)
        templist.append(tempdict)
    teachersfromdepartment(templist)

    tempdict = {}
    templist = []

    # ADD_ALL_COURSES_TO_DB
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

    # ADD_ALL_COURSES_TO_DB
    for item in departments:
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        templist.append(jsonifycoursesfromdepartment(tempdict))
    coursesfromdepartment3(templist)

    return "restartall"


@app.errorhandler(404)
def page_not_found(e):

    return "fel"


# TO DO
def courseinfoperyearandround(x, y):
    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/courseRounds/%s:%s' % (x, y))

    xml = BeautifulSoup(req)

    templist = xml.findAll("courseround")

    templist2 = []

    for item in templist:
        # print "1"
        # print item['coursecode']
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

            tempdict = {'coursecode': coursecode, 'year': year, 'period': period, 'startterm': startterm, 'roundid': roundid}

            templist2.append(tempdict)

    tempdict2 = {'year': x, 'round': y, 'courseinfo': templist2}

    return tempdict2


# TO DO
def coursesfromdepartment(templist):
    for items in templist:

        for item in items:
            print item
            name = item['name']
            code = item['code']
            examiner = item['examiner']
            department = item['department']

            teacherobj = create_or_fetch_teacherobj(examiner)

            latestcourseobj = db.session.query(Courses).filter(Courses.code == code).order_by(Courses.year.desc()).first()

            latestcourseobj.name = name
            latestcourseobj.code = code
            latestcourseobj. examiner_id = Teachers.query.filter_by(email=examiner).first().id

            db.session.commit()

    print "DONE!"


'''
def fetchslotfromsociallink(linklist):

    createtables()

    br = open_password_protected_site("https://login.kth.se/login/")

    for linkvar in linklist:
        testlink = "https://www.kth.se"
        testlink = testlink + linkvar

        try:
            url = br.open(testlink)

            # xml = BeautifulSoup(src)
            xml = BeautifulSoup(url)
            # testlist = xml.find_all('a', { "class" : "fancybox" })

            startdate = xml.find('span', itemprop=lambda value: value and value.startswith("startDate"))
            startdate = startdate.text

            enddate = xml.find('span', itemprop=lambda value: value and value.startswith("endDate"))
            enddate = enddate.text

            datevar = startdate[:10]

            yearvar = pass_courseyear_from_classdate(datevar)

            codevar = testlink[33:39]
            starttimevar = startdate[11:13]
            endtimevar = enddate[11:13]

            roomobj = None

            courseobj = create_or_fetch_courseobj(codevar, yearvar)
            term = what_term_is_this(datevar)
            courseobj.term = term
            db.session.commit()

            dateobj = create_or_fetch_dateobj(datevar)
            create_course_date_connection(courseobj, dateobj)

            try:
                locations = xml.find_all('a', href=lambda value: value and value.startswith("https://www.kth.se/places/room"))

                for location in locations:
                    location = location.text
                    print "FETCHING!!!!"
                    print location
                    print codevar
                    print yearvar

                    roomobj = create_or_fetch_roomobj(location)
                    create_room_date_connection(roomobj, dateobj)
                    classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                    create_room_class_connection(roomobj, classobj)

            except Exception, e:
                varcode = "NO ROOM"
                print varcode
                classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                create_room_class_connection(roomobj, classobj)
                continue

        except Exception, e:
            varcode = "BROKEN"
            print varcode
            continue

    return "DONE"


# Adding slots from Social for all courses
@app.route('/Xslotsfromsocial')
def Xslotsfromsocial():

    linklist = []

    br = open_password_protected_site("https://login.kth.se/login/")

    for item in allcourses():
        # print item.code
        coursecode = item.code
        # url = br.open('https://www.kth.se/social/course/AI1146/subgroup/')

        try:
            url = br.open('https://www.kth.se/social/course/%s/subgroup/' % (item.code))

            courselink = "/social/course/"
            courselink = courselink + item.code
            courselink = courselink + "/subgroup/"

        except Exception, e:
            varcode = "no subgroup on social"
            print varcode
            print coursecode

            try:
                url = br.open('https://www.kth.se/social/course/%s/other_subgroups/' % (item.code))

                courselink = "/social/course/"
                courselink = courselink + item.code
                courselink = courselink + "/other_subgroups/"

            except Exception, e:
                varcode = "no other subgroups on social"
                print varcode
                print item.code

        try:
            xml = BeautifulSoup(url)
            xml = xml.find_all('a', href=lambda value: value and value.startswith(courselink))

            for item in xml:

                fullcourselink = "https://www.kth.se"
                fullcourselink = fullcourselink + item['href']

                try:
                    url = br.open(fullcourselink)

                    xml = BeautifulSoup(url)
                    xml = xml.find('a', text="Schema")

                    schedulelink = "https://www.kth.se"
                    schedulelink = schedulelink + xml['href']

                    try:
                        url = br.open(schedulelink)

                        xml = BeautifulSoup(url)
                        xml = xml.find_all('a', href=lambda value: value and value.startswith(courselink))

                        for item in xml:
                            if "event" in item['href']:
                                # linklist.append(item['href'])
                                linkvar = item['href']
                                print "FETCHING"
                                print coursecode
                                testlink = "https://www.kth.se"
                                testlink = testlink + linkvar

                                try:
                                    url = br.open(testlink)

                                    # xml = BeautifulSoup(src)
                                    xml = BeautifulSoup(url)
                                    # testlist = xml.find_all('a', { "class" : "fancybox" })

                                    startdate = xml.find('span', itemprop=lambda value: value and value.startswith("startDate"))
                                    startdate = startdate.text

                                    enddate = xml.find('span', itemprop=lambda value: value and value.startswith("endDate"))
                                    enddate = enddate.text

                                    datevar = startdate[:10]

                                    yearvar = pass_courseyear_from_classdate(datevar)

                                    codevar = testlink[33:39]
                                    starttimevar = startdate[11:13]
                                    endtimevar = enddate[11:13]

                                    roomobj = None

                                    courseobj = create_or_fetch_courseobj(codevar, yearvar)
                                    term = what_term_is_this(datevar)
                                    db.session.commit()

                                    dateobj = create_or_fetch_dateobj(datevar)
                                    create_course_date_connection(courseobj, dateobj)

                                    try:
                                        locations = xml.find_all('a', href=lambda value: value and value.startswith("https://www.kth.se/places/room"))

                                        for location in locations:
                                            location = location.text
                                            print "FETCHING!!!!"
                                            print location
                                            print codevar
                                            print yearvar

                                            roomobj = create_or_fetch_roomobj(location)
                                            create_room_date_connection(roomobj, dateobj)
                                            classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                                            create_room_class_connection(roomobj, classobj)

                                    except Exception, e:
                                        varcode = "NO ROOM"
                                        print varcode
                                        classobj = create_or_fetch_classobj(starttimevar, endtimevar, courseobj, dateobj)
                                        create_room_class_connection(roomobj, classobj)

                                except Exception, e:
                                    varcode = "BROKEN"
                                    print varcode

                    except Exception, e:
                        varcode = "no slot on social"
                        print varcode
                        print coursecode

                except Exception, e:
                    varcode = "no schedule on social"
                    print varcode
                    print coursecode

        except Exception, e:
            varcode = "no course on social"
            print varcode
            print coursecode

    fetchslotfromsociallink(linklist)

    return "DONE"
'''


if __name__ == "__main__":
    app.secret_key = 'asdasdasdasdasd'
    app.run(debug=True, host='0.0.0.0', port=1080)
    # app.run(host='0.0.0.0', port=1080)
