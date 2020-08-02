from flask import Flask, render_template, request, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask import Response
import requests

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'postgres://kumngmqflcmynz:4200ddda909a206db818cef5a42c53fc15f38d0a2dfff8dddf546eaf1cc42dfd@ec2-54-75-244-161.eu-west-1.compute.amazonaws.com:5432/draq6o35ulr54'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True       # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    biz_bool = db.Column('biz_bool', db.Boolean(), nullable=False, server_default='0')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    name = db.Column(db.String(100), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Jobs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    poster_id = db.Column(db.Integer())
    biz_name  = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    pay = db.Column(db.String(1000))
    short = db.Column(db.String(1000))
    status = db.Column(db.String(1000))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')) #the foreign key to the user table

class Application(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    job_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')) #the foreign key to the user table
    poster_id = db.Column(db.Integer())

# Create all database tables
db.create_all()

#Create User
user = User(
                email="troy@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Troy",
                biz_bool=0,
            )
db.session.add(user)
user = User(
                email="tieg@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Tieg",
                biz_bool=0,
            )
db.session.add(user)
user = User(
                email="thomas@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Thomas",
                biz_bool=0,
            )
db.session.add(user)
user = User(
                email="cutters@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Cutters",
                biz_bool=1,
            )
db.session.add(user)
user = User(
                email="uber@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Uber",
                biz_bool=1,
            )
db.session.add(user)
user = User(
                email="build@gmail.com",
                email_confirmed_at=datetime.datetime.utcnow(),
                password="password",
                name="Build",
                biz_bool=1,
            )
db.session.add(user)
# Add jobs to the database
job = Jobs(
            title="Brick layer",
            location="Cape Town",
            category="Building",
            pay="R1000",
            short="Brick layer needed",
            poster_id=poster_id,
            biz_name="Uber",
            status="0",
        )
db.session.add(job)
job = Jobs(
            title="Cleaner",
            location="Cape Town",
            category="Cleaning",
            pay="R750",
            short="Cleaner needed",
            poster_id=poster_id,
            biz_name="Cutters",
            status="0",
        )
db.session.add(job)
job = Jobs(
            title="Handyman",
            location="Cape Town",
            category="General",
            pay="R500",
            short="In need of a good handyman",
            poster_id=poster_id,
            biz_name="Uber",
            status="0",
        )
db.session.add(job)
job = Jobs(
            title="Construction worker",
            location="Cape Town",
            category="Building",
            pay="R1250",
            short="I need a strong guy",
            poster_id=poster_id,
            biz_name="Build",
            status="0",
        )
db.session.add(job)
job = Jobs(
            title="Kitchen staff",
            location="Cape Town",
            category="Building",
            pay="R250",
            short="Helping around the kitchen",
            poster_id=poster_id,
            biz_name="Cutters",
            status="0",
        )
db.session.add(job)


db.session.commit()