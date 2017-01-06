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
from myfunctions import jsonifycoursesfromdepartment, fetchinglistofcodesfordepartmentcourses, staffperdepartment, courseinfoperyearandround, new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/f1'
db = SQLAlchemy(app)





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

    print templist[0][0]['title']


    for item in templist[0]:
        print item['title']



    testv = jsonify(tempdict3)

    return "testv"


@app.route('/2')
def hello_world():

    j = urllib2.urlopen('http://www.kth.se/api/kopps/v2/courses/%s.json' % ("aib"))

    j_obj = json.load(j)

    print j_obj

    return "HEJ"







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
