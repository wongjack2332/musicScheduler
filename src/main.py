from os import close
from flask import Flask, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
import bcrypt
from sql_factory import *
import database_utils as db


def create_app():
    app = Flask(__name__)
    return app


def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


app = create_app()
app.secret_key = 'alskghfdliu12930tu'

connection = db.get_connection()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ufac = UserFactory(connection)
tfac = TimetableFactory(connection)
lfac = LessonFactory(connection)
lrfac = LessonRequestFactory(connection)


@login_manager.user_loader
def user_load(userid):
    connection = db.get_connection()
    try:
        user = UserFactory(connection).sql_get(userid)
        connection.close()
        return user
    except LookupError:
        return None


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        connection = db.get_connection()
        form_result = request.form
        if form_result['password'] != form_result['password-confirm']:
            flash("Passwords do not match", "error")
            return redirect('/signup')
        if form_result['username'] != form_result['username-confirm']:
            flash("Emails do not match", "error")
            return redirect('/signup')

        ufac = UserFactory(connection)
        user = ufac.sql_create(
            usertype=form_result['usertype'])
        user.email = form_result['username']
        user.password = hash_password(form_result['password'])
        ufac.sql_write(user)

        login_user(user)
        db.close_connection(connection)
        return redirect('/dashboard')
    else:
        if current_user.is_authenticated:
            return redirect('/dashboard')
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        connection = db.get_connection()
        ufac = UserFactory(connection)
        form_result = request.form
        username, password = form_result['username'], form_result['password']
        print(ufac.is_user(username))
        if ufac.is_user(username) and bcrypt.checkpw(password.encode(), ufac.sql_from_username(username).password.encode()):
            user = UserFactory(connection).sql_from_username(username)
            login_user(user)
            connection.close()
            return redirect('/dashboard')

        else:
            flash("Invalid username or password", "error")
            connection.close()
            return redirect('/login')
        # except:
        #     print('boo')
        #     flash("error in decrypting password")
        #     return redirect('/login')

    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


db.close_connection(connection)
if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(debug=True, host="0.0.0.0", ssl_context='adhoc')
