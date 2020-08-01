from flask import Flask, render_template, request, redirect, url_for


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