from flask import Flask, render_template, request, flash, url_for, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc, create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111111111@localhost/e52'
#db = SQLAlchemy(app)

engine = create_engine('mysql://root:1111111111@localhost/e52', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


#session = Session(app)


teachers_classes = Table('teachers_classes',
    Column('teachers_id', Integer, ForeignKey('teachers.id')),
    Column('classes_id', Integer, ForeignKey('classes.id'))
)

rooms_classes = Table('rooms_classes',
    Column('rooms_id', Integer, ForeignKey('rooms.id')),
    Column('classes_id', Integer, ForeignKey('classes.id'))
)



dates_courses = Table('dates_courses',
    Column('dates_id', Integer, ForeignKey('dates.id')),
    Column('courses_id', Integer, ForeignKey('courses.id'))
)

dates_rooms = Table('dates_rooms',
    Column('dates_id', Integer, ForeignKey('dates.id')),
    Column('rooms_id', Integer, ForeignKey('rooms.id'))
)

dates_teachers = Table('dates_teachers',
    Column('dates_id', Integer, ForeignKey('dates.id')),
    Column('teachers_id', Integer, ForeignKey('teachers.id'))
)

'''
rooms_schedules = Table('rooms_schedules',
    Column('rooms_id', Integer, ForeignKey('rooms.id')),
    Column('schedules_id', Integer, ForeignKey('schedules.id'))
)

teachers_schedules = Table('teachers_schedules',
    Column('teachers_id', Integer, ForeignKey('teachers.id')),
    Column('schedules_id', Integer, ForeignKey('schedules.id'))
)


dates_classes = Table('dates_classes',
    Column('dates_id', Integer, ForeignKey('dates.id')),
    Column('classes_id', Integer, ForeignKey('classes.id'))
)
'''

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    pets = relationship('Pet', backref='owner', lazy='dynamic')

class Pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    owner_id = Column(Integer, ForeignKey('person.id'))

# One-to-many. Parent to Rooms
class Roomtypes(Base):
    __tablename__ = 'roomtypes'
    id = Column(Integer, primary_key=True)
    roomtype = Column(String(30))
    cost = Column(Integer)
    rooms = relationship('Rooms', backref='roomtypes', lazy='dynamic')

# One-to-many. Child to Roomtypes
class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    seats = Column(Integer)
    roomtypes_id = Column(Integer, ForeignKey('roomtypes.id'))
    #schedules = relationship('Schedules', secondary=rooms_schedules, backref=backref('rooms', lazy='dynamic'))
    classes = relationship('Classes', secondary=rooms_classes, backref=backref('rooms', lazy='dynamic'))

class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    initials = Column(String(30))
    email = Column(String(30))
    firstname = Column(String(30))
    lastname = Column(String(30))
    #schedules = relationship('Schedules', secondary=teachers_schedules, backref=backref('teachers', lazy='dynamic'))
    classes = relationship('Classes', secondary=teachers_classes, backref=backref('teachers', lazy='dynamic'))

class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    name = Column(String(30))
    schedule_exists = Column(Boolean, default=False)
    year = Column(Integer)
    #schedules = relationship('Schedules', backref='courses', lazy='dynamic')
    classes = relationship('Classes', backref='courses', lazy='dynamic')

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    #roomtypes_id = Column(Integer, ForeignKey('roomtypes.id'))

class Dates(Base):
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    #roomtypes_id = Column(Integer, ForeignKey('roomtypes.id'))
    #classes = relationship('Classes', secondary=dates_classes, backref=backref('dates', lazy='dynamic'))
    courses = relationship('Courses', secondary=dates_courses, backref=backref('dates', lazy='dynamic'))
    rooms = relationship('Rooms', secondary=dates_rooms, backref=backref('dates', lazy='dynamic'))
    teachers = relationship('Teachers', secondary=dates_teachers, backref=backref('dates', lazy='dynamic'))
    classes = relationship('Classes', backref='dates', lazy='dynamic')

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    #date = Column(String(30))
    content = Column(String(100))
    courses_id = Column(Integer, ForeignKey('courses.id'))
    dates_id = Column(Integer, ForeignKey('dates.id'))

'''
class Schedules(Base):
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    content = Column(String(100))
    courses_id = Column(Integer, ForeignKey('courses.id'))

'''

@app.route('/')
def index():
    #test1 = Teachers(username='Test1')
    #session.add(test1)
    #session.commit()
    #test1.courses.append(Courses.query.first())
    #session.commit()
    #return "Hello, World!"
    '''
    Courseclassvar = Courses.query.filter(Courses.code == "AI1125").first().classes.all()
    Coursedatevar = Courses.query.filter(Courses.code == "AI1125").first().dates.all()

    Classvar = Classes.query.all()

    Datevar = Dates.query.order_by(Dates.id).all()


    unlist = Classes.query.join(Dates, Courses).filter(Courses.code == "AI1147").order_by(Dates.date).all()
    '''
    print(session.query(Courses).first())
    '''

    unlist = []

    for item in unlistx:
        unlist.append(item.content)


    unlist = list(set(unlist))




    unlist = list(set(unlist))

    unlist = [val for val in unlist if val in Courseclassvar]

    unlist = list(set(unlist))

'''

    return "hej"
    #return render_template('main.html', Coursevar = Courseclassvar, Datevar = Coursedatevar, unlist = unlist, Roomtypes = Roomtypes(), Rooms = Rooms(), Teachers = Teachers(), Courses = Courses(), Roles = Roles(), Dates = Dates(), Classes = Classes())







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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1080)
