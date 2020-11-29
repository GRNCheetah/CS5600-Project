
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask import Blueprint, Flask, render_template, request, Response, redirect, url_for
import sqlite3
from init_db import *
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import pandas as pd
import collections
import io

app = Flask(__name__)

# Secret key of random bytes (used for sessions and user login implementation)
# Generated randomly each time the app is run
app.secret_key = os.urandom(16)

# Flask SQL Alchemy Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# Potential TODO: Get the submissions stuff set up on SQL alchemy for
# consistency and easy of use throughout the program
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
        db_query = User.query.filter_by(username=request.form.get("username")).first()

        if db_query is None:

            # Create new user
            # Generate salt for storing passwords in the database
            uname = request.form.get("username")
            salt = os.urandom(32)
            hash_pass = hashlib.pbkdf2_hmac('sha256', request.form.get("password").encode('utf-8'), salt, 100000)
            db.session.add(User(username=uname, password=hash_pass, salt=salt))
            db.session.commit()

            return redirect(url_for('login'))
        else:
            return render_template("new_user.html", user=current_user, error="Username already in use!")

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

        return render_template("login.html", user=current_user, error="Incorrect Username or Password")

    return render_template("login.html", user=current_user)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        tmp_user = current_user.username
        logout_user()
        return render_template("logout.html", user=tmp_user)

    return redirect(url_for('login'))


NUM_QUESTIONS = 50

conn = init_tables()



@app.route('/summary_plot.png')
def plot_summary_png():
    fig = update_summary_graph()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/EI_plot.png')
def plot_EI_png():
    fig = update_trait_graph()[0]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/SN_plot.png')
def plot_SN_png():
    fig = update_trait_graph()[1]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/TF_plot.png')
def plot_TF_png():
    fig = update_trait_graph()[2]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/JP_plot.png')
def plot_JP_png():
    fig = update_trait_graph()[3]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def update_summary_graph():
    # Retrieve all submission data from database.
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()

    summary = {
        'Extrovert': 0,
        'Introvert': 0,
        'Sensor': 0,
        'Intuitive': 0,
        'Thinker': 0,
        'Feeler': 0,
        'Judger': 0,
        'Perceiver': 0,
    }

    # Store aggregate database data.
    for i in range(0, len(posts)):
        summary['Extrovert'] += posts[i]['sumE']
        summary['Introvert'] += posts[i]['sumI']
        summary['Sensor'] += posts[i]['sumS']
        summary['Intuitive'] += posts[i]['sumN']
        summary['Thinker'] += posts[i]['sumT']
        summary['Feeler'] += posts[i]['sumF']
        summary['Judger'] += posts[i]['sumJ']
        summary['Perceiver'] += posts[i]['sumP']

    # Sort trait sums in ascending order.
    summary = collections.OrderedDict(sorted(summary.items(), key=lambda kv: kv[1]))

    # Generate `Trait Distribution` graph.
    colors = []
    for val in summary.keys():
        if val == 'Extrovert' or val == 'Introvert':
            colors.append('blue')
        elif val == 'Sensor' or val == 'Intuitive':
            colors.append('green')
        elif val == 'Thinker' or val == 'Feeler':
            colors.append('red')
        elif val == 'Judger' or val == 'Perceiver':
            colors.append('orange')

    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(summary.keys(), summary.values(), width=0.8, color=colors)
    ax.set_xlabel('Trait', fontsize=14)
    ax.set_ylabel('Total Trait Sum', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=13)
    fig.suptitle('Individual Trait Distribution', fontsize=16)

    return fig


def update_trait_graph():
    # Retrieve all submission data from database.
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()

    traits = {
        'Extrovert': 0,
        'Introvert': 0,
        'Sensor': 0,
        'Intuitive': 0,
        'Thinker': 0,
        'Feeler': 0,
        'Judger': 0,
        'Perceiver': 0,
    }
    # Store aggregate database data.
    for i in range(0, len(posts)):
        if(posts[i]['personalityType'][0] == 'E'):
            traits['Extrovert'] += 1
        else:
            traits['Introvert'] += 1
        if(posts[i]['personalityType'][1] == 'S'):
            traits['Sensor'] += 1
        else:
            traits['Intuitive'] += 1
        if(posts[i]['personalityType'][2] == 'T'):
            traits['Thinker'] += 1
        else:
            traits['Feeler'] += 1
        if(posts[i]['personalityType'][3] == 'J'):
            traits['Judger'] += 1
        else:
            traits['Perceiver'] += 1

    trait_sets = [['Extrovert', 'Introvert'], ['Sensor', 'Intuitive'], ['Thinker', 'Feeler'], ['Judger', 'Perceiver']]
    figures = []
    
    # Construct graph for each trait
    for subset in trait_sets:
        traits_subset = {key: traits[key] for key in subset}
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.barh(list(traits_subset.keys()), list(traits_subset.values()), height=0.8)
        ax.set_xlabel('Trait Sum', fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.suptitle(subset[0] + ' vs ' + subset[1], fontsize=16)
        figures.append(fig)

    return figures


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
                "userID": None,
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

            # Check if there is a user logged in
            # If so we get their username and insert that into
            # the submission in the database, else we simply
            # insert None (which will display as anonymous on
            # the data page)
            if not current_user.is_authenticated:
                u_id = None
            else:
                u_id = current_user.username
                result["username"] = u_id

            # Send to database
            conn = get_db_connection()
            conn.execute("INSERT INTO submissions (userID, sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, personalityType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (u_id, result["sumE"], result["sumI"], result["sumS"], result["sumN"], result["sumT"], result["sumF"], result["sumJ"], result["sumP"], result["personalityType"]))
            conn.commit()
            conn.close()
            return redirect(url_for('results'))
        else:
            return render_template("quiz.html")
    except Exception as e:
        print("error:", e)
        return render_template("quiz.html", error="something")


@app.route("/results")
def results(data=None):
    # If there is a current user logged in, get their specific result
    # and display it on the results page
    if current_user.is_authenticated:
        conn = get_db_connection()
        posts = conn.execute("SELECT * FROM submissions WHERE userID=\"" + current_user.username + "\";").fetchall()
        conn.close()

        # Check if the current user has a submission.
        # If not, display the default page
        if posts != []:
            return render_template("results.html", posts=posts)

    return render_template("results.html", posts={})


@app.route("/data")
def data():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()
    print(posts)
    return render_template("data.html", posts=posts)

@app.route("/personalities/<p_type>")
def personalities(p_type=""):
    p_type = p_type.lower()
    TYPES = ['entj', 'intj', 'entp', 'intp', 'enfj', 'infj', 'enfp', 'infp', 'estj', 'istj', 'esfj', 'isfj', 'estp', 'istp', 'esfp', 'isfp']
    INFO = {'entj': ('The Commander', 'Frank, decisive, assume leadership readily. Quickly see illogical and inefficient procedures and policies, develop and implement comprehensive systems to solve organizational problems. Enjoy long-term planning and goal setting. Usually well informed, well read, enjoy expanding their knowledge and passing it on to others. Forceful in presenting their ideas.'),
            'intj': ('The Mastermind', 'Have original minds and great drive for implementing their ideas and achieving their goals. Quickly see patterns in external events and develop long-range explanatory perspectives. When committed, organize a job and carry it through. Skeptical and independent, have high standards of competence and performance - for themselves and others.'),
            'entp': ('The Visionary', 'Quick, ingenious, stimulating, alert, and outspoken. Resourceful in solving new and challenging problems. Adept at generating conceptual possibilities and then analyzing them strategically. Good at reading other people. Bored by routine, will seldom do the same thing the same way, apt to turn to one new interest after another.'), 
            'intp': ('The Architect', 'Seek to develop logical explanations for everything that interests them. Theoretical and abstract, interested more in ideas than in social interaction. Quiet, contained, flexible, and adaptable. Have unusual ability to focus in depth to solve problems in their area of interest. Skeptical, sometimes critical, always analytical.'), 
            'enfj': ('The Teacher', 'Warm, empathetic, responsive, and responsible. Highly attuned to the emotions, needs, and motivations of others. Find potential in everyone, want to help others fulfill their potential. May act as catalysts for individual and group growth. Loyal, responsive to praise and criticism. Sociable, facilitate others in a group, and provide inspiring leadership.'), 
            'infj': ('The Counseler', 'Seek meaning and connection in ideas, relationships, and material possessions. Want to understand what motivates people and are insightful about others. Conscientious and committed to their firm values. Develop a clear vision about how best to serve the common good. Organized and decisive in implementing their vision.'), 
            'enfp': ('The Champion', 'Warmly enthusiastic and imaginative. See life as full of possibilities. Make connections between events and information very quickly, and confidently proceed based on the patterns they see. Want a lot of affirmation from others, and readily give appreciation and support. Spontaneous and flexible, often rely on their ability to improvise and their verbal fluency.'), 
            'infp': ('The Healer', 'Idealistic, loyal to their values and to people who are important to them. Want an external life that is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened.'), 
            'estj': ('The Supervisor', 'Practical, realistic, matter-of-fact. Decisive, quickly move to implement decisions. Organize projects and people to get things done, focus on getting results in the most efficient way possible. Take care of routine details. Have a clear set of logical standards, systematically follow them and want others to also. Forceful in implementing their plans.'), 
            'istj': ('The Inspector', 'Quiet, serious, earn success by thoroughness and dependability. Practical, matter-of-fact, realistic, and responsible. Decide logically what should be done and work toward it steadily, regardless of distractions. Take pleasure in making everything orderly and organized - their work, their home, their life. Value traditions and loyalty.'), 
            'esfj': ('The Provider', 'Warmhearted, conscientious, and cooperative. Want harmony in their environment, work with determination to establish it. Like to work with others to complete tasks accurately and on time. Loyal, follow through even in small matters. Notice what others need in their day-by-day lives and try to provide it. Want to be appreciated for who they are and for what they contribute.'), 
            'isfj': ('The Protector', 'Quiet, friendly, responsible, and conscientious. Committed and steady in meeting their obligations. Thorough, painstaking, and accurate. Loyal, considerate, notice and remember specifics about people who are important to them, concerned with how others feel. Strive to create an orderly and harmonious environment at work and at home.'), 
            'estp': ('The Dynamo', 'Flexible and tolerant, they take a pragmatic approach focused on immediate results. Theories and conceptual explanations bore them - they want to act energetically to solve the problem. Focus on the here-and-now, spontaneous, enjoy each moment that they can be active with others. Enjoy material comforts and style. Learn best through doing.'), 
            'istp': ('The Craftsperson', 'Tolerant and flexible, quiet observers until a problem appears, then act quickly to find workable solutions. Analyze what makes things work and readily get through large amounts of data to isolate the core of practical problems. Interested in cause and effect, organize facts using logical principles, value efficiency.'), 
            'esfp': ('The Entertainer', 'Outgoing, friendly, and accepting. Exuberant lovers of life, people, and material comforts. Enjoy working with others to make things happen. Bring common sense and a realistic approach to their work, and make work fun. Flexible and spontaneous, adapt readily to new people and environments. Learn best by trying a new skill with other people.'), 
            'isfp': ('The Composer', 'Quiet, friendly, sensitive, and kind. Enjoy the present moment, what\'s going on around them. Like to have their own space and to work within their own time frame. Loyal and committed to their values and to people who are important to them. Dislike disagreements and conflicts, do not force their opinions or values on others.')}
    print(p_type)
    if p_type in TYPES:
        return render_template("types.html", p_type=p_type.upper(), info=INFO[p_type])
    else:
        return render_template("personalities.html")

if __name__ == '__main__':
    app.run(debug=True)
