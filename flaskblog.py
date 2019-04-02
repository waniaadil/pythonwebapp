from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, session, abort, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import sys
import boto3
from botocore.exceptions import ClientError


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
instance_id ='i-0128971b12afa1401'
action = 'ON'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return User('{self.username}', '{self.email}', '{self.image_file}')



@app.route("/", methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return login()

@app.route("/home")
def home():
    form = PostForm()
    if not (session.get('logged_in')):
        return render_template('login.html')
    else:    
        return render_template('home.html')


@app.route("/about")
def about():
    form = PostForm()
    if not (session.get('logged_in')):
        return render_template('login.html')
    else:
        return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)






#api call


def main():
    if action == "start":
        startInstance()
    elif action == "stop":
        stopInstance()
    else :
        print ("please select the action")

@app.route("/config/start", methods=['GET', 'POST'])
def startInstance():
    ec2 = boto3.client('ec2')
    ec2.start_instances(InstanceIds=[instance_id] )
    return render_template('config1.html')

@app.route("/config/stop", methods=['GET', 'POST'])
def stopInstance():
    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=[instance_id] )
    return render_template('config2.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000 , debug=True)
