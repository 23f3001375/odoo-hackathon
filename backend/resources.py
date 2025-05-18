from flask_restful import Api, Resource, reqparse
from models import db, User, Role
from flask_security import auth_required, roles_accepted, roles_required, current_user
from flask import current_app as app, jsonify, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user

api=Api()
parser= reqparse.RequestParser()

class Login(Resource):
    def get(self):
        data=request.get_json()
        if not data['email'] or data['password']:
            return {
                "Message":"Both fields are required"
            },400
        user=app.security.datastore.find_user(email=data['email'])
        if not user:
            return {
                "Message": "User not found"
            },404
        if not user.active:
            return {
                "Message": "You are blocked from using the website"
            },403
        if user:
            if check_password_hash(user.password,data['password']):
                if current_user.is_authenticated:
                    return {
                        "Message":"User already logged in"
                    },400
                login_user(user)
                role=user.roles[0].name if user.roles else "user"
                return {
                    "Message":"Login successful",
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "role":role,
                    "token":user.get_auth_token()
                },200
            return {
                "message":"Invalid password"
            },400
        return {
            "Message":"User not found"
        },404
    
class Register(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        email=data['email']
        dob=data['dob']
        if not username or not password or not email or not dob:
            return {
                "Message":"All fields required to be filled"
            },400
        user=User.query.filter_by(username=username).first()
        if user:
            return {
                "Message":"This username is already taken."
            },400
        if not app.security.datastore.find_user(email=data['email']):
            app.security.datastore.create_user(username=data['username'],email=data['email'],dob=data['dob'],
                                           password=generate_password_hash(data['password']),roles=['user'])
            db.session.commit()
            return {
                "Message":"Account created successfully"
            },201
        return {
            "Message":"User already exists"
        },400