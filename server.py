import os
import hashlib
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request
app = Flask(__name__)

# Secret key of random bytes (used for sessions and user login implementation)
# app.secret_key = b'\x15\xbe\x9bW\x80\xa1\x8d\xe0\x907\x08D\xfbr\x81\xf7'

# Flask SQL Alchemy Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    '''
    Class to represent the users table in users.db
    2 Attributes, an id (primary key) and a username
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.Integer)


@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        print("HELLO")
        # Create new user
        # Generate salt for storing passwords in the database
        uname = request.form.get("username")
        salt = os.urandom(32)
        hash_pass = hashlib.pbkdf2_hmac('sha256', request.form.get("password").encode('utf-8'), salt, 100000)
        db.session.add(User(username=uname, password=hash_pass, salt=salt))
        db.session.commit()

        print(uname, hash_pass, salt)

    return render_template("new_user.html", user=current_user)


@login_manager.user_loader
def load_user(userid: int):
    return User.query.get(userid)


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        password = request.form.get("password")

        if user is not None:

            # Compute hash from the form's password and compare to stored hash
            new_hash_pass = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user.salt, 100000)

            # Login if hashes match
            if new_hash_pass == user.password:
                login_user(user)
                return render_template("login.html", user=current_user)
            else:
                return render_template("login.html", user=current_user, error="Incorrect Username or Password")
        else:
            return render_template("login.html", user=current_user, error="Incorrect Username or Password")

    return render_template("login.html", user=current_user)


# TODO: Redirect logout to login page if there is no current_user
@app.route('/logout')
@login_required
def logout():
    tmp_user = current_user.username
    logout_user()
    return render_template("logout.html", user=tmp_user)


# TODO: Remove at some point, just a test page for the moment
@app.route('/tmp')
@login_required
def tmp():
    return "The current user is " + current_user.username


NUM_QUESTIONS = 50

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    try:
        if request.method == "POST":
            # Do calcs on answers starting here
            answers = []
            for answer in range (1, NUM_QUESTIONS+1):
                if answer==25:
                    answers = answers + (request.form.getlist(str(answer)))
                else:
                    answers.append(request.form[str(answer)])
            print(answers, flush=True)

            # Calculate sums for each trait
            result = {
                "sumE": 0,
                "sumI": 0,
                "sumS": 0,
                "sumN": 0,
                "sumT": 0,
                "sumF": 0,
                "sumJ": 0,
                "sumP": 0,
                "personalityType": ""
            }
            for answer in answers:
                if answer[0] == 'E':
                    result["sumE"] += int(answer[-1])
                elif answer[0] == 'I':
                    result["sumI"] += int(answer[-1])
                elif answer[0] == 'S':
                    result["sumS"] += int(answer[-1])
                elif answer[0] == 'N':
                    result["sumN"] += int(answer[-1])
                elif answer[0] == 'T':
                    result["sumT"] += int(answer[-1])
                elif answer[0] == 'F':
                    result["sumF"] += int(answer[-1])
                elif answer[0] == 'J':
                    result["sumJ"] += int(answer[-1])
                elif answer[0] == 'P':
                    result["sumP"] += int(answer[-1])
            #print('Sums are: ', sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, flush=True)


            if(result["sumI"] >= result["sumE"]):
                result["personalityType"] += "I"
            else:
                result["personalityType"] += "E"
            if(result["sumN"] >= result["sumS"]):
                result["personalityType"] += "N"
            else:
                result["personalityType"] += "S"
            if(result["sumT"] >= result["sumF"]):
                result["personalityType"] += "T"
            else:
                result["personalityType"] += "F"
            if(result["sumP"] >= result["sumJ"]):
                result["personalityType"] += "P"
            else:
                result["personalityType"] += "J"

            # Send to database
            # TODO: Add user id to submission in database
            conn = get_db_connection()
            conn.execute("INSERT INTO submissions (sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, personalityType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (result["sumE"], result["sumI"], result["sumS"], result["sumN"], result["sumT"], result["sumF"], result["sumJ"], result["sumP"], result["personalityType"]))
            conn.commit()
            conn.close()
            return render_template("results.html", user_result=result)
        else:
            return render_template("quiz.html")
    except Exception as e:
        print("error:", e)
        return render_template("quiz.html", error="something")

@app.route("/results")
def results(data=None):
    return render_template("results.html", user_result={})


@app.route("/data")
def data():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()
    return render_template("data.html", posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
