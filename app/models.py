from __init__ import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    code = db.Column(db.String(30))
    examiner = db.Column(db.String(30))
    department = db.Column(db.String(100))



db.create_all()
db.session.commit()
