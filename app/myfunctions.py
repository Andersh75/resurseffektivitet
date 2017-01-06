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

        tempdict = {'firstname':firstname, 'lastname':lastname, 'mail':mail, 'department':department}
        templist2.append(tempdict)


    return tempdict
