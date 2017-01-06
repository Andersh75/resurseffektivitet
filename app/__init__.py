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
from myfunctions import jsonifycoursesfromdepartment, fetchinglistofcodesfordepartmentcourses

app = Flask(__name__)






@app.route('/')
def hello_world():

    #EXAMPLE OF XML TO JSON
    '''
    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/AI1147')

    xml = BeautifulSoup(req)

    varcode = xml.course['code']
    vartitle = xml.title.string
    varmail = xml.examiner['primaryemail']

    tempdict = {'code':varcode, 'title':vartitle, 'examiner':varmail}

    return json.dumps(tempdict)

    return jsonify(code=varcode, title=vartitle, examiner=varmail)
    '''


    #FETCHING LIST OF CODES FOR AIB COURSES
    '''
    j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/AIB.json')

    j_obj = json.load(j)

    templist =[]

    for item in j_obj['courses']:
        #print item['code']
        templist.append(item['code'])

    print templist

    return json.dumps(j_obj)
    '''



    #JSONIFY COURSES FROM DEPARTMENT
    '''
    j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/AIB.json')

    j_obj = json.load(j)

    templist = []

    for item in j_obj['courses']:
        #print item['code']
        templist.append(item['code'])

    templist2 = []
    tempdict = {}

    for item in templist:
        req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/%s' % (item))

        xml = BeautifulSoup(req)


        #vartitle = xml.title.string
        try:
            varcode = xml.course['code']
            print varcode

        except Exception, e:
            varcode = "no title"
            print varcode


        try:
            varmail = xml.examiner['primaryemail']
            print varmail

        except Exception, e:
            varmail = "no mail"
            print varmail


        try:
            vartitle = xml.title.string
            #print vartitle.encode('utf-8')
            print vartitle

        except Exception, e:
            vartitle = "no title"
            print vartitle

        tempdict = {'code':varcode, 'title':vartitle, 'examiner':varmail}

        templist2.append(tempdict)

    return jsonify(courses=templist2)

    '''

    templist = fetchinglistofcodesfordepartmentcourses(AIB)

    templist2 = jsonifycoursesfromdepartment(templist)

    return jsonify(courses=templist2)





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
