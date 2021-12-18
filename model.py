from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = "people"
    person_id = db.Column('person_id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    school_city = db.Column('schocity', db.Text)
    uni_city = db.Column('unicity', db.Text)