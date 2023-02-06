import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

base_dir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCGEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
Migrate(app=app, db=db)

class College(db.Model):
    
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.Text)
    students = db.relationship('Student', backref='college', lazy='dynamic')
    fee = db.Column(db.Integer)

    def __init__(self, college_name, fee):
        self.college_name = college_name
        self.fee = fee
    
    def __repr__(self) -> str:
        return f""
    



class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.text)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))

