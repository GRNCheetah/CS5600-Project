from flask import Blueprint, Flask, render_template, request
import sqlite3
app = Flask(__name__)

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
