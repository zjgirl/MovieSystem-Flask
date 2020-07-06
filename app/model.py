from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db


class MovieInfo(db.Model):
    __tanlename__ = 'movieinfo'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    moviename = db.Column(db.String(128))
    time = db.Column(db.String(128))
    director = db.Column(db.String(128))
    actor = db.Column(db.String(256))
    content = db.Column(db.TEXT)
    posterpath = db.Column(db.String(128))
    moviepath = db.Column(db.String(128))
    imageinfo = db.Column(db.TEXT)

    @staticmethod
    def addMovie(moviename, time, director, actor, content, posterpath, moviepath, imageinfo=""):
        newMovie = MovieInfo(moviename=moviename, time=time, director=director, actor=actor, content=content, posterpath=posterpath, moviepath=moviepath, imageinfo=imageinfo)
        db.session.add(newMovie)
        db.session.commit()

#define user table
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    username = db.Column(db.String(128), unique = True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable = False) #can't be null

    #define some related func there
    #define static method
    @staticmethod
    def addUser(username, password, email):        
        newuser = User(username = username, password= password, email=email) #password1 will pass to the password()
        db.session.add(newuser)
        db.session.commit()

    #@property change a method to property, at the same time create a @password.setter
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

                            
from . import login_manager

#this propriety registe the func to Flask_Login, the func will be loaded when we need to know the info of the current user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
