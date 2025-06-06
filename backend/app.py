from flask import Flask, render_template
from flask_security import SQLAlchemyUserDatastore,Security
from werkzeug.security import generate_password_hash,check_password_hash
from config import DevelopmentConfig
from models import db,User,Role
from resources import api,Login,Register,Userlist,ChangeUserStatus,UserHome,AdminHome,Logout

def create_app():
    app=Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    datastore=SQLAlchemyUserDatastore(db,User,Role)
    app.security=Security(app,datastore)
    app.app_context().push()
    return app
    
app=create_app()
api.__init__(app)

with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name="admin",description="The super user above all")
    app.security.datastore.find_or_create_role(name="user",description="The base user")
    db.session.commit()

    if not app.security.datastore.find_user(email="admin@gmail.com"):
        app.security.datastore.create_user(username="admin",email="admin@gmail.com",dob="04-01-2006",
                                           password=generate_password_hash("admin_quiz"),roles=['admin'])
    db.session.commit()

@app.route('/')
def home_webpage():
    return render_template('index.html')

api.add_resource(Login,'/api/login')
api.add_resource(Register,'/api/register')
api.add_resource(Logout,'/api/logout')
api.add_resource(UserHome,'/api/user')
api.add_resource(AdminHome,'/api/admin')
api.add_resource(Userlist,'/api/admin/userlist')
api.add_resource(ChangeUserStatus,'/api/admin/changestatus/<int:user_id>')

if __name__=="__main__":
    app.run()