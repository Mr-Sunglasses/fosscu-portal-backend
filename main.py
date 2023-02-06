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


class Puppy(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    # One to Many ie . One Puppy can Have many Toys
    toys = db.relationship('Toy', backref='puppy', lazy='dynamic')
    # One to One ie . One Puppy can have one Owner
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"The Puppy {self.name} has owner {self.owner.owner_name}."
        else:
            return f"The Puppy {self.name} has no Owner."

    def report_toys(self):
        print("Here are Puppy toys")
        for i in self.toys:
            print()

class Toy(db.Model):

    __tablename__ = 'toys'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, item_name, puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key = True)
    owner_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, owner_name, puppy_id):
        self.owner_name = owner_name
        self.puppy_id = puppy_id


