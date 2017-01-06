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





tempdict = {}

req = urllib2.urlopen('http://www.kth.se/api/kopps/v1/course/HS1735')

xml = BeautifulSoup(req)

print xml.examiner.attrs

print xml.examiner['primaryemail']


print xml.course.attrs

print xml.course['code']


tempdict['code'] = xml.course['code']
tempdict['examiner'] = xml.examiner['primaryemail']

print tempdict
