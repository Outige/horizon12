from flask import Flask, render_template, request, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask import Response


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
    biz_bool = db.Column('biz_bool', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

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
    title = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    pay = db.Column(db.String(1000))
    short = db.Column(db.String(1000))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')) #the foreign key to the user table

# Create all database tables
db.create_all()

# Create 'member@example.com' user with no roles
if not User.query.filter(User.email == 'member@example.com').first():
    user = User(
        email='member@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password='Password1',
    )
    db.session.add(user)
    db.session.commit()

# Create 'admin@example.com' user with 'Admin' and 'Agent' roles
if not User.query.filter(User.email == 'admin@example.com').first():
    user = User(
        email='admin@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password='Password1',
    )
    user.roles.append(Role(name='Admin'))
    user.roles.append(Role(name='Agent'))
    db.session.add(user)
    db.session.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('register.html')

@app.route('/jobs/add', methods=['POST'])
def add_job():
    job = Jobs(
        title='Cleaning needed',
        location='Cape Town',
        category='Cleaning',
        pay='50',
        short='Short description',
        user_id=1,
    )
    db.session.add(job)
    db.session.commit()
    return Response(status=201, mimetype='application/json')


@app.route('/register', methods=['POST'])
def register():
    if request.form.getlist('isbusiness') == []:
        # takes employee to employee profile
        return render_template('employee.html')
    else:
        # takes you to the business profile
        return render_template('business.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('works')
        # logic to determine if user exists

        # replace if true with logic to determine if user is a business
        if True:
            return render_template('business.html')
        else:
            return render_template('jobs.html')
    elif request.method == 'GET':
        return render_template('login.html')