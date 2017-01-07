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
#from myfunctions import jsonifycoursesfromdepartment, fetchinglistofcodesfordepartmentcourses, staffperdepartment, courseinfoperyearandround, coursesfromdepartment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f5'
db = SQLAlchemy(app)



class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    code = db.Column(db.String(30), unique=True)
    examiner = db.Column(db.String(50))
    department = db.Column(db.String(100))
    year = db.Column(db.Integer)
    period = db.Column(db.Integer)
    startterm = db.Column(db.Integer)
    roundid = db.Column(db.Integer)


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(30), unique=True)
    mail = db.Column(db.String(50))
    department = db.Column(db.String(100))



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


        #vartitle = xml.title.string
        try:
            varcode = xml.course['code']
            #print varcode

        except Exception, e:
            varcode = "no title"
            #print varcode


        try:
            varmail = xml.examiner['primaryemail']
            #print varmail

        except Exception, e:
            varmail = "no mail"
            #print varmail


        try:
            vartitle = xml.title.string
            #print vartitle.encode('utf-8')
            #print vartitle

        except Exception, e:
            vartitle = "no title"
            #print vartitle

        tempdict2 = {'code':varcode, 'title':vartitle, 'examiner':varmail, 'department':tempdict['department']}

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
        #print tdlist
        firstname = tdlist[2].text
        lastname = tdlist[1].text
        mail = tdlist[3].text

        tempdict = {'firstname':firstname, 'lastname':lastname, 'mail':mail}
        templist2.append(tempdict)


    tempdict2 = {'department':department, 'person':templist2}

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
                period = int(roundid)
            else:
                period = int(roundid) + 2

            year = startterm[:4]

            print coursecode, roundid, startterm, period, year

            tempdict = {'coursecode':coursecode, 'year':year, 'period':period, 'startterm':startterm, 'roundid':roundid}

            templist2.append(tempdict)

    tempdict2 = {'year':x, 'round':y, 'courseinfo':templist2}

    return tempdict2



def coursesfromdepartment(templist):
    for itemlist in templist:
        for item in itemlist:
            title = item['title']
            code = item['code']
            examiner = item['examiner']
            department = item['department']

            tempdict = {}
            exists = db.session.query(Courses).filter(code == code).count()
            print exists
            if title and code and (examiner != "no mail") and department and exists:
                tempdict['title'] = title
                tempdict['code'] = code
                tempdict['examiner'] = examiner
                tempdict['department'] = department
                record = Courses(**tempdict)
                db.session.add(record)
                db.session.commit()
                print tempdict


@app.route('/')
def hello_world2():

    tempdict = {}
    tempdict2 = {}
    tempdict3 = {}

    templist = []
    templist2 = []

    departments = ["AIB", "AIC", "AID", "AIE"]

    for item in departments:
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        templist.append(jsonifycoursesfromdepartment(tempdict))

        tempdict2 = staffperdepartment(item)
        templist2.append(tempdict2)

    tempdict3 = courseinfoperyearandround(2016, 1)

    coursesfromdepartment(templist)


    testv = jsonify(tempdict3)

    return "testv"









if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
