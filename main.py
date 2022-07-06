import bcrypt

from forms import LoginForm, RegistrationForm, ProfileForm, HomeForm
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
    def __init__(self, id, email, password, pseudo):
        self.id = id
        self.email = email
        self.password = password
        self.pseudo = pseudo
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

    def get_pseudo(self):
        return self.pseudo


class Profile:
    def __init__(self, pseudo, age, height, weight, seggs):
        self.pseudo = pseudo
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
        return User(result[0], result[1], result[2], result[3])


def load_profile(pseudo):
    conn = sqlite3.connect('Nutrivie')
    curs = conn.cursor()
    curs.execute("SELECT * from profile where pseudo = (?)", [pseudo])
    result = curs.fetchone()
    if result is None:
        return None
    else:
        return Profile(result[0], result[1], result[2], result[3], result[4])


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where email = (?)", [form.email.data])
        user = list(curs.fetchone())
        us = load_user(user[0])
        if us and bcrypt.checkpw(form.password.data.encode('utf-8'), us.password):
            login_user(us, form.remember.data)
            flash('Logged in successfully ' + us.pseudo)
            curs.execute("SELECT * FROM profile where pseudo = (?)", [us.pseudo])
            row = curs.fetchone()
            if row is None:
                conn.close()
                return redirect(url_for('profile'))
            else:
                conn.close()
                return redirect(url_for('home'))
        else:
            conn.close()
            flash('Could not log in')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        hashed = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        curs.execute("INSERT INTO login (email,password,pseudo) VALUES (?,?,?)",
                     (form.email.data, hashed, form.pseudo.data))
        conn.commit()
        conn.close()
        flash('You have successfully registered ' + form.pseudo.data)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        # charger le profile de l'utilisateur
        # remplir le profile avec id
        usps = User.get_pseudo(current_user)
        print(usps)
        print(form.age.data)
        curs.execute(
            "INSERT INTO profile (pseudo,age,weight,height,seggs) VALUES (?,?,?,?,? )",
            (usps, form.age.data, form.weight.data, form.height.data, form.seggs.data))
        conn.commit()
        conn.close()
        flash('You have completed your profile')
        return redirect(url_for('home'))
    return render_template('profile.html', title='Profile', form=form)


@app.route("/home", methods=['GET', 'POST'])
def home():
    form = HomeForm()
    if form.validate_on_submit():
        return redirect(url_for('logout'))
    return render_template('home.html', title='Home', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
