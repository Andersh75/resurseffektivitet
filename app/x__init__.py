from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import urllib
import urllib2
import xmltodict
from xml.etree import ElementTree as ET
from decimal import Decimal
import json
from flask import jsonify
from socket import *
from functools import wraps

#sock=socket()
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# then bind

def grabcoursepm(code):
    requestURL = 'http://www.kth.se/api/kopps/v1/course/' + code

    file = urllib2.urlopen(requestURL)
    data = file.read()
    file.close

    data = xmltodict.parse(data)



    title = data['course']['title'][0]['#text']
    credits = data['course']['credits'][0]['#text']
    gradeScaleCode = data['course']['gradeScaleCode']['#text']
    educationalLevel = data['course']['educationalLevel'][0]['#text']
    #department = data['course']['department'][0]['#text'].encode('utf-8')
    department = data['course']['department'][0]['#text']
    #contactName = data['course']['contactName']['#text'].split(',')[0]
    #contactName = contactName.split(';')[0]
    courseresp = data['course']['contactName']['#text'].split(',')[0]

    examiner = data['course']['examiners']['examiner']['#text']
    examinerMail = data['course']['examiners']['examiner']['@primaryEmail']
    #print title
    #print examiner

    #contactName = contactName.encode('utf-8')

    #print contactName
    if isinstance(courseresp, unicode):
        #contactName = unicode(contactName, "utf8")
        print "Unicode Hej  as"
        #contactName="Unicode"
        #print contactName
    else:
        print "ASCII He"
        #print contactName
        #contactName="ASCII"
        #contactName = unicode(contactName, "utf8")
        #print contactName

    #contactName = "Heej"
    #contactName="Hej"
    #print contactName.encode('utf-8')

    return title, credits, educationalLevel, department, courseresp, examiner

#grabcoursepm("AI1147")







app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/e61'
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



'''
rooms_schedules = db.Table('rooms_schedules',
    db.Column('rooms_id', db.Integer, db.ForeignKey('rooms.id')),
    db.Column('schedules_id', db.Integer, db.ForeignKey('schedules.id'))
)

teachers_schedules = db.Table('teachers_schedules',
    db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('schedules_id', db.Integer, db.ForeignKey('schedules.id'))
)










dates_classes = db.Table('dates_classes',
    db.Column('dates_id', db.Integer, db.ForeignKey('dates.id')),
    db.Column('classes_id', db.Integer, db.ForeignKey('classes.id'))
)
'''

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
    examiner = db.relationship('Courses', backref='examiner', lazy='dynamic')



class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30))
    name = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    #schedules = db.relationship('Schedules', backref='courses', lazy='dynamic')
    classes = db.relationship('Classes', backref='courses', lazy='dynamic')
    examiners_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))



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

'''
class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    content = db.Column(db.String(100))
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

'''


class RegistrationForm(Form):
    initials = TextField('Initials', [validators.Length(min=2, max=20)])
    firstname = TextField('First name', [validators.Length(min=2, max=20)])
    lastname = TextField('Last name', [validators.Length(min=2, max=20)])
    email = TextField('Email Address', [validators.Length(min=9, max=17)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])






def allcourses():
    templist = []
    tempvar = db.session.query(Courses).order_by(Courses.code).all()
    for item in tempvar:
        templist.append(item)
    return templist

def allteachers():
    templist = []
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname, Teachers.initials).distinct().order_by(Teachers.initials).all()
    for item in tempvar:
        templist.append(item)
    return templist



# Lista med larare som anvands i en kurs
def teachersInCourse(course):
    templist = []
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname, Teachers.initials).distinct().join(Teachers.classes).join(Classes.courses).filter(Courses.code == course).order_by(Teachers.lastname).all()
    for item in tempvar:
        templist.append(item)
    return templist



def scheduleInCourse(course):
# Lista med kurstillfallen som anvands i en kurs
    templist = []
    tempvar = db.session.query(Dates.date, func.year(Dates.date), func.month(Dates.date), func.day(Dates.date), Classes.starttime, Classes.endtime, Classes.content, Classes.id).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.code == course).order_by(Dates.date).order_by(Classes.starttime).all()
    for item in tempvar:
        templist.append(item)
    return templist

def roomsInCourse(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name).distinct().join(Rooms.classes).join(Classes.courses).filter(Courses.code == course).order_by(Rooms.name).all()
    for item in tempvar:
        templist.append(item)
    return templist

def roomsOnDate(date, course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name).distinct().join(Rooms.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).filter(Courses.code == course).all()
    for item in tempvar:
        templist.append(item)
    return templist

def roomsPerDate(date):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Classes.starttime, Classes.endtime, Courses.code, Roomtypes.id).join(Rooms.classes).join(Rooms.roomtypes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).order_by(Classes.starttime).all()
    for item in tempvar:
        templist.append(item)
    return templist

def coursesPerDate(date):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Teachers.initials, Classes.starttime, Classes.endtime, Courses.code).distinct().join(Teachers.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).order_by(Classes.starttime).all()
    for item in tempvar:
        templist.append(item)
    return templist

def AllDates(page):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Dates).order_by(Dates.date).slice(page, page+1).all()
    for item in tempvar:
        templist.append(item)
    return templist





def defteachersondate(date, course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname, Teachers.initials).distinct().join(Teachers.classes).join(Classes.dates).join(Classes.courses).filter(Dates.date == date).filter(Courses.code == course).all()
    for item in tempvar:
        templist.append(item)
    return templist

# Lista med antal salstimmar per rum i sjunkande ordning
def topRoomsInCourse(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Roomtypes.roomtype, func.sum(Classes.endtime - Classes.starttime), Roomtypes.cost).join(Rooms.classes).join(Rooms.roomtypes).join(Classes.courses).filter(Courses.code == course).group_by(Roomtypes.roomtype).order_by(Roomtypes.roomtype).all()
    for item in tempvar:
        templist.append(item)
    return templist


# Lista med antal salstimmar per rum i sjunkande ordning
def topRoomsInCourseSum(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Roomtypes.roomtype, func.sum(Classes.endtime - Classes.starttime), func.sum((Classes.endtime - Classes.starttime) * Roomtypes.cost)).join(Rooms.classes).join(Rooms.roomtypes).join(Classes.courses).filter(Courses.code == course).group_by(Roomtypes.roomtype).order_by(Roomtypes.roomtype).all()
    for item in tempvar:
        templist.append(item)
    return templist

# Lista med antal salstimmar per rum i sjunkande ordning
def topRoomsInCourseTotal(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Roomtypes.roomtype, func.sum(Classes.endtime - Classes.starttime), func.sum((Classes.endtime - Classes.starttime) * Roomtypes.cost)).join(Rooms.classes).join(Rooms.roomtypes).join(Classes.courses).filter(Courses.code == course).group_by(Courses.code).order_by(Roomtypes.roomtype).first()

    if tempvar is not None:
        for item in tempvar:
            templist.append(item)
        return templist[3]
    return 0



def topRoomsInCourseNumbers(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Rooms.name, Roomtypes.roomtype, func.sum(Classes.endtime - Classes.starttime), Roomtypes.cost).join(Rooms.classes).join(Rooms.roomtypes).join(Classes.courses).filter(Courses.code == course).group_by(Roomtypes.roomtype).order_by(Roomtypes.roomtype).all()
    for item in tempvar:
        templist.append(item[2])
    return templist




def TeachersInCourseNumbers(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname, func.sum(Classes.endtime - Classes.starttime)).join(Teachers.classes).join(Classes.courses).filter(Courses.code == course).group_by(Teachers.initials).order_by(Teachers.initials).all()
    for item in tempvar:
        templist.append(item)
    return templist

def TeachersInCourseNumbersSum(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Teachers.classes).join(Classes.courses).filter(Courses.code == course).group_by(Courses.code).first()
    templist = tempvar

    if templist is not None:
        return templist[0]
    return 0


def RoomsInCourseNumbersSum(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(func.sum(Classes.endtime - Classes.starttime)).join(Rooms.classes).join(Classes.courses).filter(Courses.code == course).group_by(Courses.code).first()
    templist = tempvar

    if templist is not None:
        return templist[0]
    return 0

def TeachersInCourseNumbersTest(course):
# Lista med salar som anvands i en kurs
    templist = []
    tempvar = db.session.query(Teachers.initials, func.sum(Classes.endtime - Classes.starttime)).join(Teachers.classes).join(Classes.courses).filter(Courses.code == course).group_by(Teachers.initials).order_by(Teachers.initials).all()
    for item in tempvar:
        templist.append(float(item[1]))
    return templist
    print templist

testarlista = topRoomsInCourseNumbers("AI1147")

def testar(tesvar):
    return db.session.query(Dates.date, Classes.content).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.code == tesvar).order_by(Dates.date).all()



def teachernamefromid(teacherid):
    tempvar = db.session.query(Teachers.firstname, Teachers.lastname).filter(Teachers.id == teacherid[0]).first()
    templist = []
    #print teacherid[0]
    #print tempvar
    for item in tempvar:
        templist.append(item)
    return templist
    #print templist
    return templist





def defcoursesforteacherid(teacherid):
    templist = []
    tempvar = db.session.query(Courses.code, Courses.name, func.sum(Classes.endtime - Classes.starttime)).join(Courses.classes).join(Classes.teachers).filter(Teachers.id == teacherid[0]).group_by(Courses.code).order_by(Courses.code).all()
    #print teacherid[0]
    #print tempvar
    for item in tempvar:
        templist.append(item)
    return templist
    #print templist
    return templist

def defcoursestotalhoursforteacherid(teacherid):
    templist = []
    tempvar = db.session.query(Courses.code, Courses.name, func.sum(Classes.endtime - Classes.starttime)).join(Courses.classes).join(Classes.teachers).filter(Teachers.id == teacherid[0]).group_by(Teachers.id).all()
    #print teacherid[0]
    #print tempvar
    for item in tempvar:
        templist.append(item)
    return templist
    #print templist
    return templist



def defexaminerforteacherid(teacherid):
    templist = []
    tempvar = db.session.query(Courses.code, Courses.name).join(Courses.classes).join(Classes.teachers).filter(Teachers.id == teacherid[0]).group_by(Courses.code).order_by(Courses.code).all()
    #print teacherid[0]
    #print tempvar
    for item in tempvar:
        templist.append(item)
    return templist
    #print templist
    return templist

yeartest = "2013"






def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap




app.jinja_env.globals.update(testar=testar)
app.jinja_env.globals.update(coursesPerDate=coursesPerDate, allcourses=allcourses, AllDates=AllDates, roomsPerDate=roomsPerDate, allteachers=allteachers, defteachersondate=defteachersondate, defexaminerforteacherid=defexaminerforteacherid, defcoursestotalhoursforteacherid=defcoursestotalhoursforteacherid, defcoursesforteacherid=defcoursesforteacherid, teachernamefromid=teachernamefromid, roomsOnDate=roomsOnDate, topRoomsInCourseTotal=topRoomsInCourseTotal, yeartest=yeartest, TeachersInCourseNumbersSum=TeachersInCourseNumbersSum, RoomsInCourseNumbersSum=RoomsInCourseNumbersSum, topRoomsInCourseSum=topRoomsInCourseSum)
app.jinja_env.globals.update(TeachersInCourseNumbersTest=TeachersInCourseNumbersTest, TeachersInCourseNumbers=TeachersInCourseNumbers, grabcoursepm=grabcoursepm)
app.jinja_env.globals.update(teachersInCourse=teachersInCourse, scheduleInCourse=scheduleInCourse, roomsInCourse=roomsInCourse, topRoomsInCourse=topRoomsInCourse, topRoomsInCourseNumbers=topRoomsInCourseNumbers, testarlista=testarlista)




@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login_page'))



@app.route('/<int:page>')
def index(page):

    if page < 29 and page > 6:
        xrubrik = db.session.query(Courses.code).filter(Courses.id == page).first()
        xkurskod = db.session.query(Courses.name).filter(Courses.id == page).first()
        #return "hej"
        #return render_template('new.html', kurskod="AI1146", xvar = xvar, Roomtypes = Roomtypes(), Rooms = Rooms(), Teachers = Teachers(), Courses = Courses(), Roles = Roles(), Dates = Dates(), Classes = Classes())
        #return render_template('base.html')
        #return render_template('test.xml'), mimetype='application/xml'
        #print json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
        #print json.dumps([{'text': 'first', 'value': 1}, {'text': 'second', 'value': 2}], separators=(',', ':'))
        return render_template('blocks.html.j2', varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=page)
    xrubrik = db.session.query(Courses.code).filter(Courses.id == 17).first()
    xkurskod = db.session.query(Courses.name).filter(Courses.id == 17).first()
    return render_template('blocks.html.j2', varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=17)





@app.route('/people/<int:page>')
def peopleindex(page):

        if page < 29 and page > 6:
            xrubrik = db.session.query(Courses.code).filter(Courses.id == page).first()
            xkurskod = db.session.query(Courses.name).filter(Courses.id == page).first()
            xteacher = db.session.query(Teachers.id).filter(Teachers.id == page).first()
            #return "hej"
            #return render_template('new.html', kurskod="AI1146", xvar = xvar, Roomtypes = Roomtypes(), Rooms = Rooms(), Teachers = Teachers(), Courses = Courses(), Roles = Roles(), Dates = Dates(), Classes = Classes())
            #return render_template('base.html')
            #return render_template('test.xml'), mimetype='application/xml'

            return render_template('peopleblocks.html.j2', xteacher=xteacher, varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=page)
        xrubrik = db.session.query(Courses.code).filter(Courses.id == 17).first()
        xkurskod = db.session.query(Courses.name).filter(Courses.id == 17).first()
        xteacher = db.session.query(Teachers.id).filter(Teachers.id == 27).first()
        return render_template('peopleblocks.html.j2', xteacher=xteacher, varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=17)


@app.route('/')
def index3():
    return redirect(url_for('login_page'))

@app.route('/headerlink1')
def headerlink1():
    return render_template('headerlink1head.html.j2')


@app.route('/headertoincludeincluder')
def headertoincludeincluder():
    return render_template('headertoincludeincluder.html.j2')


@app.route('/headertoincludeextender')
def headertoincludeextender():
    return render_template('headertoincludeextender.html.j2')

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



@app.route('/s')
@login_required
def index2():
    xrubrik = db.session.query(Courses.code).filter(Courses.id == 17).first()
    xkurskod = db.session.query(Courses.name).filter(Courses.id == 17).first()
    return render_template('blocks.html.j2', varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=17)




@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:

        if request.method == "POST":

            attempted_initials = request.form['initials']
            attempted_password = request.form['password']

            xrubrik = db.session.query(Teachers).filter(Teachers.initials == attempted_initials).first()

            flash(xrubrik.initials)
            #flash(attempted_password)

            if attempted_initials == xrubrik.initials and attempted_password == xrubrik.password:
                session['logged_in'] = True
                session['username'] = request.form['initials']
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
    flash("Before IF")

    if request.method == "POST" and form.validate():
            initials  = form.initials.data
            firstname  = form.firstname.data
            lastname  = form.lastname.data
            email = form.email.data
            password = form.password.data
            xrubrik = db.session.query(Teachers.initials).filter(Teachers.initials == initials).first()
            if xrubrik:
                flash("That username is already taken, please choose another")
                return render_template('register.html.j2', form=form)
            else:
                flash("Thanks for registering!")
                flash(initials)
                record = Teachers(**{
                    'initials' : initials,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'email' : email,
                    'password' : password
                })
                db.session.add(record)
                db.session.commit()
                return redirect(url_for('login_page'))


    flash("Please register!")
    return render_template("register.html.j2", form=form)






@app.route('/select2')
def select21():
    #flash("That username is already taken, please choose another")
    #return render_template('/select2/test.html')
    return "Hejja"





@app.route('/background_process', methods=['GET', 'POST'])
def background_process():
    #return json.dumps({'value': 'OK'})
    print json.dumps([{"text": "Hej", "value": 1}, {"value": 2, "text": "Hopp"}], separators=(',', ':'))
    return json.dumps([{"text": "Hej", "value": 1}, {"value": 2, "text": "Hopp"}], separators=(',', ':'))








@app.route('/user_edit_titlename1', methods=['GET', 'POST'])
def user_edit_titlename1():
    id = request.form["pk"]
    print id
    print "he"

    varteacher = Teachers.query.get(id)
    print varteacher
    print varteacher.firstname.encode('utf-8')
    print request.form["value"].encode('utf-8')
    varteacher.firstname = request.form["value"]
    print "Efter"
    varteacher = Teachers.query.get(id)
    print varteacher.firstname.encode('utf-8')
    result = {}
    db.session.commit()
    return json.dumps(result)





@app.route('/user_edit_titlename2', methods=['GET', 'POST'])
def user_edit_titlename2():
    id = request.form["pk"]
    print id
    print "hej"

    varteacher = Teachers.query.get(id)
    print varteacher
    print varteacher.lastname.encode('utf-8')
    print request.form["value"].encode('utf-8')
    varteacher.lastname = request.form["value"]
    print "Efter"
    varteacher = Teachers.query.get(id)
    print varteacher.lastname.encode('utf-8')
    result = {}
    db.session.commit()
    return json.dumps(result)



@app.route('/user_edit_course_name/<int:page>', methods=['GET', 'POST'])
def user_edit_course_name(page):
    id = request.form["pk"]
    #print id
    #print "hej"

    varcourse = Courses.query.get(id)
    #print varteacher
    #print varteacher.lastname.encode('utf-8')
    #print request.form["value"].encode('utf-8')
    varcourse.name = request.form["value"]
    #print "Efter"
    #varteacher = Teachers.query.get(id)
    #print varteacher.lastname.encode('utf-8')
    result = {}
    db.session.commit()
    return json.dumps(result)


@app.route('/user_edit_course_examiner/<int:page>', methods=['GET', 'POST'])
def user_edit_course_examiner(page):
    id = request.form["pk"]

    tempvar = Courses.query.get(id)

    uservar = Teachers.query.filter_by(initials=request.form["value"]).first()

    tempvar.examiner = uservar


    #tempvar.name = request.form["value"]
    #print "TEST"
    #print varteacher
    #print varteacher.lastname.encode('utf-8')
    #print request.form["value"].encode('utf-8')
    #examvar = db.session.query(Examiners.id).join(Examiners.teachers).filter(Teachers.initials == request.form["value"]).first()
    #flash(tempvar.initials)
    #tempvar.examiners_id = Teachers.query.filter_by(initials="AH").first().id
    #tempvar.examiners.teachers.initials = "AX"
    #print "Efter"
    #varteacher = Teachers.query.get(id)
    #print varteacher.lastname.encode('utf-8')
    result = {}
    db.session.commit()
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





@app.errorhandler(404)
def page_not_found(e):
    xrubrik = db.session.query(Courses.code).filter(Courses.id == 17).first()
    xkurskod = db.session.query(Courses.name).filter(Courses.id == 17).first()
    #return render_template('blocks.html.j2', varia="TESTVARIABEL", varrubrik=xrubrik[0], xkurskod=xkurskod[0], courseid=17)
    return "fel"



def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print '=' * 80
    print ' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2))
    print '=' * 80
    print query_str.rstrip('\n')
    print '=' * 80 + '\n'

    return response

app.after_request(sql_debug)













'''
#test1 = Teachers(username='Test1')
#db.session.add(test1)
#db.session.commit()
#test1.courses.append(Courses.query.first())
#db.session.commit()
#return "Hello, World!"
#Courseclassvar = Courses.query.filter(Courses.code == "AI1125").first().classes.all()
#Coursedatevar = Courses.query.filter(Courses.code == "AI1125").first().dates.all()

#Classvar = Classes.query.all()

#Datevar = Dates.query.order_by(Dates.id).all()

#uvar = Classes.query.join(Dates, Courses).filter(Courses.code == "AI1147").order_by(Dates.date).first()
#uvar = Classes.query.join(Dates, Courses).filter(Courses.code.startswith("AI114")).order_by(Dates.date).first()


#print uvar.__dict__

#xvar = db.session.query(Teachers.firstname, Classes.content).group_by(Teachers.firstname).all()

#for item in xvar:
    #print item

#xvar = db.session.query(func.count(Teachers.initials)).all()

#for item in xvar:
    #print item[0]

xvar = db.session.query(Teachers.firstname, func.count(Teachers.firstname)).group_by(Teachers.firstname).all()

for item in xvar:
    print item


xvar = db.session.query(Teachers.firstname, func.count(Classes.id)).join(Teachers.classes).group_by(Teachers.firstname).all()

for item in xvar:
    print item


xvar = db.session.query(Courses.code, Classes.content).join(Courses.classes).group_by(Courses.code).all()
for item in xvar:
    print item


xvar = db.session.query(Teachers.firstname, func.count(Courses.code)).join(Teachers.classes).join(Classes.courses).group_by(Teachers.firstname).order_by(func.count(Courses.id)).all()
for item in xvar:
    print item



xvar = db.session.query(Courses.code, Teachers.firstname).distinct().join(Courses.classes).join(Classes.teachers).all()
for item in xvar:
    print item



subq = db.session.query(Courses.code, Teachers.firstname).distinct().join(Courses.classes).join(Classes.teachers).subquery()


xvar = db.session.query(subq.c.firstname, func.count(subq.c.code)).group_by(subq.c.firstname).order_by(desc(func.count(subq.c.code))).slice(0, 5).all()
for item in xvar:
    print item





xvar = db.session.query(func.avg(Classes.starttime)).all()
for item in xvar:
    print item


xvar = db.session.query(func.avg(Classes.endtime - Classes.starttime)).all()
for item in xvar:
    print item

xvar = db.session.query(func.sum(Classes.endtime - Classes.starttime)).all()
for item in xvar:
    print item



# Lista med antal salstimmar per kurs i sjunkande ordning
xvar = db.session.query(Courses.code, func.sum(Classes.endtime - Classes.starttime)).join(Courses.classes).group_by(Courses.code).order_by(desc(func.sum(Classes.endtime - Classes.starttime))).all()
for item in xvar:
    print item








# Lista med datum som anvands i en kurs
xvar = db.session.query(Dates.date).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.code == "AI1147").order_by(Dates.date).all()
for item in xvar:
    print item


# Lista med kurstillfallen som anvands i en kurs
xvar = db.session.query(Dates.date, Classes.starttime, Classes.endtime, Classes.content).distinct().join(Dates.classes).join(Classes.courses).filter(Courses.code == "AI1147").order_by(Dates.date).order_by(Classes.starttime).all()
for item in xvar:
    print item


# Lista med antal salstimmar per larare i sjunkande ordning
xvar = db.session.query(Teachers.initials, func.sum(Classes.endtime - Classes.starttime)).join(Teachers.classes).group_by(Teachers.initials).order_by(desc(func.sum(Classes.endtime - Classes.starttime))).all()
for item in xvar:
    print item


# Lista med antal salstimmar per rum i sjunkande ordning
xvar = db.session.query(Rooms.name, func.sum(Classes.endtime - Classes.starttime)).join(Rooms.classes).group_by(Rooms.name).order_by(desc(func.sum(Classes.endtime - Classes.starttime))).all()
for item in xvar:
    print item

# Lista med kurser i stigande ordning
xvar = db.session.query(Courses.code, Courses.name).order_by(Courses.code).all()
for item in xvar:
    print item



xvar = testar("AI1147")

'''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
    #app.run()
