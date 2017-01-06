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
from myfunctions import jsonifycoursesfromdepartment, fetchinglistofcodesfordepartmentcourses, staffperdepartment

app = Flask(__name__)





@app.route('/2')
def hello_world2():

    tempdict = {}
    templist = []
    departments = ["AIB", "AIC", "AID", "AIE"]

    for item in departments:
        tempdict = fetchinglistofcodesfordepartmentcourses(item)
        templist.append(jsonifycoursesfromdepartment(tempdict))

    return jsonify(courses=templist)


@app.route('/')
def hello_world():


    department = "AIB"
    templist2 = staffperdepartment(department)
    return jsonify(staff=templist2)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
