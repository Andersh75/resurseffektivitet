
#from __init__ import db


from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
import urllib2
import xmltodict
from xml.etree import ElementTree as ET
from decimal import Decimal
import json
from flask import jsonify
from socket import *



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/e59'
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



class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

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
    #schedules = db.relationship('Schedules', secondary=rooms_schedules, backref=db.backref('rooms', lazy='dynamic'))
    classes = db.relationship('Classes', secondary=rooms_classes, backref=db.backref('rooms', lazy='dynamic'))

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    initials = db.Column(db.String(30))
    email = db.Column(db.String(30))
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    password = db.Column(db.String(30))
    #schedules = db.relationship('Schedules', secondary=teachers_schedules, backref=db.backref('teachers', lazy='dynamic'))
    classes = db.relationship('Classes', secondary=teachers_classes, backref=db.backref('teachers', lazy='dynamic'))
    examiners = db.relationship('Examiners', backref='teachers', lazy='dynamic')


class Examiners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teachers_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    courses = db.relationship('Courses', backref='examiners', lazy='dynamic')

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30))
    name = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    #schedules = db.relationship('Schedules', backref='courses', lazy='dynamic')
    classes = db.relationship('Classes', backref='courses', lazy='dynamic')
    exminers_id = db.Column(db.Integer, db.ForeignKey('examiners.id'))

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    #roomtypes_id = db.Column(db.Integer, db.ForeignKey('roomtypes.id'))


class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    #roomtypes_id = db.Column(db.Integer, db.ForeignKey('roomtypes.id'))
    #classes = db.relationship('Classes', secondary=dates_classes, backref=db.backref('dates', lazy='dynamic'))
    courses = db.relationship('Courses', secondary=dates_courses, backref=db.backref('dates', lazy='dynamic'))
    rooms = db.relationship('Rooms', secondary=dates_rooms, backref=db.backref('dates', lazy='dynamic'))
    teachers = db.relationship('Teachers', secondary=dates_teachers, backref=db.backref('dates', lazy='dynamic'))
    classes = db.relationship('Classes', backref='dates', lazy='dynamic')

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.String(30))
    content = db.Column(db.String(100))
    starttime = db.Column(db.Integer)
    endtime = db.Column(db.Integer)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    dates_id = db.Column(db.Integer, db.ForeignKey('dates.id'))



db.create_all()
db.session.commit()
