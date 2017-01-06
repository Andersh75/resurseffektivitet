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



app = Flask(__name__)

@app.route('/')
def hello_world():

    req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/AI1147')

    xml = BeautifulSoup(req)

    #print xml.examiner.attrs


    #print xml.examiner['primaryemail']

    #print varmail

    #print (xml.title.string).encode('utf-8')

    #print xml.course['code']

    varcode = xml.course['code']
    varmail = xml.examiner['primaryemail']


    #print varcode

    #tempdict = {'code':xml.course['code'], 'examiner':xml.examiner['primaryemail']}

    #print tempdict


    return jsonify(code=varcode, examiner=varmail, title=(xml.title.string).encode('utf-8'))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
