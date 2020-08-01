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

# Register
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        #add to database
        print(email, password, name)
        if request.form.getlist('isbusiness') == []:
            user = User(
                email=email,
                email_confirmed_at=datetime.datetime.utcnow(),
                password=password,
                name=name,
                biz_bool=0,
            )
            db.session.add(user)
            db.session.commit()
            # takes employee to employee profile
            return redirect('/login')
        else:
            user = User(
                email=email,
                email_confirmed_at=datetime.datetime.utcnow(),
                password=password,
                name=name,
                biz_bool=1,
            )
            db.session.add(user)
            db.session.commit()
            # takes you to the business profile
            return redirect('/login')

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

# Display job form and create job on submission
@app.route('/jobs/create/<int:id>', methods=['GET', 'POST'])
def create_job(id):
    if request.method == 'GET':
        return render_template('job.html', id=id)
    elif request.method == 'POST':
        #return redirect('/business/' + str(id))
        title = request.form.get('title')
        location = request.form.get('location')
        category = request.form.get('category')
        pay = request.form.get('pay')
        short = request.form.get('short')

        user = User.query.filter(User.id == id).first()
        ###########TODO: Get this from the email passed in
        biz_name = user.name #fix
        status = 0 #fix
        poster_id = id #fix
        print(poster_id)
        ##############
        print(short)
        job = Jobs(
            title=title,
            location=location,
            category=category,
            pay=pay,
            short=short,
            poster_id=poster_id,
            biz_name=biz_name,
            status=status,
        )
        db.session.add(job)
        db.session.commit()
        return redirect('/business/' + str(id))
        #return Response(status=201, mimetype='application/json')
        # ! /bsuiness/ you need to get the id somehow
        # go to the business profile
        #return redirect('/business')
        #return render_template('business.html')

# Update job listing TODO: !!!!!!
@app.route('/jobs/update', methods=['POST'])
def update_job():
    user_id = request.form.get('id')
    job_id = request.form.get('job_id')
    print(user_id)
    print(job_id)
    #Jobs.query().filter(Jobs.id == job_id).update({"user_id": user_id})
    #db.session.commit()

    return Response(status=201, mimetype='application/json')
    #db.session.add(job)
    #db.session.commit()

# @app.route('/jobs/update', methods=['POST'])
# def update_job():
#     user_id = request.form.get('id')
#     job_id = request.form.get('job_id')
#     print(user_id)
#     print(job_id)
#     #Jobs.query().filter(Jobs.id == job_id).update({"user_id": user_id})
#     #db.session.commit()
#     return Response(status=201, mimetype='application/json')
#     #db.session.add(job)
#     #db.session.commit()

# Display login form and login on submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # check if the user exists
        # logic to determine if user exists
        #check if the query returns null
        if (User.query.filter(User.email == email).first() != None):
            #user exists
            print("Here")
        else:
            #user does not exist
            return redirect('/login')

        if ( User.query.filter(User.email == email).first().biz_bool ):
            #take to the business page
            return render_template('business.html')
        else:
            #take to the job board
            return redirect(url_for('jobs', email=email))
    elif request.method == 'GET':
        return render_template('login.html')

# Display jobs for users to apply for
@app.route('/jobs')
def jobs():
    # get my id
    print(request.args.get('email'))
    user = User.query.filter(User.email == request.args.get('email')).first()
    users = User.query.all()
    apps = Application.query.all()
    print(apps[0].id)
    #print(user.name)
    jobs = Jobs.query.all()
    #business name
    #jobbies = {}
    #for job in jobs:
        #jobbies.update(job)
        #job.update( {'name' : "poes"} )


    return render_template('jobs.html', jobs=jobs, user=user, users=users, apps=apps)

@app.route('/jobs/apply/<int:job_id>/<int:user_id>/<string:email>')
def apply(job_id, user_id, email):
    poster = Jobs.query.filter(Jobs.id == job_id).first()
    print("***************")
    print(poster)
    application = Application(
        user_id=user_id,
        job_id=job_id,
        poster_id=poster.poster_id
    )
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('jobs', email=email))
    # job_link = '/jobs#job-' + str(job_id)
    # return redirect(job_link)# render_template('jobs.html')

@app.route('/employee/<int:id>')
def employee(id):
    return render_template('employee.html', id=id)

@app.route('/business/<int:id>')
def business(id):
    return render_template('business.html', id=id)

# Block chain
@app.route('/addcontract', methods=['POST'])
def addcontract():
    r = requests.post('http://robabrams.homeip.net:9999/api/create', data = {
    "companyID": "100",
    "userID": "poes",
    "amount": "69",
    "jobID": "4"})
    return Response(status=201, mimetype='application/json')