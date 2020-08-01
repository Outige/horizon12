from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.form.getlist('isbusiness') == []:
        # takes employee to employee profile
        return render_template('employee.html')
    else:
        # takes you to the business profile
        return render_template('business.html')

@app.route('/login', methods=['GET'])
def getlogin():
    return render_template('login.html')

@app.route('/login/activate', methods=['POST'])
def login():
    # logic to determine if user exists

    # replace if true with logic to determine if user is a business
    if True:
        return render_template('business.html')
    else:
        return render_template('jobs.html')