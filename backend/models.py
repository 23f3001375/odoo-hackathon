from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime
db=SQLAlchemy()

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    dob=db.Column(db.String(20),nullable=False)
    fs_uniquifier=db.Column(db.String(50),nullable=False,unique=True)
    active=db.Column(db.Boolean,nullable=False)
    roles=db.relationship("Role",backref="user",secondary="user_roles")

class Role(db.Model,RoleMixin):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False,unique=True)
    description=db.Column(db.String(42))

class UserRoles(db.Model):
    __tablename__="user_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    role_id=db.Column(db.Integer,db.ForeignKey("roles.id"))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    location = db.Column(db.String(200))
    registration_start_date = db.Column(db.DateTime, nullable=False)
    registration_end_date = db.Column(db.DateTime, nullable=False)
    event_start_date = db.Column(db.DateTime, nullable=False)
    event_end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending') 
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request= db.relationship('EventRequest', backref='event', lazy=True)



class EventRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    number_of_people = db.Column(db.Integer, default=1)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  
