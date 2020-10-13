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
            # Do calcs on answers starting here
            answers = []
            for answer in range (1, NUM_QUESTIONS+1):
                if answer==25:
                    answers = answers + (request.form.getlist(str(answer)))
                else:
                    answers.append(request.form[str(answer)])
            print(answers, flush=True)

            # Calculate sums for each trait
            sumE = 0
            sumI = 0
            sumS = 0
            sumN = 0
            sumT = 0
            sumF = 0
            sumJ = 0
            sumP = 0
            for answer in answers:
                if answer[0] == 'E':
                    sumE += int(answer[-1])
                elif answer[0] == 'I':
                    sumI += int(answer[-1])
                elif answer[0] == 'S':
                    sumS += int(answer[-1])
                elif answer[0] == 'N':
                    sumN += int(answer[-1])
                elif answer[0] == 'T':
                    sumT += int(answer[-1])
                elif answer[0] == 'F':
                    sumF += int(answer[-1])
                elif answer[0] == 'J':
                    sumJ += int(answer[-1])
                elif answer[0] == 'P':
                    sumP += int(answer[-1])
            print('Sums are: ', sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, flush=True)

            personalityType = ""
            if(sumI >= sumE):
                personalityType += "I"
            else:
                personalityType += "E"
            if(sumN >= sumS):
                personalityType += "N"
            else:
                personalityType += "S"
            if(sumT >= sumF):
                personalityType += "T"
            else:
                personalityType += "F"
            if(sumP >= sumJ):
                personalityType += "P"
            else:
                personalityType += "J"

            # Send to database
            conn = get_db_connection()
            conn.execute("INSERT INTO submissions (sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, personalityType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, personalityType))
            conn.commit()
            conn.close()
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
