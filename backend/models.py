from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
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
