from flask import Blueprint, Flask, render_template, request
import sqlite3
app = Flask(__name__)

NUM_QUESTIONS = 26

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
            print("question 25: ", request.form.getlist(str(25)), flush=True)

            # Do calcs on answers starting here
            answers = []
            for answer in range (1, NUM_QUESTIONS+1):
                if answer==25:
                    answers = answers + (request.form.getlist(str(answer)))
                else:
                    answers.append(request.form[str(answer)])
            print(answers, flush=True)
        return render_template("quiz.html")
    except Exception as e:
        print("error")
        return render_template("quiz.html", error="something")


        

    

@app.route("/data")
def data():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()
    return render_template("data.html", posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
