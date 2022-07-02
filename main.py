import bcrypt

from forms import LoginForm, RegistrationForm
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
import os
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.debug = True
login_manager = LoginManager(app)
login_manager.login_view = "login"

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id


class Profile():
    def __init__(self, id, name, age, height, weight, seggs):
        self.id = id
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.seggs = seggs


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('Nutrivie')
    curs = conn.cursor()
    curs.execute("SELECT * from login where user_id = (?)", [user_id])
    result = curs.fetchone()
    if result is None:
        return None
    else:
        return User(result[0], result[1], result[2])


def load_profile(user_id):
    conn = sqlite3.connect('Nutrivie')
    curs = conn.cursor()
    curs.execute("SELECT * from profile where user_id = (?)", [user_id])
    result = curs.fetchone()
    if result is None:
        return None
    else:
        return Profile(result[0], result[1], result[2], result[3], result[4], result[5])


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('redirected'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where email = (?)", [form.email.data])
        user = list(curs.fetchone())
        us = load_user(user[0])
        conn.close()
        if us and bcrypt.checkpw(form.password.data.encode('utf-8'), us.password):
            login_user(us, form.remember.data)
            umail = list({form.email.data})[0].split('@')[0]
            flash('Logged in successfully ' + umail)
            return redirect(url_for('redirected'))
        else:
            flash('Could not log in')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('redirected'))
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        hashed = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        curs.execute("INSERT INTO login (email,password) VALUES (?,?)", (form.email.data, hashed))
        conn.commit()
        conn.close()
        umail = list({form.email.data})[0].split('@')[0]
        flash('You have successfully registered ' + umail)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/redirected")
def redirected():
    return "You were redirected. Congrats :)!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
