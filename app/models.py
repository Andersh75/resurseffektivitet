from __init__ import db


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30))
    name = db.Column(db.String(30))
    schedule_exists = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)


db.create_all()
db.session.commit()
