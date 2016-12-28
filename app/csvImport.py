import csv

from __init__ import Roomtypes
from __init__ import Rooms
from __init__ import Teachers
from __init__ import Courses
from __init__ import Roles
#from __init__ import Schedules
from __init__ import Dates
from __init__ import Classes
from __init__ import db

from csvCleaner import remove_col, reformat_date, add_col, extract_start_slut_tid, separate_teachers, separate_rooms


#Import CSV-file
def importer():
    with open('static/teachers.csv', 'rb') as f:
        reader = csv.reader(f)
        teachers_list = list(reader)

    with open('static/roomtypes.csv', 'rb') as f:
        reader = csv.reader(f)
        roomtypes_list = list(reader)

    with open('static/rooms.csv', 'rb') as f:
        reader = csv.reader(f)
        rooms_list = list(reader)

    with open('static/courses.csv', 'rb') as f:
        reader = csv.reader(f)
        courses_list = list(reader)

    with open('static/roles.csv', 'rb') as f:
        reader = csv.reader(f)
        roles_list = list(reader)

    with open('static/schedules.csv', 'rb') as f:
        reader = csv.reader(f)
        schedules_list = list(reader)

    return teachers_list, roomtypes_list, rooms_list, courses_list, roles_list, schedules_list


teachers_list, roomtypes_list, rooms_list, courses_list, roles_list, schedules_list = importer()

schedules_list = remove_col(schedules_list, 0)

schedules_list = reformat_date(schedules_list)

schedules_list = add_col(schedules_list)

schedules_list = add_col(schedules_list)

schedules_list = extract_start_slut_tid(schedules_list)

schedules_list = remove_col(schedules_list, 1)






#for i in schedules_list:
#    print i




#Populate tables
for i in roomtypes_list:
    record = Roomtypes(**{
        'roomtype' : i[0],
        'cost' : i[1]
    })
    db.session.add(record)
    db.session.commit()

for i in rooms_list:
    #print i[0]
    record = Rooms(**{
        'name' : i[0],
        'seats' : i[1],
        'roomtypes_id' : Roomtypes.query.filter_by(id=i[2]).first().id
    })
    db.session.add(record)
    db.session.commit()


for i in teachers_list:
    #print i
    record = Teachers(**{
        'username' : i[0],
        'initials' : i[1],
        'email' : i[2],
        'firstname' : i[3],
        'lastname' : i[4]
    })
    db.session.add(record)
    db.session.commit()

for i in courses_list:
    record = Courses(**{
        'code' : i[0],
        'name' : i[1],
        'schedule_exists' : i[2],
        'year' : i[3]


    })
    db.session.add(record)
    db.session.commit()

#print Courses.query.filter_by(code='AI1174').first().id

for i in roles_list:
    record = Roles(**{
        'name' : i[0]
    })
    db.session.add(record)
    db.session.commit()






for i in schedules_list:
    if not Dates.query.filter_by(date=i[0]).first():
        #print "dubbel"
    #else:
        record = Dates(**{
            'date' : i[0]
            })
        db.session.add(record)
        db.session.commit()


for i in schedules_list:
    print i[8]
    #print Dates.query.first().date
    record = Classes(**{
        #'date' : i[0],
        'content' : i[3],
        'starttime' : i[7],
        'endtime' : i[8],
        'courses_id' : Courses.query.filter_by(code=i[5]).first().id,
        'dates_id' : Dates.query.filter_by(date=i[0]).first().id
    })
    db.session.add(record)
    db.session.commit()

    coursevar = Courses.query.filter_by(code=i[5]).first()
    datevar = Dates.query.filter_by(date=i[0]).first()
    #print datevar.date
    datevar.courses.append(coursevar)
    #datevar.classes.append(record)
    db.session.commit()


    words = i[4].split()
    for word in words:
        teachervar = Teachers.query.filter_by(initials=word).first()
        #print teachervar.firstname
        teachervar.classes.append(record)
        teachervar.dates.append(datevar)
        db.session.commit()

    words = i[2].split()
    for word in words:
        roomvar = Rooms.query.filter_by(name=word).first()
        #print roomvar.name
        roomvar.classes.append(record)
        roomvar.dates.append(datevar)

        db.session.commit()



'''
schedules_list = separate_teachers(schedules_list)

schedules_list = [schedules_list[x:x+9] for x in xrange(0, len(schedules_list), 9)]

schedules_list = separate_rooms(schedules_list)

schedules_list = [schedules_list[x:x+9] for x in xrange(0, len(schedules_list), 9)]



for i in schedules_list:
    #print i[5]
    record = Schedules(**{
        'date' : i[0],
        'content' : i[3],
        'courses_id' : Courses.query.filter_by(code=i[5]).first().id
    })
    db.session.add(record)
    db.session.commit()

    #print i[2]
    #print i[3]
    #print i[5]
    teachervar = Teachers.query.filter_by(initials=i[4]).first()
    #print teachervar.firstname
    teachervar.schedules.append(record)
    db.session.commit()

    #print i[2]
    roomvar = Rooms.query.filter_by(name=i[2]).first()
    #print roomvar.name
    roomvar.schedules.append(record)
    db.session.commit()
'''
