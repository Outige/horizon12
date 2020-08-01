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
        # logic to determine if user exists

        # replace if true with logic to determine if user is a business
        if False:
            return render_template('business.html')
        else:
            return redirect('/jobs')
    elif request.method == 'GET':
        return render_template('login.html')

# ?-----------------------
# Employee
# ?-----------------------
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/jobs/apply/<int:job_id>/<int:user_id>')
def apply(job_id, user_id):
    return redirect('/jobs#foo')# render_template('jobs.html')

@app.route('/employee/<int:id>')
def employee(id):
    return render_template('employee.html', id=id)

@app.route('/business/<int:id>')
def business(id):
    return render_template('business.html', id=id)